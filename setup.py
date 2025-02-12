import os
import subprocess
from setuptools import setup, find_packages

# JavaScript dependencies
js_tools = ["jshint", "prettier", "retire"]

# Function to install JS dependencies locally
def install_js_dependencies():
    print("\n📦 Installing JavaScript dependencies locally...\n")

    try:
        # Initialize npm project if package.json is missing
        if not os.path.exists("package.json"):
            subprocess.run(["npm", "init", "-y"], check=True)

        # Install JS dependencies **locally** (no `-g`)
        subprocess.run(["npm", "install"] + js_tools, check=True)
    except subprocess.CalledProcessError as e:
        print("❌ Error installing JavaScript dependencies:", e)
        exit(1)

# Install JS dependencies before setup
install_js_dependencies()

setup(
    name="frappe-code-validate",
    version="1.1.0",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "frappe-code=my_code_validator.cli:main",
        ],
    },
    python_requires=">=3.8",
)
