import subprocess
import sys
import os
import shutil

from .dependencies import install_requires, js_dependencies

def uninstall_packages():
    """Uninstall both Python and JavaScript dependencies."""
    remove_python_dependencies()
    remove_js_dependencies()
    remove_pre_commit_hook()

def remove_python_dependencies():
    """Uninstall Python dependencies."""
    print(f"🗑 Uninstalling Python dependencies: {install_requires}")

    if not install_requires:
        print("⚠️ No Python dependencies found. Skipping uninstallation.")
        return

    for package in install_requires:
        print(f"🚀 Uninstalling {package}...")
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", package], check=False)

    # Ensure all dependencies are removed, including leftovers
    subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "frappe-code-validate"], check=False)

    print("✅ Python dependencies fully uninstalled.")

def remove_js_dependencies():
    """Uninstall JavaScript dependencies."""
    print(f"🗑 Uninstalling JavaScript dependencies: {js_dependencies}")

    if not js_dependencies:
        print("⚠️ No JavaScript dependencies found. Skipping uninstallation.")
        return

    for package in js_dependencies:
        print(f"🚀 Uninstalling {package}...")
        subprocess.run(["npm", "uninstall", package], check=False)

    remove_node_modules()

def remove_node_modules():
    """Remove node_modules and package-lock.json to fully reset dependencies."""
    if os.path.exists("node_modules"):
        shutil.rmtree("node_modules")
        print("🗑 Removed node_modules directory.")

    if os.path.exists("package-lock.json"):
        os.remove("package-lock.json")
        print("🗑 Removed package-lock.json.")

    print("✅ JavaScript dependencies fully uninstalled.")

def remove_pre_commit_hook():
    """Modify the pre-commit hook by removing only the frappe-code-validate command and echo line."""
    pre_commit_path = ".git/hooks/pre-commit"

    if not os.path.exists(pre_commit_path):
        print("⚠️ No pre-commit hook found. Skipping removal.")
        return

    with open(pre_commit_path, "r") as file:
        lines = file.readlines()

    new_lines = [
        line for line in lines
        if "echo \"🚀 Running frappe-code-validate on staged files...\"" not in line
        and "python -m my_code_validator.cli validate-staged" not in line
    ]

    with open(pre_commit_path, "w") as file:
        file.writelines(new_lines)

    print("✅ Removed frappe-code-validate command and echo message from the pre-commit hook.")
