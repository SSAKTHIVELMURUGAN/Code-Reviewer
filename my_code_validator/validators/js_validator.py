import os
from .utils import run_command, format_output

class JSValidator:
    def __init__(self, directory):
        """Initialize the JSValidator with the directory."""
        self.directory = directory  # Store the directory (useful for future expansion)
        self.run_command = run_command
        self.format_output = format_output

    def check_jshint(self, file_path):
        """Check JavaScript code with JSHint."""
        try:
            result = self.run_command(f"npx jshint {file_path}")
            return self.format_output("JSHint Check", result) if result else None
        except Exception as e:
            return f"❌ Error running JSHint: {e}"

    def check_prettier(self, file_path):
        """Check JavaScript code formatting with Prettier."""
        result = self.run_command(f"npx prettier --check {file_path}")
        return self.format_output("Prettier Formatting", result) if result else None

    def check_retire(self, file_path):
        """Check for security vulnerabilities using Retire.js (only for JS files)."""
        result = self.run_command(f"npx retire --js {file_path}")
        return self.format_output("Retire.js Security Check", result) if result else None

    def fix_jshint(self, file_path):
        """Fix JSHint issues by enabling ES6 support."""
        try:
            with open(file_path, "r+") as file:
                content = file.read()
                if "/* jshint esversion: 6 */" not in content:
                    file.seek(0, 0)
                    file.write("/* jshint esversion: 6 */\n" + content)
            print(f"✅ JSHint Fix: ES6 enabled in {file_path}")
        except Exception as e:
            print(f"❌ Error fixing JSHint: {e}")

    def fix_prettier(self, file_path):
        """Fix Prettier formatting issues."""
        result = self.run_command(f"npx prettier --write {file_path}")
        print(f"✅ Prettier Fix: Formatting applied to {file_path}")
        return result

    def fix_retire(self, file_path):
        """Re-run Retire.js without cache for accurate security checks."""
        result = self.run_command(f"npx retire --js {file_path} --no-cache")
        print(f"✅ Retire.js Fix: Security check re-run for {file_path}")
        return result

    def validate_code(self, file_path, auto_fix=False):
        """Run validation checks only for the specified JavaScript file."""
        print("\n🔍 Running JavaScript Code Validation...\n")
        print(f"Validating: {file_path}\n{'-'*50}")

        jshint_result = self.check_jshint(file_path)
        prettier_result = self.check_prettier(file_path)
        retire_result = self.check_retire(file_path)

        checks = [jshint_result, prettier_result, retire_result]

        # Print only non-None results
        for result in checks:
            if result is not None:
                print(result)

        # If auto_fix is enabled, attempt to fix issues
        if auto_fix:
            print("\n🔧 Attempting to fix issues...\n")
            if jshint_result:
                self.fix_jshint(file_path)
            if prettier_result:
                self.fix_prettier(file_path)
            if retire_result:
                self.fix_retire(file_path)

        print("\n✅ JavaScript validation complete!\n")
