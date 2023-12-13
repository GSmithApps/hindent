"""
Provides functions for executing Hindent (or other) code.

The Hindent interpreter executes
Hindent code by translating
it to lisp then executing it using
existing lisp interpreters/compilers.

Provided functions
------------------

run_file(file_path: Path)
    Executes and retrieves the output of Lisp code from a specified file.

run_string(hindent_code: str)
    Executes and retrieves the output of Lisp code from a given string.

execute_lisp(lisp_code: str)
    Executes the given lisp code.

Using a custom Lisp executor
----------------------------

The default Lisp executor uses clojure. However, you can
use a custom Lisp executor by setting the `lisp_executor` variable to a function
that takes a filename as input, executes the Lisp code in the file, and returns the
output and error of the execution as a tuple.
"""

import subprocess
import os
from pathlib import Path
from hindent import translate_string, get_text_from_file_path


_SAVED_FILE_TXT = "SAVED_FILE.txt"


# This class is just for type hinting for a function/callback
class LispExecutor:
    """
    A callback function type that executes Lisp code from a given filename.

    This is intended to be used as a function type for custom executors.

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

    >>> def _clojure_executor(filename):
    ...     process = subprocess.run(
    ...         ["clojure", filename], capture_output=True, text=True
    ...     )
    ...     return process.stdout, process.stderr
    """


def _scheme_executor(filename):
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


def _clojure_executor(filename):
    """
    Executor function for executing Clojure code using Clojure.

    This function executes Clojure code from a specified file using Clojure, capturing
    and returning the standard output and standard error.

    Parameters
    ----------
    filename : str
        The path to the Clojure file to be executed.

    Returns
    -------
    tuple
        A tuple containing two elements: the standard output and standard error from the executed Clojure code.

    Examples
    --------
    >>> stdout, stderr = _clojure_executor("example.clj")
    >>> print(stdout)
    """

    # For Clojure, the command is typically 'clojure'
    process = subprocess.run(
        ["clojure", "-M", filename], capture_output=True, text=True
    )
    return process.stdout, process.stderr


lisp_executor: LispExecutor = _clojure_executor


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
        get_text_from_file_path(file_path),
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
    ... println
    ...   + 2 2
    ... '''
    >>> h.run_string(hindent_code)
    some output
    """

    # Add parentheses with the fixed function and return the result
    parenthesized_code_fixed = translate_string(hindent_code)

    # Example usage
    output, error = execute_lisp(parenthesized_code_fixed)

    return output, error


def _save_code_to_file(code, filename):
    with open(filename, "w") as file:
        file.write(code)


def execute_lisp(lisp_code: str) -> tuple:
    """
    Executes the given lisp code.

    Parameters
    ----------
    parenthesized_code_fixed : str
        The lisp code to be executed.

    Returns
    -------
    tuple
        A tuple containing the standard output and standard error from the executed lisp code.
    """

    _save_code_to_file(lisp_code, _SAVED_FILE_TXT)
    output, error = lisp_executor(_SAVED_FILE_TXT)

    print(output)
    print(error)

    # delete file
    os.remove(_SAVED_FILE_TXT)
    return output, error
