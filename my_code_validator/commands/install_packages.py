import subprocess
import sys
import os

from .dependencies import install_requires, js_dependencies

# Updated pre-commit hook with strict validation
PRE_COMMIT_HOOK = """#!/bin/bash
echo "🚀 Running frappe-code-validate on staged files..."

# Run validation and capture output + exit status
OUTPUT=$(python -m my_code_validator.cli validate-staged)
RESULT=$?

echo "$OUTPUT"

# Check if the validation failed
if [[ $OUTPUT == *"Overall Status       Fail"* ]]; then
    echo "❌ Validation failed! Commit aborted."
    exit 1
fi

# Fallback check in case RESULT is non-zero
if [ $RESULT -ne 0 ]; then
    echo "❌ Validation script exited with an error! Commit aborted."
    exit 1
fi

exit 0

"""

def install_packages():
    """Install required Python and JavaScript dependencies and set up pre-commit hook."""
    
    print("🔄 Checking and installing dependencies...")

    # ✅ Ensure pre-commit is installed
    if not is_pre_commit_installed():
        print("🔄 Installing pre-commit...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pre-commit"], check=True)
        print("✅ pre-commit installed.")

    # Install Python dependencies
    if install_requires:
        print("🔄 Installing Python dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install"] + install_requires, check=True)
        print("✅ Python dependencies installed.")

    # Install JavaScript dependencies
    if js_dependencies:
        print("🔄 Installing JavaScript dependencies...")
        subprocess.run(["npm", "install"] + js_dependencies, check=True)
        print("✅ JavaScript dependencies installed.")

    setup_pre_commit_hook()

def is_pre_commit_installed():
    """Check if pre-commit is installed."""
    try:
        subprocess.run(["pre-commit", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def setup_pre_commit_hook():
    """Set up the pre-commit hook to run frappe-code-validate before committing."""
    git_hooks_dir = ".git/hooks"
    pre_commit_path = os.path.join(git_hooks_dir, "pre-commit")

    if not os.path.exists(git_hooks_dir):
        print("❌ Error: Not a Git repository. Pre-commit hook setup failed.")
        return

    if os.path.exists(pre_commit_path):
        print("🔄 Updating existing pre-commit hook...")
    else:
        print("📝 Creating new pre-commit hook...")

    # Write the pre-commit script
    with open(pre_commit_path, "w") as hook_file:
        hook_file.write(PRE_COMMIT_HOOK)

    # Make it executable
    subprocess.run(["chmod", "+x", pre_commit_path], check=True)
    print("✅ Pre-commit hook installed successfully.")