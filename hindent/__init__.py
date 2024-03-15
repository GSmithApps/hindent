from functools import partial
import inspect


# Function to calculate remaining arguments, now handles both partials and regular functions
def _remaining_args(func_or_partial):
    # Check if the input is a partial object
    if isinstance(func_or_partial, partial):
        # If so, retrieve the original function and count the supplied arguments
        original_func = func_or_partial.func
        supplied_args_count = len(func_or_partial.args) + len(func_or_partial.keywords)
    else:
        # If it's not a partial, it's a regular function, so consider no arguments supplied
        original_func = func_or_partial
        supplied_args_count = 0

    # Inspect the original function signature
    sig = inspect.signature(original_func)
    total_params = len(sig.parameters)

    # Calculate remaining arguments required
    remaining = total_params - supplied_args_count
    return remaining


def co(*fs):

    if len(fs) == 0:
        raise Exception("No functions to compose")

    if len(fs) == 1:
        return fs[0]

    for i, f in enumerate(fs):

        if i == 0:
            current = f

        if _remaining_args(current) == 1:

            return current(fs[i + 1])
        else:
            current = partial(current, fs[i + 1])

    # this happens if the function accepts more arguments than
    # the number of functions to compose
    return current


def translate_hindent(input_code: str) -> str:
    lines = input_code.strip().split("\n")
    output_lines = []

    for i, line in enumerate(lines):
        # Count the number of leading spaces (our indentation is two spaces per level)
        indent = len(line) - len(line.lstrip(" "))
        num_indents = indent // 2

        # Replace '} ' with 'co( '
        current_line = line.replace("} ", "co(")

        # Determine the number of indents in the next line to decide on closing parentheses
        if i < len(lines) - 1:
            next_line_indent = len(lines[i + 1]) - len(lines[i + 1].lstrip(" "))
            next_num_indents = next_line_indent // 2
        else:
            # If this is the last line, ensure we close all open parentheses
            next_num_indents = 0

        # Calculate how many parentheses to close based on the indent difference
        closing_parens = ")" * (num_indents - next_num_indents)
        # Append the modified line with closing parentheses and a comma if not the last line
        output_lines.append(
            current_line + closing_parens + ("," if i < len(lines) - 1 else "")
        )

    return "\n".join(output_lines)
