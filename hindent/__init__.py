from functools import partial
import inspect
import re

def replace_whole_word(text, word, replacement):
    # Escape the word_or_symbol to ensure special characters are treated literally
    pattern = r'\b' + re.escape(word) + r'\b'
    # Replace the word_or_symbol with the specified replacement
    replaced_text = re.sub(pattern, replacement, text)
    return replaced_text

from typing import Any, Callable, Union


def wrap_in_unit_function(x) -> Callable[[None], Any]:
    """
    Raise a value to be a function
    """

    def returnfunc(y):
        if y is None:
            return x
        else:
            raise NotImplementedError("This function's domain is None")

    return returnfunc


def our_id(f: Callable[[Any], None]) -> Callable[[Any], None]:
    """
    The identity function.

    This works on functions or on values.
    - If it's given a function, it returns the function.
    - If it's given a value, it returns that value.
    """

    return f


Numeric = Union[int, float, complex]


def p(
    f1_num: Callable[[None], Numeric], f2_num: Callable[[None], Numeric]
) -> Callable[[None], Numeric]:
    """
    Plus on the level of functions
    """

    return wrap_in_unit_function(f1_num(None) + f2_num(None))


def t(
    f1_num: Callable[[None], Numeric], f2_num: Callable[[None], Numeric]
) -> Callable[[None], Numeric]:
    """
    Plus on the level of functions
    """

    return wrap_in_unit_function(f1_num(None) * f2_num(None))


def pri(
    f: Callable[[None], Any]
) -> Callable[[Callable[[Any], None]], Callable[[Any], None]]:
    """
    print on the level of functions
    """
    print(f(None))
    return our_id


def concat(
    f1_string: Callable[[None], str], f2_string: Callable[[None], str]
) -> Callable[[None], str]:
    """
    Concatenation on the level of functions
    """

    return wrap_in_unit_function(f1_string(None) + f2_string(None))


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

    input_code = replace_whole_word(input_code, "print", "pri")
    input_code = input_code.replace('+', 'p')
    input_code = input_code.replace("*", "t")

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

def run_hindent(input_code: str, locals) -> None:
    exec(translate_hindent(input_code), globals(), locals)
