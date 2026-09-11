import subprocess


def RunCommand(command, wait=True, timeout=180, shell=True):
    """
    Execute a command with a timeout.

    Returns:
        {
            "success": bool,
            "returncode": int,
            "stdout": str,
            "stderr": str,
            "timeout": bool,
        }
    """

    process = subprocess.Popen(
        command,
        shell=shell,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        # cwd=""
    )
    
    # Return immediately
    if not wait:
        return {
            "success": True,
            "process": process,
            "pid": process.pid,
            "running": process.poll() is None,
        }

    try:
        stdout, stderr = process.communicate(timeout=timeout)

        return {
            "success": process.returncode == 0,
            "returncode": process.returncode,
            "stdout": stdout.strip(),
            "stderr": stderr.strip(),
            "timeout": False,
        }

    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()

        return {
            "success": False,
            "returncode": -1,
            "stdout": stdout.strip(),
            "stderr": stderr.strip(),
            "timeout": True,
        }
