import subprocess
import shlex


BLOCKED_COMMANDS = [
    "rm -rf /",
    "shutdown",
    "reboot",
    "mkfs",
    "dd ",
    ">:",
    ":(){",
    "chmod -R 777 /",
    "chown -R",
]


def is_safe_command(command):

    lowered = command.lower().strip()

    for blocked in BLOCKED_COMMANDS:
        if blocked in lowered:
            return False

    return True


def run_terminal(
    command,
    timeout=20
):

    if not command:
        return {
            "status": "error",
            "output": "Command kosong."
        }

    if not is_safe_command(command):
        return {
            "status": "blocked",
            "output": "Command diblokir karena berbahaya."
        }

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        output = ""

        if result.stdout:
            output += result.stdout

        if result.stderr:
            output += "\nSTDERR:\n" + result.stderr

        return {
            "status": "success" if result.returncode == 0 else "error",
            "returncode": result.returncode,
            "output": output[:12000]
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "output": f"Command timeout setelah {timeout} detik."
        }

    except Exception as e:
        return {
            "status": "error",
            "output": str(e)
        }
