from devassure.workflow import DevelopmentWorkflow

def test_workflow_proposes_but_does_not_execute():
    result=DevelopmentWorkflow().analyze("The service must validate requests.")
    assert result["execution_allowed"] is False
    assert result["test_proposals"][0]["approved"] is False
    assert result["workflow"][-1]=="await_human_review"


def test_context_is_retrieved_and_cited_in_proposal():
    result=DevelopmentWorkflow().analyze(
        "The API must validate request payloads.",
        context_files=[{"path":"src/api.py","content":"Request schema validates payload fields."}],
    )
    proposal=result["test_proposals"][0]
    assert proposal["context_sources"]==["src/api.py:1"]
    assert result["project_context"]["REQ-001"]
