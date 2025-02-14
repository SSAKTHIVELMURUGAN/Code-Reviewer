import os
import sys
from my_code_validator.validators.python_validator import PythonValidator
from my_code_validator.validators.js_validator import JSValidator
from .validate_project import is_ignored 

def validate_files(file_paths):
    """Validate one or more Python or JS files."""
    if not file_paths:
        print("❌ Error: No files provided for validation.")
        sys.exit(1)

    for file_path in file_paths:
        if not os.path.isfile(file_path):
            print(f"❌ Error: {file_path} is not a valid file.")
            continue  

        if is_ignored(file_path):
            print(f"⚠️ Skipping ignored file: {file_path}")
            continue

        file_dir = os.path.dirname(file_path)  

        if file_path.endswith(".py"):
            PythonValidator(file_dir).validate_code(file_path)
        elif file_path.endswith(".js"):
            JSValidator(file_dir).validate_code(file_path)
        else:
            print(f"❌ Error: {file_path} - Only .py and .js files are supported.")
