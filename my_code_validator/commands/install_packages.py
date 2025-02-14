import subprocess
import sys
import os

from .dependencies import install_requires, js_dependencies

PRE_COMMIT_HOOK = """#!/bin/bash
echo "🚀 Running frappe-code-validate on staged files..."

OUTPUT=$(python -m my_code_validator.cli validate-staged)
RESULT=$?

echo "$OUTPUT"

if [[ $OUTPUT == *"Overall Status       Fail"* ]]; then
    echo "❌ Validation failed! Commit aborted."
    exit 1
fi

if [ $RESULT -ne 0 ]; then
    echo "❌ Validation script exited with an error! Commit aborted."
    exit 1
fi

exit 0
"""

def install_python_dependencies():
    """Install required Python dependencies."""
    if install_requires:
        print("\U0001F504 Installing Python dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install"] + install_requires, check=True)
        print("✅ Python dependencies installed.")

def install_js_dependencies():
    """Install required JavaScript dependencies."""
    if js_dependencies:
        print("\U0001F504 Installing JavaScript dependencies...")
        subprocess.run(["npm", "install"] + js_dependencies, check=True)
        install_eslint()
        print("✅ JavaScript dependencies installed.")

def is_pre_commit_installed():
    """Check if pre-commit is installed."""
    try:
        subprocess.run(["pre-commit", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_pre_commit():
    """Ensure pre-commit is installed."""
    if not is_pre_commit_installed():
        print("\U0001F504 Installing pre-commit...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pre-commit"], check=True)
        print("✅ pre-commit installed.")

def setup_pre_commit_hook():
    """Set up the pre-commit hook."""
    git_hooks_dir = ".git/hooks"
    pre_commit_path = os.path.join(git_hooks_dir, "pre-commit")
    
    if not os.path.exists(git_hooks_dir):
        print("❌ Error: Not a Git repository. Pre-commit hook setup failed.")
        return
    
    action = "Updating" if os.path.exists(pre_commit_path) else "Creating"
    print(f"\U0001F58D {action} pre-commit hook...")
    
    with open(pre_commit_path, "w") as hook_file:
        hook_file.write(PRE_COMMIT_HOOK)
    
    subprocess.run(["chmod", "+x", pre_commit_path], check=True)
    print("✅ Pre-commit hook installed successfully.")

def install_eslint():
    """Set up ESLint with a custom configuration file."""
    print("\U0001F504 Installing ESLint...")
    subprocess.run(["npm", "install", "eslint"], check=True)
    subprocess.run(["npm", "install", "--save-dev", "eslint", "@eslint/js", "globals"], check=True)
    print("✅ ESLint installed.")
    
    eslint_config_file = "eslint.config.cjs"
    if not os.path.exists(eslint_config_file):
        print("📄 Creating eslint.config.cjs file...")
        with open(eslint_config_file, "w") as config_file:
            config_file.write("""// eslint.config.cjs
const pluginJs = require("@eslint/js");

module.exports = [
  pluginJs.configs.recommended,
  {
    rules: {
      "no-unused-vars": "warn",
      "no-undef": "warn",
      "semi": ["error", "always"],
      "quotes": ["error", "single"],
      "eqeqeq": "warn",
      "curly": "error",
      "no-console": "warn",
      "no-eval": "error",
      "no-debugger": "error",
      "indent": ["error", 2],
      "comma-dangle": ["error", "never"],
      "camelcase": ["error", { "properties": "always", "ignoreDestructuring": false }],
      "new-cap": ["error", { "newIsCap": true, "capIsNew": true }],
      "max-len": ["warn", { "code": 100, "ignoreUrls": true }],
      "space-infix-ops": "error",
      "keyword-spacing": "error",
      "space-before-blocks": "error",
      "space-unary-ops": "error",
      "prefer-const": "error",
      "no-var": "error",
      "no-implicit-globals": "error",
      "no-restricted-syntax": [
        "error",
        { "selector": "CallExpression[callee.name='eval']", "message": "Avoid eval()." },
        { "selector": "Identifier[name='cur_frm']", "message": "Deprecated API cur_frm is not allowed." },
        { "selector": "CallExpression[callee.name='get_query']", "message": "Deprecated API get_query()." },
        { "selector": "CallExpression[callee.name='add_fetch']", "message": "Deprecated API add_fetch()." }
      ]
    }
  }
];""")
        print("✅ eslint.config.cjs created with default settings.")
    else:
        print("✅ eslint.config.cjs already exists.")

def install_packages():
    """Install required dependencies and set up pre-commit hook."""
    print("\U0001F504 Checking and installing dependencies...")
    install_pre_commit()
    install_python_dependencies()
    install_js_dependencies()
    setup_pre_commit_hook()
    print("🚀 All dependencies installed ")

