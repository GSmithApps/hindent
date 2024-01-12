"""
Provides functions to translate Hindent code.

>>> import hindent as h
>>> hindent_code = '''
... println
...   + 2 2
... '''
>>> h.translate(hindent_code)
(
println (
  + 2 2 ) )

or

>>> import hindent as h
>>> h.translate_file('./your-file.hin')
(
println (
  + 2 2 ) )
"""

__version__ = "4.0.0"

from pathlib import Path


def translate(hindent_code: str) -> str:
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
    >>> hindent_code = '''
    ... println
    ...   + 2 2
    ... '''
    >>> lisp_code = h.translate(hindent_code)
    >>> print(lisp_code)
    """

    # Split the code into lines
    lines = hindent_code.split("\n")

    # add a newline to the beginning of the list to ensure the first line is processed correctly
    lines.insert(0, "")

    lines.append(
        ""
    )  # Add a newline to the end to ensure the final outdent is correct

    non_comment_line_numbers = []

    # remove comment blocks and whole line comments.
    for i, line in enumerate(lines):

        # We want to remove the comments, so we don't want to add them to the
        # list of valid lines, so we simply skip them with a continue statement/guard clause
        if line.strip().find(";") == 0:
            continue

        non_comment_line_numbers.append(i)

    # Function to calculate the indentation level of a line
    def indentation_level(line):
        """
        The indentation should be the number of spaces at the beginning of the line
        divided by two.
        """

        if line.strip() == "":
            return 0
        else:
            return (len(line) - len(line.lstrip())) // 2
        
    
    for i in range(len(non_comment_line_numbers)-1):
        line = lines[non_comment_line_numbers[i]]
        next_line = lines[non_comment_line_numbers[i + 1]]

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
        hasdot = False
        if line.strip() == ".":
            line = ""
        elif line.lstrip().find(". ") == 0:
            line = " " + line.lstrip()[1:]

        if next_indent > current_indent:

            # add an opening parenthesis at the location at with the current
            # indent starts

            line = line[: current_indent * 2] + ("(" * (next_indent - current_indent)) + line[current_indent * 2 :]

        elif next_indent < current_indent:
            line = line.rstrip() + (")" * (current_indent - next_indent))

        lines[non_comment_line_numbers[i]] = line

    # remove the newline we added to the beginning of the list
    # lines.pop(0)
    # we can't do this because sometimes the user writes on
    # the first line.

    # remove the newline we added to the end of the list
    lines.pop()

    # Join the processed lines
    return "\n".join(lines)

