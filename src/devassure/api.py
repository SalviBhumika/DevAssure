from pathlib import Path
import os
from fastapi import FastAPI, HTTPException
from .schemas import AnalyzeRequest, ExecutionRequest
from .workflow import DevelopmentWorkflow
from .runner import run_approved_tests, ApprovalRequired

app=FastAPI(title="DevAssure API",version="0.1.0")
workflow=DevelopmentWorkflow()
@app.get("/health")
def health(): return {"status":"ok"}
@app.post("/analyze")
def analyze(req: AnalyzeRequest): return workflow.analyze(req.specification,req.test_names,req.context_files)
@app.post("/execute")
def execute(req: ExecutionRequest):
    try: return run_approved_tests(Path(os.getenv("WORKSPACE_DIR", ".")),req.test_file,req.approved,req.timeout_seconds)
    except ApprovalRequired as exc: raise HTTPException(status_code=403,detail=str(exc)) from exc
    except ValueError as exc: raise HTTPException(status_code=400,detail=str(exc)) from exc
