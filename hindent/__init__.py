"""
Contains the class ``Hindent``. Import and use that class.

>>> from hindent import Hindent
"""

from pathlib import Path
import os
import subprocess


_SAVED_FILE_SCM = "SAVED_FILE.scm"

class LispExecutor:
    """
    Function that takes a filename and executes the lisp code on it.

    The default will use Chez Scheme.

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


def _execute_scheme_code(filename):
    # For Chez Scheme, the command is typically 'scheme --script'
    process = subprocess.run(['chez', '--script', filename], capture_output=True, text=True)
    return process.stdout, process.stderr

class Hindent:
    """
    Has two methods: ``initialize`` and ``run``.

    >>> # from hindent import Hindent
    >>> # Hindent.initialize()
    >>> # Hindent.run()

    Other usage
    -----------

    You can also use ``Hindent.run_file`` and ``Hindent.run_string``.
    ``Hindent.run_file`` takes a ``Path`` object, which lets you specify the
    file to run instead of only using the default file. ``Hindent.run_string``
    takes a string, which lets you run code on the fly instead of having to
    write it to a file first.
    """

    @classmethod
    def initialize(
        cls,
        file_path: Path = Path('./first.hin'),
        lisp_executor: LispExecutor = _execute_scheme_code
    ):
        """
        >>> # import Hindent
        >>> from pathlib import Path
        >>> Hindent.initialize(
        ...     Path('./example_hindent_code.hin'), 
        ... )
        >>> # then do Hindent.run()


        Using Something Other Than Chez Scheme
        --------------------------------------

        If you want to use something other than Chez Scheme, you can do so by
        passing a different function to ``Hindent.initialize``. This function
        should take a filename as a parameter and return a tuple of the output
        and error of the execution.
        """

        cls._file_path = file_path
        cls._lisp_executor = lisp_executor

    @classmethod
    def run(cls) -> tuple:
        """
        >>> # import and initialize Hindent
        >>> output, error = Hindent.run()
        >>> print(output)
        some output
        """
        return Hindent._interpret(
            Hindent._get_text_from_file_path(cls._file_path),
            cls._lisp_executor
        )
    
    @classmethod
    def run_file(cls, file_path: Path) -> tuple:
        """
        >>> # import and initialize Hindent
        >>> file_path = Path('./example_hindent_code.hin')
        >>> output, error = Hindent.run_file(file_path)
        >>> print(output)
        some output
        """
        return Hindent._interpret(
            Hindent._get_text_from_file_path(file_path),
            cls._lisp_executor
        )

    @classmethod
    def run_string(cls, string: str) -> tuple:
        """
        >>> # import and initialize Hindent
        >>> input_string = (
        ...     "display\\n"
        ...     "  2\\n"
        ...     ""
        ... )
        >>> output, error = Hindent.run_string(input_string)
        >>> print(output)
        some output
        """
        return Hindent._interpret(
            string,
            cls._lisp_executor
        )

    @staticmethod
    def _process_code_v3(code):
        # Split the code into lines
        lines = code.split("\n")

        # Function to calculate the indentation level of a line
        def indentation_level(line):
            return (len(line) - len(line.lstrip())) // 2

        # Process each line
        processed_lines = []
        for i in range(len(lines)):
            # Handle blank lines or lines with only whitespace (except the last line)
            if lines[i].strip() == '' and i != len(lines) - 1:
                # Avoid adding multiple consecutive blank lines
                if processed_lines and processed_lines[-1] == '':
                    continue
                else:
                    processed_lines.append('')
                    continue

            # Skip processing for the very last line (it should remain blank)
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

    @staticmethod
    def _save_code_to_file(code, filename):
        with open(filename, 'w') as file:
            file.write(code)

    @staticmethod
    def _interpret(input_code: str, lisp_executor: LispExecutor) -> tuple:

        # Add parentheses with the fixed function and return the result
        parenthesized_code_fixed = Hindent._process_code_v3(input_code)

        # print(parenthesized_code_fixed)

        # Example usage
        Hindent._save_code_to_file(parenthesized_code_fixed, _SAVED_FILE_SCM)
        output, error = lisp_executor(_SAVED_FILE_SCM)

        # delete file
        os.remove(_SAVED_FILE_SCM)

        return output, error

    @staticmethod
    def _get_text_from_file_path(file_path: Path) -> str:
        file_path = Path(file_path)

        input_code = file_path.read_text()
        return input_code


