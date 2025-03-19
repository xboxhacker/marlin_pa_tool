import tkinter as tk
from tkinter import filedialog, ttk
import re

class GCodeAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Marlin PA Tool")
        self.z_heights = []
        self.gcode_lines = []

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # File selection
        self.file_btn = tk.Button(self.root, text="Open G-code File", command=self.load_file)
        self.file_btn.grid(row=0, column=0, columnspan=2, pady=10)

        # PA Start
        tk.Label(self.root, text="PA Start:").grid(row=1, column=0, padx=5, pady=5)
        self.pa_start_var = tk.DoubleVar(value=0.0)
        self.pa_start_entry = tk.Entry(self.root, textvariable=self.pa_start_var)
        self.pa_start_entry.grid(row=1, column=1, padx=5, pady=5)

        # PA End
        tk.Label(self.root, text="PA End:").grid(row=2, column=0, padx=5, pady=5)
        self.pa_end_var = tk.DoubleVar(value=0.3)
        self.pa_end_entry = tk.Entry(self.root, textvariable=self.pa_end_var)
        self.pa_end_entry.grid(row=2, column=1, padx=5, pady=5)

        # PA Step
        tk.Label(self.root, text="PA Step:").grid(row=3, column=0, padx=5, pady=5)
        self.pa_step_var = tk.DoubleVar(value=0.002)
        self.pa_step_entry = tk.Entry(self.root, textvariable=self.pa_step_var)
        self.pa_step_entry.grid(row=3, column=1, padx=5, pady=5)

        # Z Height Start dropdown
        tk.Label(self.root, text="Z Height Start:").grid(row=4, column=0, padx=5, pady=5)
        self.z_height_var = tk.StringVar()
        self.z_height_dropdown = ttk.Combobox(self.root, textvariable=self.z_height_var, state='readonly')
        self.z_height_dropdown.grid(row=4, column=1, padx=5, pady=5)

        # Pause checkbox
        self.pause_var = tk.BooleanVar(value=False)
        self.pause_check = tk.Checkbutton(self.root, text="Pause at Z Start", variable=self.pause_var)
        self.pause_check.grid(row=5, column=0, columnspan=2, pady=5)

        # Process button
        self.process_btn = tk.Button(self.root, text="Process Layers", command=self.process_layers)
        self.process_btn.grid(row=6, column=0, columnspan=2, pady=10)

        # Calculation section
        tk.Label(self.root, text="PA Calculation:", font=("Arial", 10, "bold"), justify=tk.LEFT).grid(row=7, column=0, columnspan=2, padx=5, pady=5)
        tk.Label(self.root, text="PA Start + (PA Step × measured_value) = PA Value", justify=tk.LEFT).grid(row=8, column=0, columnspan=2, padx=5, pady=0)
        tk.Label(self.root, text="Measured Value:").grid(row=9, column=0, padx=5, pady=5)
        self.measured_var = tk.DoubleVar(value=0.0)
        self.measured_entry = tk.Entry(self.root, textvariable=self.measured_var)
        self.measured_entry.grid(row=9, column=1, padx=5, pady=5)
        self.calc_btn = tk.Button(self.root, text="Calculate", command=self.calculate_pa)
        self.calc_btn.grid(row=10, column=0, padx=5, pady=5)
        self.calc_result_var = tk.StringVar(value="Result: ")
        tk.Label(self.root, textvariable=self.calc_result_var).grid(row=10, column=1, padx=5, pady=5)

        # Results text area
        self.results_text = tk.Text(self.root, height=10, width=50)
        self.results_text.grid(row=11, column=0, columnspan=2, padx=5, pady=5)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("G-code files", "*.gcode"), ("All files", "*.*")])
        if file_path:
            self.z_heights = []
            self.gcode_lines = []
            with open(file_path, 'r') as file:
                current_z = None
                for line in file:
                    stripped_line = line.strip()
                    self.gcode_lines.append(stripped_line)
                    # Look for Z movements in G0/G1 commands without modifying the line
                    z_match = re.search(r'Z([\d.]+)', stripped_line)
                    if z_match:
                        z_value = float(z_match.group(1))
                        if z_value != current_z and z_value not in self.z_heights:
                            self.z_heights.append(z_value)
                            current_z = z_value
            
            # Sort Z heights and populate dropdown
            self.z_heights.sort()
            self.z_height_dropdown['values'] = [str(z) for z in self.z_heights]
            if self.z_heights:
                self.z_height_dropdown.set(str(self.z_heights[0]))

    def calculate_pa(self):
        try:
            # Fetch current values from GUI each time Calculate is pressed
            pa_start = self.pa_start_var.get()  # Get latest PA Start from user input
            pa_step = self.pa_step_var.get()    # Get latest PA Step from user input
            measured_value = self.measured_var.get()  # Get latest measured value from user input
            result = pa_start + (pa_step * measured_value)
            self.calc_result_var.set(f"Result: {result:.4f}")
        except ValueError:
            self.calc_result_var.set("Result: Invalid input")

    def process_layers(self):
        if not self.z_heights:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "Please load a G-code file first!")
            return

        try:
            pa_start = float(self.pa_start_var.get())
            pa_end = float(self.pa_end_var.get())
            pa_step = float(self.pa_step_var.get())
            z_start = float(self.z_height_var.get())
            pause_at_start = self.pause_var.get()

            # Process G-code and add M900 commands
            modified_gcode = []
            current_pa = pa_start
            z_index = self.z_heights.index(z_start)
            pause_added = False

            for line in self.gcode_lines:
                modified_gcode.append(line)  # Add original line unchanged
                z_match = re.search(r'Z([\d.]+)', line)
                if z_match:
                    z_value = float(z_match.group(1))
                    if z_value in self.z_heights:
                        layer_index = self.z_heights.index(z_value)
                        if layer_index >= z_index:
                            # Add pause at start height if checked and not yet added
                            if pause_at_start and layer_index == z_index and not pause_added:
                                modified_gcode.append("M0 Click to continue")
                                pause_added = True
                            # Add PA command
                            if current_pa <= pa_end:
                                modified_gcode.append(f"M900 K{current_pa:.4f}")
                                current_pa += pa_step

            # Save modified G-code
            output_path = filedialog.asksaveasfilename(defaultextension=".gcode",
                                                     filetypes=[("G-code files", "*.gcode")])
            if output_path:
                with open(output_path, 'w') as f:
                    f.write("\n".join(modified_gcode))

            # Display results
            results = []
            current_pa = pa_start
            for z in self.z_heights[z_index:]:
                if current_pa <= pa_end:
                    if z == z_start and pause_at_start:
                        results.append(f"Z Height: {z} - PA Value: {current_pa:.4f} (Pause)")
                    else:
                        results.append(f"Z Height: {z} - PA Value: {current_pa:.4f}")
                    current_pa += pa_step
                else:
                    break

            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Modified G-code saved to: {output_path}\n\n")
            self.results_text.insert(tk.END, "\n".join(results))

        except ValueError as e:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Error: Please enter valid numerical values\n{e}")
        except Exception as e:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Error processing G-code: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GCodeAnalyzer(root)
    root.mainloop()
