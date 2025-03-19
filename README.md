# Marlin PA Tool

A Python-based GUI tool for generating and analyzing Pressure Advance (PA) test G-code for Marlin firmware 3D printers.

## Overview

This tool helps 3D printing enthusiasts calibrate Pressure Advance (Linear Advance) settings for Marlin firmware by:
- Modifying existing G-code to add PA test values (M900 commands)
- Providing a calculator to determine exact PA values based on measurements

## Features

- **G-code Modification:**
  - Loads a G-code file and identifies all Z-layer heights
  - Adds `M900 K[value]` commands starting at a user-selected Z height
  - Optionally adds an `M0` pause command at the start height
  - Preserves all original X, Y, Z, and E movements unchanged

- **GUI Inputs:**
  - PA Start: Initial Pressure Advance value (default: 0.0)
  - PA End: Maximum Pressure Advance value (default: 0.3)
  - PA Step: Increment between PA values (default: 0.002)
  - Z Height Start: Dropdown of detected layer heights to begin PA testing
  - Pause at Z Start: Checkbox to add a pause at the starting height

- **Pressure Advance Calculator:**
  - Calculates: `PA Start + (PA Step × Measured Value) = PA Value`
  - Uses current GUI values for PA Start and PA Step
  - User enters a Measured Value (e.g., height or layer number where quality is optimal)
  - Updates result with each "Calculate" press

- **Output:**
  - Saves modified G-code to a user-specified file
  - Displays Z height and PA value pairs in a results window

## Requirements

- Python 3.x
- Tkinter (usually included with Python)
- No additional external libraries are required

## Installation

1. Ensure Python 3 is installed on your system
2. Download the script file (e.g., `marlin_pa_tool.py`)
3. Run the script: `python marlin_pa_tool.py`

## Usage

1. **Generate Base G-code:**
   - Create a simple tower in your slicer (recommended: 2 shells, 0% infill, no Z-hop)
   - Export the G-code file

2. **Run the Tool:**
   - Open the script to launch the GUI
   - Click "Open G-code File" and select your tower G-code

3. **Configure Settings:**
   - Set PA Start, PA End, and PA Step values
   - Select Z Height Start from the dropdown
   - Check "Pause at Z Start" if desired. This will allow you to mark your start location with a Sharpie.

4. **Process G-code:**
   - Click "Process Layers"
   - Choose a location to save the modified G-code
   - Review the results showing Z heights and corresponding PA values

5. **Print and Calibrate:**
   - Print the modified G-code
   - Observe the print quality at different heights
   - Use the calculator to find the optimal PA value based on your measurement
  
6. **Calculate PA Value:**
   - After printing, measure where the tower looks best (e.g., height in mm)
   - Enter this as the "Measured Value"
   - Click "Calculate" to get the corresponding PA value
   - Enter this value into your slicer setting
   
## Notes

- The tool does not modify existing movement commands (X, Y, Z, E)
- Only adds new lines for `M900 K[value]` and optional `M0`
- PA values are formatted to 4 decimal places in the output
- Works with any G-code containing Z movements in the format `Z[number]`

## License

This is a free, open-source tool. Feel free to modify and distribute it as needed.

## Support

For issues or feature requests, please contact the developer or submit a pull request if hosted on a repository.
