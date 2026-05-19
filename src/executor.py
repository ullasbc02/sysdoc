import subprocess


def execute_command(command: str) -> dict:
    try:
        result = subprocess.run( #creates the child process to execute the command
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )

        return {
            "command": command,
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode,
        }

    except subprocess.TimeoutExpired:
        return {
            "command": command,
            "success": False,
            "stdout": "",
            "stderr": "Command timed out",
            "returncode": -1,
        }