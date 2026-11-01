from pydantic import BaseModel, Field


class Requirement(BaseModel):
    requirement_id: str
    text: str
    acceptance_criteria: list[str] = Field(default_factory=list)


class ContextFile(BaseModel):
    path: str = Field(min_length=1, max_length=500)
    content: str = Field(min_length=1, max_length=50_000)


class AnalyzeRequest(BaseModel):
    specification: str = Field(min_length=1, max_length=100_000)
    context_files: list[ContextFile] = Field(default_factory=list, max_length=100)
    test_names: list[str] = Field(default_factory=list, max_length=500)


class TestProposal(BaseModel):
    requirement_id: str
    test_name: str
    purpose: str
    inputs: list[str]
    expected_behavior: str
    generated_code: str
    context_sources: list[str] = Field(default_factory=list)
    approved: bool = False


class ExecutionRequest(BaseModel):
    test_file: str
    approved: bool = False
    timeout_seconds: int = Field(default=10, ge=1, le=60)
