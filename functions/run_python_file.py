import os
import subprocess
import sys

"""
THIS CODE IS UNTRUSTED. It is my opinion that you should NEVER permit an LLM to run arbitrary code on your system.
This holds ESPECIALLY true if the LLM wrote the code that it will be executing.
This project does not contain the same guardrails that production LLM agents have to prevent abuse or 
accidental damages to your system.
This module will be disabled by default on the Git repo. Enable at your own peril.
"""

def run_python_file(working_directory, file_path, args=[]):
    filepath = os.path.join(working_directory, file_path)

    # Normalize to account for cross-platform compatibility
    abs_working_dir = os.path.normcase(os.path.abspath(working_directory))
    abs_filepath = os.path.normcase(os.path.abspath(filepath))

    # Check for external path
    common_path = os.path.commonpath([abs_working_dir, abs_filepath])

    if common_path != abs_working_dir:
        return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
    
    final_abs_path = os.path.abspath(filepath)
    if not os.path.isfile(final_abs_path):
        return f"Error: File \"{file_path}\" not found."

    if not file_path.endswith(".py"):
        return f"Error: \"{file_path}\" is not a Python file."

    python_executable = sys.executable
    command = [python_executable, final_abs_path] + args

    try:
        result = subprocess.run(command, timeout=30, capture_output=True, text=True, cwd=abs_working_dir)
        output_lines = []
        stdout_str = result.stdout.strip()
        stderr_str = result.stderr.strip()
        if result.returncode != 0:
            output_lines.append(f"Process exited with code {result.returncode}")
        if not stdout_str and not stderr_str:
            output_lines.append("No output produced.")
        output_lines.append(f"STDOUT: {stdout_str}")
        output_lines.append(f"STDERR: {stderr_str}")
        return "\n".join(output_lines)
    except subprocess.TimeoutExpired:
        return "Process exited with code -1\nSTDOUT:\nSTDERR:Execution timed out after 30 seconds."
    except Exception as e:
        return f"Error: e"