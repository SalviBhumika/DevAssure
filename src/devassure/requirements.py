from __future__ import annotations
import re
from .schemas import Requirement

VERB=re.compile(r"\b(shall|must|should|will|is required to)\b",re.I)

def extract_requirements(specification: str) -> list[Requirement]:
    requirements=[]
    for raw in specification.splitlines():
        line=raw.strip().lstrip("-•* ").strip()
        if len(line)<12 or not VERB.search(line): continue
        rid=f"REQ-{len(requirements)+1:03d}"
        criteria=[]
        if ":" in line and line.split(":",1)[1].strip(): criteria.append(line.split(":",1)[1].strip())
        requirements.append(Requirement(requirement_id=rid,text=line,acceptance_criteria=criteria))
    return requirements

def ambiguity_flags(requirement: Requirement) -> list[str]:
    flags=[]; low=requirement.text.lower()
    vague={"fast":"contains vague performance term 'fast'","user-friendly":"contains subjective term 'user-friendly'","secure":"contains broad term 'secure' without a measurable criterion","appropriate":"contains subjective term 'appropriate'"}
    for term,message in vague.items():
        if term in low: flags.append(message)
    if not requirement.acceptance_criteria: flags.append("no explicit acceptance criterion parsed")
    return flags
