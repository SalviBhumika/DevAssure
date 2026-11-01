import json
from pathlib import Path
from devassure.requirements import extract_requirements
from devassure.traceability import map_tests
from devassure.context import ProjectContextRetriever
import re

SPEC="""
The service must validate input payloads and return a clear validation error.
The API shall record an audit event for every accepted request.
The system should respond fast under normal load.
"""
TESTS=["test_payload_validation_rejects_invalid_input","test_audit_event_written_for_request"]

def run():
    reqs=extract_requirements(SPEC)
    baseline=map_tests(reqs,TESTS)
    # Context arm retrieves candidate test identifiers from a tiny synthetic test-source file.
    # This demonstrates context lookup, not LLM generation or a user study.
    context=ProjectContextRetriever(chunk_lines=1)
    context.index_files([{"path":"tests/test_performance.py",
                          "content":"def test_service_response_latency_under_normal_load(): pass"}])
    retrieved_names=[]
    for requirement in reqs:
        hits=context.search(requirement.text,top_k=1)
        if hits:
            match=re.search(r"def\s+(test_[a-zA-Z0-9_]+)",hits[0]["text"])
            if match: retrieved_names.append(match.group(1))
    grounded=map_tests(reqs,TESTS+retrieved_names)
    return {"experiment":"context_retrieval_traceability_proxy",
            "retrieved_context_test_names":retrieved_names,
            "arms":{"name_only":baseline,"retrieved_context":grounded},
            "warning":"Synthetic deterministic proxy only. It does not measure LLM-generated test correctness, seeded-defect detection or human review effort."}

if __name__=="__main__":
    result=run(); path=Path("results/generated/traceability_ab.json"); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2)); print(json.dumps(result,indent=2))
