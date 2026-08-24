import subprocess
import json
import os
import logging

logger = logging.getLogger(__name__)

def run_pmd(target_path: str) -> dict:
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    pmd_exe = os.path.join(project_root, "tools", "pmd", "bin", "pmd.bat" if os.name == 'nt' else "pmd")

    
    command = [
        pmd_exe,
        "check",
        "-d", target_path,
        "-R", "category/java/errorprone.xml,category/java/bestpractices.xml",
        "-f", "json"
    ]

    logger.info(f"Executing PMD on {target_path}")

    try:
        # check=False is intentional: PMD exits with code 4 when violations are found.
        result = subprocess.run(command, capture_output=True, text=True, check=False)

        # Code 0 = no violations, 4 = violations found, anything else = real error.
        if result.returncode not in (0, 4):
            logger.error(f"PMD failed with unexpected exit code {result.returncode}")
            logger.error(result.stderr)
            raise RuntimeError("PMD execution failed")

        pmd_report = json.loads(result.stdout)

        smell_found = len(pmd_report.get('files', []))
        logger.info(f"PMD Analysis complete. Found issues in {smell_found} files.")

        return pmd_report

    except FileNotFoundError:
        logger.error("PMD Executable not found. Did you run setup_bash.sh?")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse PMD output. Raw output: {result.stdout}")
        raise

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    pmd_results = run_pmd("tests/sample_java/OrderProcessor.java")

    print("\n------ PMD Deterministic Analysis Result -------\n")
    print(json.dumps(pmd_results, indent=2))
    print("\n---------------- Analysis End ------------------\n")