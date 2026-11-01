from __future__ import annotations
from .schemas import Requirement, TestProposal


class TestPlanner:
    """Deterministic baseline planner; proposals remain reviewable, not trusted executable code."""
    def propose(self, requirement: Requirement, context: list[dict] | None=None) -> TestProposal:
        slug=requirement.requirement_id.lower().replace("-","_")
        safe_text=requirement.text.replace('"','\\"')
        code=(f"def test_{slug}_behavior():\n"
              "    # Review and adapt this assertion to the actual implementation.\n"
              f"    expected_contract = {safe_text!r}\n"
              "    assert expected_contract.strip()\n")
        context=context or []
        return TestProposal(requirement_id=requirement.requirement_id,test_name=f"test_{slug}_behavior",
                            purpose="Create a reviewable behavioral test proposal using available requirement context.",
                            inputs=["valid input","invalid input","boundary input"],
                            expected_behavior="The implementation satisfies the requirement's measurable acceptance criteria.",
                            generated_code=code,
                            context_sources=[f"{hit['path']}:{hit['start_line']}" for hit in context],
                            approved=False)
