import subprocess


def execute_script(script_path: str) -> dict:
    try:
        result = subprocess.run(
            ["bash", script_path],
            capture_output=True,
            text=True,
            timeout=30,
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode,
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": "Script execution timed out",
            "returncode": -1,
        }