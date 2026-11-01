from __future__ import annotations
import subprocess, sys
from pathlib import Path

class ApprovalRequired(PermissionError): pass

def run_approved_tests(project_root: Path, test_file: str, approved: bool, timeout_seconds: int=10) -> dict:
    if not approved: raise ApprovalRequired("Human approval is required before test execution")
    root=project_root.resolve(); target=(root/test_file).resolve()
    if root not in target.parents or target.suffix!=".py" or not target.is_file():
        raise ValueError("Test file must be an existing Python file inside the project workspace")
    # Fixed executable and argument vector; shell=False prevents shell interpolation.
    command=[sys.executable,"-m","pytest","-q",str(target)]
    try:
        result=subprocess.run(command,cwd=root,capture_output=True,text=True,timeout=timeout_seconds,check=False)
    except subprocess.TimeoutExpired:
        return {"status":"timeout","returncode":None,"stdout":"","stderr":"Test run exceeded timeout"}
    return {"status":"passed" if result.returncode==0 else "failed","returncode":result.returncode,
            "stdout":result.stdout[-6000:],"stderr":result.stderr[-6000:]}
