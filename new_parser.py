def parse_newlang_to_python(input_code: str) -> str:
    lines = input_code.strip().split('\n')
    output_lines = []

    for i, line in enumerate(lines):
        # Count the number of leading spaces (our indentation is two spaces per level)
        indent = len(line) - len(line.lstrip(' '))
        num_indents = indent // 2

        # Replace '} ' with 'co( '
        current_line = line.replace('} ', 'co(')

        # Determine the number of indents in the next line to decide on closing parentheses
        if i < len(lines) - 1:
            next_line_indent = len(lines[i + 1]) - len(lines[i + 1].lstrip(' '))
            next_num_indents = next_line_indent // 2
        else:
            # If this is the last line, ensure we close all open parentheses
            next_num_indents = 0

        # Calculate how many parentheses to close based on the indent difference
        closing_parens = ')' * (num_indents - next_num_indents)
        # Append the modified line with closing parentheses and a comma if not the last line
        output_lines.append(current_line + closing_parens + (',' if i < len(lines) - 1 else ''))

    return '\n'.join(output_lines)

