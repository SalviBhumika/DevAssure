import pytest
from devassure.runner import run_approved_tests,ApprovalRequired

def test_approval_gate(tmp_path):
    (tmp_path/"test_ok.py").write_text("def test_ok(): assert True")
    with pytest.raises(ApprovalRequired): run_approved_tests(tmp_path,"test_ok.py",False)

def test_restricted_runner(tmp_path):
    (tmp_path/"test_ok.py").write_text("def test_ok(): assert True")
    result=run_approved_tests(tmp_path,"test_ok.py",True)
    assert result["status"]=="passed"

def test_rejects_path_escape(tmp_path):
    with pytest.raises(ValueError): run_approved_tests(tmp_path,"../outside.py",True)
