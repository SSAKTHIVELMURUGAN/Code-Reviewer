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
        install_eslint()
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

def install_eslint():
    """Set up ESLint manually with a custom configuration file."""
    
    print("🔄 Initializing ESLint setup...")

    # Install ESLint and required dependencies
    print("🔄 Installing ESLint packages...")
    subprocess.run(["npm", "install", "eslint"], check=True)
    subprocess.run(["npm", "install", "--save-dev", "eslint", "@eslint/js", "globals"], check=True)
    print("✅ ESLint installed.")

    # Define eslint.config.cjs file path
    eslint_config_file = "eslint.config.cjs"

    # Create eslint.config.cjs file if it doesn't exist
    if not os.path.exists(eslint_config_file):
        print("📄 Creating eslint.config.cjs file...")
        eslint_config_content = '''// eslint.config.cjs
const pluginJs = require("@eslint/js");

module.exports = [
  pluginJs.configs.recommended,
  {
    rules: {
      "no-unused-vars": "warn",
      "no-undef": "warn",
      "semi": ["error", "always"],             // Enforces semicolons at the end of statements
      "quotes": ["error", "single"],           // Enforces the use of single quotes
      "eqeqeq": "warn",                        // Enforces strict equality operators
      "curly": "error",                        // Requires consistent brace style for all control statements
      "no-console": "warn",                    // Warns about console usage
      "no-eval": "error",                      // Disallows the use of eval()
      "no-debugger": "error",                  // Disallows the use of debugger
      "indent": ["error", 2],                  // Enforces consistent indentation of 2 spaces
      "comma-dangle": ["error", "never"],      // Disallows trailing commas

      // Naming Conventions:
      "camelcase": ["error", { "properties": "always", "ignoreDestructuring": false }],
      "new-cap": ["error", { "newIsCap": true, "capIsNew": true }],

      // Break long lines for readability:
      "max-len": ["warn", { "code": 100, "ignoreUrls": true }],

      // Clear spacing around expressions and operators:
      "space-infix-ops": "error",
      "keyword-spacing": "error",
      "space-before-blocks": "error",
      "space-unary-ops": "error",

      // Prefer const and let (avoid var):
      "prefer-const": "error",
      "no-var": "error",

      // Minimize the use of global variables:
      "no-implicit-globals": "error",

      // Avoid using deprecated APIs:
      "no-restricted-syntax": [
        "error", // ✅ Added severity level
        {
          "selector": "CallExpression[callee.name='eval']",
          "message": "Avoid using eval() due to security risks."
        },
        {
          "selector": "Identifier[name='cur_frm']",
          "message": "Deprecated API cur_frm is not allowed. Use an alternative approach."
        },
        {
          "selector": "CallExpression[callee.name='get_query']",
          "message": "Deprecated API get_query() is not allowed. Use a modern API method."
        },
        {
          "selector": "CallExpression[callee.name='add_fetch']",
          "message": "Deprecated API add_fetch() is not allowed. Use an updated data retrieval method."
        }
      ]
    }
  }
];
'''
        with open(eslint_config_file, "w") as config_file:
            config_file.write(eslint_config_content)
        print("✅ eslint.config.cjs created with default settings.")
    else:
        print("✅ eslint.config.cjs already exists, skipping creation.")

    print("\n🚀 ESLint setup complete!")