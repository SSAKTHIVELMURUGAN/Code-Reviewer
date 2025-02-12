import subprocess

def run_command(command):
    """Runs a shell command using Popen and returns the output and errors."""
    try:
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = proc.communicate()
        return stdout.strip() + "\n" + stderr.strip()
    except Exception as e:
        return str(e)

def format_output(title, result):
    """Formats the output for better readability."""
    border = "=" * 60
    return f"""
{border}
📌 {title}
{border}

{result}
"""
