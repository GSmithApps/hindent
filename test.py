from pathlib import Path
import re

test = Path('./first.hin')

def add_parentheses_to_code_multi(code):
    # Split the code into blocks separated by empty lines
    blocks = code.strip().split('\n\n')

    # Function to process a single block of code
    def process_block(block):
        lines = block.split('\n')
        indent_levels = [len(line) - len(line.lstrip()) for line in lines]
        indent_levels = [indent // 2 for indent in indent_levels]
        indent_diff = [indent_levels[i + 1] - indent_levels[i] for i in range(len(indent_levels) - 1)]

        result = []
        for i, line in enumerate(lines):
            if i < len(indent_diff) and indent_diff[i] > 0:
                result.append('(' * indent_diff[i] + line)
            else:
                result.append(line)

        # Add closing parentheses at the end
        if indent_diff:
            final_indent = indent_levels[-1]
            result[-1] += ')' * final_indent

        joined_text = '\n'.join(result)

        # joined_text = f"(display {joined_text})"

        return joined_text

    # Process each block and combine
    processed_blocks = [process_block(block) for block in blocks]
    return '\n\n'.join(processed_blocks)


input_code = test.read_text()

# Add parentheses with the fixed function and return the result
parenthesized_code_fixed = add_parentheses_to_code_multi(input_code)

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

