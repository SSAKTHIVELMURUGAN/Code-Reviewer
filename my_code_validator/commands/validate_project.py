import os
import sys
from my_code_validator.validators.python_validator import PythonValidator
from my_code_validator.validators.js_validator import JSValidator

IGNORE_FILES = {"node_modules", ".git", ".venv", ".vscode", "__pycache__"}

def is_ignored(path):
    """Check if the given path is inside any ignored directory."""
    abs_path = os.path.abspath(path)  # Convert to absolute path
    return any(ignored in abs_path.split(os.sep) for ignored in IGNORE_FILES)

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
