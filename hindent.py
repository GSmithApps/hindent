from pathlib import Path
import os
from scheme_execution import execute_scheme_code as _execute_scheme_code


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
    """

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

def _save_code_to_file(code, filename):
    with open(filename, 'w') as file:
        file.write(code)


def _interpret(file_path: Path, lisp_executor: LispExecutor) -> tuple:

    file_path = Path(file_path)

    input_code = file_path.read_text()

    # Add parentheses with the fixed function and return the result
    parenthesized_code_fixed = _process_code_v3(input_code)

    # print(parenthesized_code_fixed)

    # Example usage
    _save_code_to_file(parenthesized_code_fixed, _SAVED_FILE_SCM)
    output, error = lisp_executor(_SAVED_FILE_SCM)

    # delete file
    os.remove(_SAVED_FILE_SCM)

    return output, error

class Hindent:

    def __init__(
        self,
        file_path: Path = Path('./first.hin'),
        lisp_executor: LispExecutor = _execute_scheme_code
    ):
        self.file_path = file_path
        self.lisp_executor = lisp_executor

    def run(self) -> tuple:
        return _interpret(self.file_path, self.lisp_executor)
