import os
import sys
from my_code_validator.validators.python_validator import PythonValidator
from my_code_validator.validators.js_validator import JSValidator

def get_files_by_extension(directory):
    """Recursively finds all .py and .js files in a given directory."""
    python_files = []
    js_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
            elif file.endswith(".js"):
                js_files.append(os.path.join(root, file))
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
