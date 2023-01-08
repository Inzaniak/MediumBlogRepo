import PySimpleGUI as sg
import csv
import json

sg.theme('Dark Blue 3')

layout = [
    [sg.Text('Input file'), sg.Input(), sg.FileBrowse()],
    [sg.Text('Output format'), sg.Combo(['CSV', 'JSON'], size=(10, 1))],
    [sg.Text('Output file'), sg.Input(), sg.FileSaveAs()],
    [sg.Button('Convert'), sg.Exit()]
]

window = sg.Window('Converter', layout)

def json_to_csv(json_data, output_file):
    # Create a CSV file
    with open(output_file, 'w', newline='') as csv_file:
        # Create a CSV writer
        writer = csv.DictWriter(csv_file, fieldnames=json_data[0].keys())
        # Write the header row
        writer.writeheader()
        # Write the data rows
        for row in json_data:
            writer.writerow(row)

# Main loop of the application
while True:
    event, values = window.read()
    # Event handler for closing the window
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    # Event handler for the Convert button
    if event == 'Convert':
        # Get the input and output files
        input_file = values[0]
        output_format = values[1]
        output_file = values[2]
        # Open the input file
        with open(input_file, 'r') as in_file:
            # Convert JSON to CSV
            if output_format == 'CSV':
                data = json.load(in_file)
                json_to_csv(data, output_file)
            # Convert CSV to JSON
            else:
                data = csv.DictReader(in_file)
                with open(output_file, 'w') as out_file:
                    json.dump(list(data), out_file, indent=4)
        # Show a popup window to confirm the conversion
        sg.popup('Conversion complete!')
        # Close the window
        window.close()
