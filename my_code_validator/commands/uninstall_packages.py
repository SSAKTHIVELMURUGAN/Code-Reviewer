import subprocess
import sys
import os
import shutil

from .dependencies import install_requires, js_dependencies

def uninstall_packages():
    print(f"🗑 Uninstalling Python dependencies: {install_requires}")
    print(f"🗑 Uninstalling JavaScript dependencies: {js_dependencies}")

    """Uninstall Python dependencies."""
    print("🔄 Uninstalling Python dependencies...")

    if not install_requires:
        print("⚠️ No Python dependencies found. Skipping uninstallation.")
    else:
        for package in install_requires:
            print(f"🚀 Uninstalling {package}...")
            subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", package], check=False)
        
        # Ensure all dependencies are removed, including leftovers
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "frappe-code-validate"], check=False)
        subprocess.run([sys.executable, "-m", "pip", "freeze"], stdout=open("pip_freeze.txt", "w"))
        with open("pip_freeze.txt", "r") as f:
            installed_packages = f.read().splitlines()
        if installed_packages:
            print("⚠️ Some Python packages are still installed:", installed_packages)
        else:
            print("✅ Python dependencies fully uninstalled.")

    """Uninstall JavaScript dependencies."""
    print("🔄 Uninstalling JavaScript dependencies...")

    if not js_dependencies:
        print("⚠️ No JavaScript dependencies found. Skipping uninstallation.")
    else:
        for package in js_dependencies:
            print(f"🚀 Uninstalling {package}...")
            subprocess.run(["npm", "uninstall", package], check=False)

    """Remove node_modules and package-lock.json to fully reset dependencies."""
    if os.path.exists("node_modules"):
        shutil.rmtree("node_modules")
        print("🗑 Removed node_modules directory.")

    if os.path.exists("package-lock.json"):
        os.remove("package-lock.json")
        print("🗑 Removed package-lock.json.")

    print("✅ JavaScript dependencies fully uninstalled.")

    """Remove only the frappe-code-validate related lines from the pre-commit hook."""
    remove_pre_commit_hook()

def remove_pre_commit_hook():
    """Modify the pre-commit hook by removing only the frappe-code-validate command and echo line."""
    pre_commit_path = ".git/hooks/pre-commit"

    if not os.path.exists(pre_commit_path):
        print("⚠️ No pre-commit hook found. Skipping removal.")
        return

    with open(pre_commit_path, "r") as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        # Remove only the specific lines related to frappe-code-validate
        if "echo \"🚀 Running frappe-code-validate on staged files...\"" in line:
            continue
        if "python -m my_code_validator.cli validate-staged" in line:
            continue
        new_lines.append(line)

    with open(pre_commit_path, "w") as file:
        file.writelines(new_lines)

    print("✅ Removed frappe-code-validate command and echo message from the pre-commit hook.")

