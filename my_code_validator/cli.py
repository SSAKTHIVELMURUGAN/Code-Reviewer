import argparse
import subprocess
from my_code_validator.commands.validate_project import validate_project
from my_code_validator.commands.validate_file import validate_files
from my_code_validator.commands.install_packages import install_packages
from my_code_validator.commands.uninstall_packages import uninstall_packages
from my_code_validator.commands.version import version

def get_staged_files():
    """Retrieve a list of staged files from Git."""
    try:
        result = subprocess.run(["git", "diff", "--name-only", "--cached"], capture_output=True, text=True, check=True)
        files = result.stdout.strip().split("\n")
        return [file for file in files if file.endswith((".py", ".js"))]
    except subprocess.CalledProcessError:
        print("❌ Error: Failed to get staged files. Ensure you're inside a Git repository.")
        return []

def main():
    """Entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Frappe Code Validator CLI")

    # Version flag
    parser.add_argument("--version", "-v", action="store_true", help="Show the version of frappe-code-validate")

    # Subparsers for different commands
    subparsers = parser.add_subparsers(dest="command")

    # Install packages
    subparsers.add_parser("install", help="Install required dependencies")

    # Uninstall package
    subparsers.add_parser("uninstall", help="Uninstall frappe-code-validate package")

    # Validate project
    validate_parser = subparsers.add_parser("validate", help="Validate all Python and JS files in a project directory")
    validate_parser.add_argument("directory", type=str, help="Project directory path")

    # Validate multiple files
    file_parser = subparsers.add_parser("validate-file", help="Validate one or more Python or JS files")
    file_parser.add_argument("files", nargs="+", help="Path(s) to file(s)")

    # Validate only staged files
    subparsers.add_parser("validate-staged", help="Validate only staged Python and JS files")


    args = parser.parse_args()

    # Handle commands
    if args.version:
        version()
    elif args.command == "validate":
        validate_project(args.directory)
    elif args.command == "validate-file":
        validate_files(args.files)  
    elif args.command == "validate-staged":
        staged_files = get_staged_files()
        if staged_files:
            print(f"📂 Staged files: {', '.join(staged_files)}")
            validate_files(staged_files)
        else:
            print("✅ No staged Python or JavaScript files to validate.")
    elif args.command == "install":
        install_packages()
    elif args.command == "uninstall":
        uninstall_packages()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
