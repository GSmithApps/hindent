"""
Provides functions to transpile and/or execute Hindent code.

>>> import hindent as h
>>> h.run_file('./your-file.hin')

or

>>> import hindent as h
>>> hindent_code = '''
... display
...   2
... '''
>>> h.run_string(hindent_code)

Provided functions
------------------

run_file(file_path: Path)
    Executes and retrieves the output of Lisp code from a specified file.

run_string(hindent_code: str)
    Executes and retrieves the output of Lisp code from a given string.

transpile_file(file_path: Path)
    Transpiles Hindent code from a specified file to Scheme code.

transpile_string(hindent_code: str)
    Transpiles Hindent code to Scheme code by adding appropriate parentheses based on indentation.

execute_lisp(lisp_code: str)
    Executes the given Scheme code.
"""

__version__ = "2.0.1"

from pathlib import Path
import os
import subprocess


_SAVED_FILE_SCM = "SAVED_FILE.scm"


# This class is just for type hinting for a function/callback
class LispExecutor:
    """
    A callback function type that executes Lisp (Scheme) code from a given filename.

    This is intended to be used as a function type for custom executors, with a default
    implementation using Chez Scheme.

    The function should take a filename as input, execute the Lisp code in the file, and
    return the output and error of the execution as a tuple.

    Parameters
    ----------
    filename : str
        The name of the file to execute.

    Returns
    -------

    tuple
        The output and error of the execution.

    Examples
    --------

    >>> def execute_scheme_code(filename):
    ...     # For Chez Scheme, the command is typically 'scheme --script'
    ...     process = subprocess.run(['chez', '--script', filename], capture_output=True, text=True)
    ...     return process.stdout, process.stderr
    """


def _default_lisp_executor(filename):
    """
    Default executor function for executing Scheme code using Chez Scheme.

    This function executes Scheme code from a specified file using Chez Scheme, capturing
    and returning the standard output and standard error.

    Parameters
    ----------
    filename : str
        The path to the Scheme file to be executed.

    Returns
    -------
    tuple
        A tuple containing two elements: the standard output and standard error from the executed Scheme code.

    Examples
    --------
    >>> stdout, stderr = _default_lisp_executor("example.scm")
    >>> print(stdout)
    """

    # For Chez Scheme, the command is typically 'scheme --script'
    process = subprocess.run(
        ["chez", "--script", filename], capture_output=True, text=True
    )
    return process.stdout, process.stderr


lisp_executor: LispExecutor = _default_lisp_executor


def run_file(file_path: Path) -> tuple:
    """
    Executes and retrieves the output of Lisp code from a specified file.

    This method allows the user to run Lisp code from a file of their choice,
    rather than the default file set during initialization.

    Parameters
    ----------
    file_path : Path
        The path to the file containing the Hindent code to be formatted and executed.

    Returns
    -------
    tuple
        A tuple containing the standard output and standard error from the executed Lisp code.

    >>> import hindent as h
    >>> h.run_file('./example_hindent_code.hin')
    some output
    """
    return run_string(
        _get_text_from_file_path(file_path),
    )


def run_string(hindent_code: str) -> tuple:
    """
    Executes and retrieves the output of Lisp code from a given string.

    This method allows the user to run Lisp code directly from a string,
    enabling on-the-fly execution without needing to write to a file.

    Parameters
    ----------
    hindent_code : str
        The string containing the Hindent code to be formatted and executed.

    Returns
    -------
    tuple
        A tuple containing the standard output and standard error from the executed Lisp code.

    Examples
    --------

    >>> import hindent as h
    >>> hindent_code = '''
    ... display
    ...   2
    ... '''
    >>> h.run_string(hindent_code)
    some output
    """

    # Add parentheses with the fixed function and return the result
    parenthesized_code_fixed = transpile_string(hindent_code)

    # Example usage
    output, error = execute_lisp(parenthesized_code_fixed)

    return output, error



def transpile_file(file_path: Path) -> str:
    """
    Transpiles Hindent code from a specified file to Scheme code.

    This method reads the Hindent code from the given file, transpiles it to Scheme code
    by adding appropriate parentheses based on indentation, and returns the transpiled
    Scheme code.

    Parameters
    ----------
    file_path : Path
        The path to the file containing the Hindent code to be transpiled.

    Returns
    -------
    str
        The transpiled Scheme code.

    Examples
    --------
    >>> scheme_code = h.transpile_file('./example.hin')
    >>> print(scheme_code)
    """
    return transpile_string(
        _get_text_from_file_path(file_path),
    )


def transpile_string(hindent_code: str) -> str:
    """
    Transpiles Hindent code to Scheme code by adding appropriate parentheses based on indentation.

    This method processes Hindent code, which uses indentation to denote structure,
    and converts it to valid Scheme code by adding parentheses according to the
    indentation levels.

    Parameters
    ----------
    code : str
        The Hindent code to be transpiled.

    Returns
    -------
    str
        The transpiled Scheme code.

    Examples
    --------
    >>> hindent_code = (
    ...     "display\\n"
    ...     "  2\\n"
    ...     ""
    ... )
    >>> scheme_code = h.transpile(hindent_code)
    >>> print(scheme_code)
    """

    # Split the code into lines
    lines = hindent_code.split("\n")

    validlines = []

    in_code_block = True

    for i, line in enumerate(lines):

        # Handle code blocks
        if line.rstrip() == ".":
            in_code_block = not in_code_block
            continue

        if not in_code_block:
            continue

        # Handle blank lines or lines with only whitespace (except the last line)
        # guard clause to exit early if the line is whitespace or a comment
        if line.strip() == "" or line.strip()[0] == ";":
            continue

        validlines.append(line)

    validlines.append("\n")  # Add a newline to the end

    # Function to calculate the indentation level of a line
    def indentation_level(line):
        return (len(line) - len(line.lstrip())) // 2

    # Process each line
    processed_lines = []

    for i, line in enumerate(validlines[:-1]):

        # Remove any end-of-line comments
        line = _remove_potential_end_of_line_comment(line)

        # Calculate the current and next line's indentation levels
        current_indent = indentation_level(line)
        next_indent = indentation_level(validlines[i + 1])

        # Determine the required parentheses
        if next_indent > current_indent:
            line = "(" + line
        elif next_indent < current_indent:
            line += ")" * (current_indent - next_indent)

        # Special case: same indentation level
        if next_indent == 0 and current_indent == 0:
            line = "(" + line + ")"

        processed_lines.append(line)

    # Join the processed lines
    return "\n".join(processed_lines)


def _save_code_to_file(code, filename):
    with open(filename, "w") as file:
        file.write(code)


def execute_lisp(lisp_code: str) -> tuple:
    """
    Executes the given Scheme code after saving it to a temporary file.

    This method is used internally to execute Scheme code. It saves the provided
    Scheme code to a temporary file, executes the file using the configured Lisp executor,
    and then deletes the file.

    Parameters
    ----------
    parenthesized_code_fixed : str
        The Scheme code to be executed.

    Returns
    -------
    tuple
        A tuple containing the standard output and standard error from the executed Scheme code.
    """

    _save_code_to_file(lisp_code, _SAVED_FILE_SCM)
    output, error = lisp_executor(_SAVED_FILE_SCM)

    print(output)
    print(error)

    # delete file
    os.remove(_SAVED_FILE_SCM)
    return output, error


def _get_text_from_file_path(file_path: Path) -> str:
    """
    Reads text from a file specified by the given file path.

    This utility method reads and returns the contents of the file at the specified path.

    Parameters
    ----------
    file_path : Path
        The path of the file to be read.

    Returns
    -------
    str
        The content of the file as a string.

    Examples
    --------
    >>> content = h._get_text_from_file_path('./example.hin')
    >>> print(content)
    """
    file_path = Path(file_path)

    input_code = file_path.read_text()
    return input_code


def _remove_potential_end_of_line_comment(line: str) -> str:
    """
    Removes any end-of-line comments from a line of code.

    This method removes any end-of-line comments from a line of code, returning the
    line without the comment.

    We need to make sure that we don't remove comments from within strings.

    Parameters
    ----------
    line : str
        The line of code to be processed.

    Returns
    -------
    str
        The line of code without any end-of-line comments.

    Examples
    --------
    >>> line = "display 2 ; this is a comment"
    >>> line_without_comment = h.remove_potential_end_of_line_comment(line)
    >>> print(line_without_comment)
    display 2
    """

    in_string = False

    for i, char in enumerate(line):
        if char == '"':
            in_string = not in_string

        if char == ";" and not in_string:
            return line[:i]
    
    return line

            