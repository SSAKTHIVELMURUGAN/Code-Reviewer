import os
import sys
from my_code_validator.validators.python_validator import PythonValidator
from my_code_validator.validators.js_validator import JSValidator

IGNORE_FILES = {"node_modules", ".git", ".venv", ".vscode", "__pycache__"}
VENV_INDICATORS = {"bin", "Scripts", "pyvenv.cfg"}  # Common venv structure

def is_virtual_env(path):
    """Check if the given path belongs to a virtual environment folder."""
    abs_path = os.path.abspath(path)  # Convert to absolute path
    folder_name = os.path.basename(abs_path)  # Get the folder name

    # Check if the folder name is commonly used for virtual environments
    if folder_name in {"venv", ".venv", "env", "myenv"}:
        return True

    # Check if it contains virtual environment indicators
    return any(os.path.exists(os.path.join(abs_path, indicator)) for indicator in VENV_INDICATORS)

def is_ignored(path):
    """Check if the given path is inside any ignored directory."""
    abs_path = os.path.abspath(path)  # Convert to absolute path
    path_parts = abs_path.split(os.sep)  # Split path into components

    # Ignore node_modules, .git, etc.
    if any(ignored in path_parts for ignored in IGNORE_FILES):
        return True

    # Ignore virtual environments
    if any(is_virtual_env(os.path.join(*path_parts[:i])) for i in range(1, len(path_parts) + 1)):
        return True

    return False

def get_files_by_extension(directory):
    """Recursively finds all .py and .js files in a given directory."""
    python_files = []
    js_files = []
    
    for root, _, files in os.walk(directory):
        if is_ignored(root): 
            continue

        for file in files:
            file_path = os.path.join(root, file)
            if is_ignored(file_path):  
                continue
            
            if file.endswith((".py", ".js")):  
                (python_files if file.endswith(".py") else js_files).append(file_path)
                
    return python_files, js_files

def validate_project(directory):
    """Validate all Python and JS files in the given project directory."""
    if not os.path.isdir(directory):
        print(f"❌ Error: {directory} is not a valid directory.")
        sys.exit(1)

    python_files, js_files = get_files_by_extension(directory)

    if not python_files:
        print("✅ No Python files found for validation.")
    if not js_files:
        print("✅ No JavaScript files found for validation.")

    python_validator = PythonValidator(directory)
    for file in python_files:
        python_validator.validate_code(file)

    js_validator = JSValidator(directory)
    for file in js_files:
        js_validator.validate_code(file)
