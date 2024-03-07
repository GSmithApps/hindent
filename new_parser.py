def parse_newlang_to_python(input_code: str) -> str:
    lines = input_code.strip().split('\n')
    python_code = []
    stack = []  # Stack to keep track of (indentation level, 'co(' or ', co(')

    for line in lines:
        if not line.strip():  # Skip empty lines
            continue
        indent = len(line) - len(line.lstrip())
        # Determine the current line's content without leading spaces
        content = line.lstrip()

        # Handle function calls (lines starting with '}')
        if content.startswith('}'):
            func_name = content[1:].strip()
            while stack and indent <= stack[-1][0]:
                stack.pop()
                python_code.append(')')
            prefix = '' if not stack else ', '
            python_code.append(f"{prefix}co({func_name}")
            stack.append((indent, 'co('))
        else:
            # It's an argument to a function
            python_code.append(f", {content}")

    # Close any remaining open 'co' calls
    while stack:
        stack.pop()
        python_code.append(')')

    return ''.join(python_code)

# # Example usage
# input_code1 = """
# } my_func
#   2
#   2
# """

# input_code2 = """
# } newfunc
#   2
#   } otherfunc
#     3
#     4
# """

# print(parse_newlang_to_python(input_code1))
# print(parse_newlang_to_python(input_code2))
