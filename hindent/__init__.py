"""
Provides functions to translate and/or execute Hindent code.

>>> import hindent as h
>>> h.translate_file('./your-file.hin')
(
println (
  + 2 2 ) )

or

>>> import hindent as h
>>> hindent_code = '''
... println
...   + 2 2
... '''
>>> h.translate_string(hindent_code)
(
println (
  + 2 2 ) )

Provided functions
------------------

translate_file(file_path: Path)
    Translates Hindent code from a specified file.

translate_string(hindent_code: str)
    Translates Hindent code by adding appropriate parentheses based on indentation.

get_text_from_file_path(file_path: Path)
    Reads text from a file specified by the given file path.

Additional Modules
------------------

lisp_execution
    Provides functions to execute Lisp code.

"""

__version__ = "4.0.0"

from pathlib import Path


def translate_file(file_path: Path) -> str:
    """
    Translates Hindent code from a specified file.

    This method reads the Hindent code from the given file, translates it
    by adding parentheses based on indentation, and returns the translated
    code.

    Parameters
    ----------
    file_path : Path
        The path to the file containing the Hindent code to be translated.

    Returns
    -------
    str
        The translated code.

    Examples
    --------
    >>> lisp_code = h.translate_file('./examples/example.hin')
    >>> print(lisp_code)
    """
    return translate_string(
        get_text_from_file_path(file_path),
    )


def translate_string(hindent_code: str) -> str:
    """
    Translates Hindent code to lisp code by adding appropriate parentheses based on indentation.

    This method processes Hindent code, which uses indentation to denote structure,
    and converts it to valid lisp code by adding parentheses according to the
    indentation levels.

    Parameters
    ----------
    code : str
        The Hindent code to be translated.

    Returns
    -------
    str
        The translated lisp code.

    Examples
    --------
    >>> hindent_code = (
    ...     "println\\n"
    ...     "  + 2 2\\n"
    ...     ""
    ... )
    >>> lisp_code = h.translate_string(hindent_code)
    >>> print(lisp_code)
    """

    # Split the code into lines
    lines = hindent_code.split("\n")

    validlines = []

    in_code_block = True

    # remove comment blocks and whole line comments.
    for i, line in enumerate(lines):
        # Handle code/comment blocks
        if line.rstrip() == ",":
            in_code_block = not in_code_block
            continue

        if not in_code_block:
            continue

        # We want to remove the comments, so we don't want to add them to the
        # list of valid lines, so we simply skip them with a continue statement/guard clause
        if line.strip().find(";") == 0:
            continue

        validlines.append(line)

    validlines.append(
        "\n"
    )  # Add a newline to the end to ensure the final outdent is correct

    # Function to calculate the indentation level of a line
    def indentation_level(line):
        return (len(line) - len(line.lstrip())) // 2

    # Process each line
    processed_lines = []

    for i, line in enumerate(validlines[:-1]):
        next_line = validlines[i + 1]

        # Remove any end-of-line comments
        line = _remove_potential_end_of_line_comment(line)

        # Calculate the current and next line's indentation levels
        current_indent = indentation_level(line)
        next_indent = indentation_level(next_line)

        # if a line starts with `. ` (or, in the case that a period is
        # the only thing on the line... some examples of use cases are in
        # the examples) then remove the period
        # after the indentation is calculated. This lets the user
        # use the period to modify the indentation level of a line.
        # an example is given in `examples/example.hin`.  This is also
        # used to evaluate functions that have no arguments.
        if line.strip() == "." or line.lstrip().find(". ") == 0:
            line = " " + line.lstrip()[1:]

        # Determine the required parentheses
        if (
            # current line is totally blank with no indentation or period
            (current_indent == 0 and line.strip() == "")
            and
            # the next line is anything but blank
            not (next_indent == 0 and next_line.strip() == "")
        ):
            line = "("

        if (
            # current line is anything but blank
            not (current_indent == 0 and line.strip() == "")
            and
            # next line is blank
            (next_indent == 0 and next_line.strip() == "")
        ):
            line = line.rstrip() + " )"

        if next_indent > current_indent:
            line = line.rstrip() + " " + ("(" * (next_indent - current_indent))
        elif next_indent < current_indent:
            line = line.rstrip() + " " + (")" * (current_indent - next_indent))

        processed_lines.append(line)

    # Join the processed lines
    return "\n".join(processed_lines)


def get_text_from_file_path(file_path: Path) -> str:
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
    >>> content = h._get_text_from_file_path('./examples/example.hin')
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
    >>> line = "println 2 ; this is a comment"
    >>> line_without_comment = h.remove_potential_end_of_line_comment(line)
    >>> print(line_without_comment)
    println 2
    """

    in_string = False

    for i, char in enumerate(line):
        if char == '"':
            in_string = not in_string

        if char == ";" and not in_string:
            return line[:i]

    return line
