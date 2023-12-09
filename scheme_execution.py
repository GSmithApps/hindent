import subprocess

def execute_scheme_code(filename):
    # For Chez Scheme, the command is typically 'scheme --script'
    process = subprocess.run(['chez', '--script', filename], capture_output=True, text=True)
    return process.stdout, process.stderr
