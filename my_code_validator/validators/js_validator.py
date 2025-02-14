import os
from .utils import run_command, format_output

class JSValidator:
    def __init__(self, directory):
        """Initialize the JSValidator with the directory."""
        self.directory = directory  
        self.run_command = run_command
        self.format_output = format_output

    def check_eslint(self, file_path):
        """Check JavaScript code quality with globally installed ESLint."""
        result = self.run_command(f"npx eslint \"{file_path}\"")
        return self.format_output("ESLint Code Quality", result) if result else None

    def check_prettier(self, file_path):
        """Check JavaScript code formatting with Prettier."""
        result = self.run_command(f"npx prettier --check {file_path}")
        return self.format_output("Prettier Formatting", result) if result else None

    def check_retire(self, file_path):
        """Check for security vulnerabilities using Retire.js (only for JS files)."""
        result = self.run_command(f"npx retire --js {file_path}")
        return self.format_output("Retire.js Security Check", result) if result else None
    
    def validate_code(self, file_path):
        """Run validation checks only for the specified JavaScript file."""
        print("\n🔍 Running JavaScript Code Validation...\n")
        print(f"Validating: {file_path}\n{'-'*50}")

        eslint_result = self.check_eslint(file_path)
        prettier_result = self.check_prettier(file_path)
        retire_result = self.check_retire(file_path)

        checks = [eslint_result, prettier_result, retire_result]

        # Print only non-None results
        for result in checks:
            if result is not None:
                print(result)

        print("\n✅ JavaScript validation complete!\n")
