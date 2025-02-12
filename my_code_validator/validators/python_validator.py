import re
from .utils import run_command, format_output

class PythonValidator:
    def __init__(self, file_path):
        self.file_path = file_path
        self.summary = {
            "Pylint": "Skipped",
            "Mypy": "Skipped",
            "Dead Code": "Skipped",
            "Dependencies": "Skipped",
            "Complexity": "Skipped",
            "Maintainability": "Skipped",
            "Security": "Skipped",
            "Overall Status": "Pass"
        }
        self.failed_checks = 0  # Track failures to ensure correct Overall Status

    def check_pylint(self, file_path):
        raw_output = run_command(f"pylint {file_path}")
        if not raw_output.strip():
            return None  

        match = re.search(r"Your code has been rated at (-?\d+\.\d+)/10", raw_output)
        rating = float(match.group(1)) if match else 0

        self.summary["Pylint"] = "Passed" if rating >= 7 else "Failed"

        # Fail overall check if Pylint rating is below 5
        if rating < 5:
            self.fail_check("Pylint")

        formatted_result = f"""
{raw_output}

📊 **Rating:** {rating}/10
{self.generate_pylint_rating_explanation(rating)}
"""
        return format_output("Pylint Check",formatted_result)

    def check_mypy(self, file_path):
        output = run_command(f"mypy {file_path}")
        self.summary["Mypy"] = "Passed" if "Success" in output else "Failed"

        if "Success" not in output:
            self.fail_check("Mypy")

        return format_output("Mypy Type Check", output) if output.strip() else None

    def check_dead_code(self, file_path):
        output = run_command(f"vulture {file_path}")
        dead_code_count = len(re.findall(r"unused", output))
        self.summary["Dead Code"] = "Passed" if dead_code_count <= 3 else "Failed"

        if dead_code_count > 3:
            self.fail_check("Dead Code")

        return format_output("Dead Code Analysis", output) if output.strip() else None

    def check_dependencies(self, file_path):
        output = run_command(f"pipreqs --print {file_path}")
        return format_output("Dependency Check", output) if output.strip() else None

    def check_complexity(self, file_path):
        cc_result = run_command(f"radon cc {file_path} -a")
        mi_result = run_command(f"radon mi {file_path}")
        if not cc_result.strip() and not mi_result.strip():
            return None  

        cc_rank = self.extract_rank(cc_result, r"Average complexity: (\w)")
        mi_rank = self.extract_rank(mi_result, rf"{file_path} - (\w)")

        self.summary["Complexity"] = "Passed" if cc_rank in ["A", "B"] else "Failed"
        self.summary["Maintainability"] = "Passed" if mi_rank in ["A", "B"] else "Failed"

        if cc_rank not in ["A", "B"] or mi_rank not in ["A", "B"]:
            self.fail_check("Complexity & Maintainability")

        formatted_result = f"""
🛠 **Cyclomatic Complexity (CC)**
{cc_result}
➡️ **Rank: {cc_rank}**

📖 **Maintainability Index (MI)**
{mi_result}
➡️ **Rank: {mi_rank}**
"""
        return format_output("Complexity & Maintainability Check", formatted_result)

    def check_security(self, file_path):
        output = run_command(f"bandit -r {file_path}")
        high_issues = len(re.findall(r"Severity: High", output))
        self.summary["Security"] = "Passed" if high_issues == 0 else "Failed"

        if high_issues > 0:
            self.fail_check("Security")

        return format_output("Security Check", output) if output.strip() else None

    def check_coverage(self):
        output = run_command("coverage report -m")
        return format_output("Test Coverage", output) if output.strip() else None

    def extract_rank(self, output, pattern):
        """Extracts ranking (A, B, C, D, etc.) from a given output using regex."""
        match = re.search(pattern, output)
        return match.group(1) if match else "N/A"

    def fail_check(self, check_name):
        """Marks a check as failed and updates the overall status."""
        self.summary[check_name] = "Failed"
        self.failed_checks += 1
        self.summary["Overall Status"] = "Fail"

    def generate_pylint_rating_explanation(self, rating):
        if rating >= 9:
            return "✅ Excellent Code Quality! Keep it up!"
        elif rating >= 7:
            return "👍 Good Code Quality, but some improvements can be made."
        elif rating >= 5:
            return "⚠️ Average Code Quality. Consider refactoring."
        else:
            return "❌ Poor Code Quality. Major improvements needed!"

    def validate_code(self, file_path):
        print("\n🔍 Running Python Code Validation...\n")
        print(f"Validating: {file_path}\n{'-'*50}")

        checks = [
            self.check_pylint(file_path),
            self.check_mypy(file_path),
            self.check_dead_code(file_path),
            self.check_dependencies(file_path),
            self.check_complexity(file_path),
            self.check_security(file_path)
        ]

        for result in checks:
            if result:
                print(result)

        # Ensure "Overall Status" remains "Fail" if any check failed
        if self.failed_checks > 0:
            self.summary["Overall Status"] = "Fail"

        print("\n📊 Validation Summary\n" + "-"*30)
        for check, status in self.summary.items():
            print(f"{check:<20} {status}")
        print("-"*30)
