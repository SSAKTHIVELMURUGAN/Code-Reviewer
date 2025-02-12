import os
import sys
from my_code_validator.validators.python_validator import PythonValidator
from my_code_validator.validators.js_validator import JSValidator

def validate_files(file_paths):
    """Validate one or more Python or JS files."""
    if not file_paths:
        print("❌ Error: No files provided for validation.")
        sys.exit(1)

    for file_path in file_paths:
        if not os.path.isfile(file_path):
            print(f"❌ Error: {file_path} is not a valid file.")
            continue  # Skip invalid files instead of exiting

        if file_path.endswith(".py"):
            python_validator = PythonValidator(os.path.dirname(file_path))
            python_validator.validate_code(file_path)
        elif file_path.endswith(".js"):
            # FIX: Pass directory correctly
            js_validator = JSValidator(os.path.dirname(file_path))  # ✅ Fixed
            js_validator.validate_code(file_path)
        else:
            print(f"❌ Error: {file_path} - Only .py and .js files are supported.")
