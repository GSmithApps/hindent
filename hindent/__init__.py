"""
Contains the class `Hindent`. Import and use this class to format and execute Scheme code.

Usage:
    >>> from hindent import Hindent
    >>> Hindent.initialize(
    ...     # args here
    ... )
    >>> output, error = Hindent.run()
    >>> print(output)
"""

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


def _execute_scheme_code(filename):
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
    >>> stdout, stderr = _execute_scheme_code("example.scm")
    >>> print(stdout)
    """

    # For Chez Scheme, the command is typically 'scheme --script'
    process = subprocess.run(['chez', '--script', filename], capture_output=True, text=True)
    return process.stdout, process.stderr


class Hindent:
    """
    A class for handling Hindent syntax for Lisp code. Provides methods to initialize the
    environment, run Lisp code from a file or a string, and to transpile Hindent syntax to Lisp.

    Use `Hindent.initialize` to configure the environment, and then use `Hindent.run`,
    `Hindent.run_file`, or `Hindent.run_string` to execute Hindent code.

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
        Initializes the Hindent environment with a specified file and Lisp executor.

        Parameters
        ----------

        file_path : Path
            The file path of the Hindent code to be formatted and executed.
        lisp_executor : LispExecutor
            The executor function to run the Lisp code. Defaults to `_execute_scheme_code` using Chez Scheme.

        Examples
        --------

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
        Executes and retrieves the output of Lisp code from the initialized file.

        Returns
        -------
        tuple
            A tuple containing the standard output and standard error from the executed Lisp code.

        Examples
        --------

        >>> # import and initialize Hindent
        >>> output, error = Hindent.run()
        >>> print(output)
        some output
        """
        return Hindent._interpret(
            Hindent._get_text_from_file_path(cls._file_path),
        )
    
    @classmethod
    def run_file(cls, file_path: Path) -> tuple:
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

        >>> # import and initialize Hindent
        >>> file_path = Path('./example_hindent_code.hin')
        >>> output, error = Hindent.run_file(file_path)
        >>> print(output)
        some output
        """
        return Hindent._interpret(
            Hindent._get_text_from_file_path(file_path),
        )

    @classmethod
    def run_string(cls, string: str) -> tuple:
        """
        Executes and retrieves the output of Lisp code from a given string.

        This method allows the user to run Lisp code directly from a string,
        enabling on-the-fly execution without needing to write to a file.

        Parameters
        ----------
        string : str
            The string containing the Hindent code to be formatted and executed.

        Returns
        -------
        tuple
            A tuple containing the standard output and standard error from the executed Lisp code.

        Examples
        --------

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
        )

    @staticmethod
    def transpile(code):
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
        >>> hindent_code = "define x 10\\n  display x"
        >>> scheme_code = Hindent.transpile(hindent_code)
        >>> print(scheme_code)
        """

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
    def _interpret(input_code: str) -> tuple:
        """
        Interprets the given Hindent code, transpiling it to Scheme and executing it.

        This internal method first transpiles the provided Hindent code to Scheme,
        then executes the Scheme code and returns the output and error.

        Parameters
        ----------
        input_code : str
            The Hindent code to be interpreted.

        Returns
        -------
        tuple
            A tuple containing the standard output and standard error from the executed Scheme code.

        Examples
        --------
        >>> hindent_code = "define x 10\\n  display x"
        >>> output, error = Hindent._interpret(hindent_code)
        >>> print(output)
        """

        # Add parentheses with the fixed function and return the result
        parenthesized_code_fixed = Hindent.transpile(input_code)

        # Example usage
        output, error = Hindent.run_lisp(parenthesized_code_fixed)

        return output, error

    @classmethod
    def run_lisp(cls, parenthesized_code_fixed):
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

        Hindent._save_code_to_file(parenthesized_code_fixed, _SAVED_FILE_SCM)
        output, error = cls._lisp_executor(_SAVED_FILE_SCM)

        # delete file
        os.remove(_SAVED_FILE_SCM)
        return output,error

    @staticmethod
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
        >>> file_path = Path('./example.hin')
        >>> content = Hindent._get_text_from_file_path(file_path)
        >>> print(content)
        """
        file_path = Path(file_path)

        input_code = file_path.read_text()
        return input_code


