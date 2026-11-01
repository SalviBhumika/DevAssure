from __future__ import annotations
from .tools import DevelopmentTools


class DevelopmentWorkflow:
    """Bounded tool-calling workflow; proposal generation never triggers test execution."""
    def __init__(self):
        self.tools=DevelopmentTools()

    def analyze(self,specification: str,test_names: list[str] | None=None,
                context_files: list | None=None) -> dict:
        steps=[]; calls=[]
        parsed=self.tools.call("extract_requirements",specification=specification)
        steps.append("tool:extract_requirements"); calls.append({"tool":parsed.name,"status":"completed"})
        requirements=parsed.output

        flagged=self.tools.call("flag_ambiguity",requirements=requirements)
        steps.append("tool:flag_ambiguity"); calls.append({"tool":flagged.name,"status":"completed"})

        context=self.tools.call("retrieve_project_context",requirements=requirements,context_files=context_files or [])
        steps.append("tool:retrieve_project_context"); calls.append({"tool":context.name,"status":"completed"})

        proposed=self.tools.call("propose_tests",requirements=requirements,context_by_requirement=context.output)
        steps.append("tool:propose_tests"); calls.append({"tool":proposed.name,"status":"completed"})

        matrix=self.tools.call("traceability_matrix",requirements=requirements,test_names=test_names or [])
        steps.append("tool:traceability_matrix"); calls.append({"tool":matrix.name,"status":"completed"})
        steps.append("await_human_review")

        return {"requirements":flagged.output,"project_context":context.output,
                "test_proposals":proposed.output,"traceability":matrix.output,
                "workflow":steps,"tool_calls":calls,"execution_allowed":False}
