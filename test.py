from pathlib import Path
import re

test = Path('./first.hin')

def process_code_v2(code):
    # Split the code into lines
    lines = code.split("\n")

    # Function to calculate the indentation level of a line
    def indentation_level(line):
        return (len(line) - len(line.lstrip())) // 2

    # Process each line
    processed_lines = []
    for i in range(len(lines)):
        # Skip processing for the last line (it should remain blank)
        if i == len(lines) - 1:
            processed_lines.append('')
            continue

        # Calculate the current and next line's indentation levels
        current_indent = indentation_level(lines[i])
        next_indent = indentation_level(lines[i + 1]) if i + 1 < len(lines) - 1 else 0

        # Determine the required parentheses
        line = lines[i].lstrip()  # Remove leading spaces
        if next_indent > current_indent:
            line = "(" + line
        elif next_indent < current_indent:
            line += ")" * (current_indent - next_indent)

        # Special case: same indentation level
        if next_indent == current_indent and current_indent == 0 and i != 0:
            line = "(" + line + ")"

        processed_lines.append(line)

    # Join the processed lines
    return "\n".join(processed_lines)


input_code = test.read_text()

# Add parentheses with the fixed function and return the result
parenthesized_code_fixed = process_code_v2(input_code)

# print(parenthesized_code_fixed)

import subprocess

def save_code_to_file(code, filename):
    with open(filename, 'w') as file:
        file.write(code)

def execute_scheme_code(filename):
    # For Chez Scheme, the command is typically 'scheme --script'
    process = subprocess.run(['chez', '--script', filename], capture_output=True, text=True)
    return process.stdout, process.stderr

# Example usage
save_code_to_file(parenthesized_code_fixed, 'example.scm')
output, error = execute_scheme_code('example.scm')


print(output)

# output, error

