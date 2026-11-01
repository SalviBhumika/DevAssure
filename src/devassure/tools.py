from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Any
from .requirements import extract_requirements, ambiguity_flags
from .traceability import map_tests
from .generator import TestPlanner
from .context import ProjectContextRetriever


@dataclass
class ToolResult:
    name: str
    output: Any


class DevelopmentTools:
    """Allowlisted deterministic tools; no tool accepts an arbitrary command string."""
    def __init__(self):
        self.planner=TestPlanner()
        self.context_retriever=ProjectContextRetriever()
        self._tools: dict[str, Callable[..., Any]]={
            "extract_requirements":self.extract,
            "flag_ambiguity":self.flag,
            "retrieve_project_context":self.retrieve_context,
            "propose_tests":self.propose,
            "traceability_matrix":self.traceability,
        }

    def call(self,name: str,**kwargs) -> ToolResult:
        if name not in self._tools:
            raise ValueError(f"Tool is not allowlisted: {name}")
        return ToolResult(name=name,output=self._tools[name](**kwargs))

    @staticmethod
    def extract(specification: str):
        return extract_requirements(specification)

    @staticmethod
    def flag(requirements):
        return [{"requirement":req.model_dump(),"flags":ambiguity_flags(req)} for req in requirements]

    def retrieve_context(self,requirements,context_files):
        serialized=[item.model_dump() if hasattr(item,"model_dump") else item for item in context_files]
        self.context_retriever.index_files(serialized)
        return {req.requirement_id:self.context_retriever.search(req.text,top_k=2) for req in requirements}

    def propose(self,requirements,context_by_requirement):
        return [self.planner.propose(req,context_by_requirement.get(req.requirement_id,[])).model_dump()
                for req in requirements]

    @staticmethod
    def traceability(requirements,test_names):
        return map_tests(requirements,test_names)
