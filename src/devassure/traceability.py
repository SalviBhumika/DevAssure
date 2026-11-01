from __future__ import annotations
import re
from .schemas import Requirement

def words(text: str) -> set[str]:
    stop={"shall","must","should","the","and","for","with","from","that","this","will","system","user","service","normal","under"}
    terms={w for w in re.findall(r"[a-z0-9]+",text.lower()) if len(w)>2 and w not in stop}
    if "fast" in terms: terms.add("latency")
    return terms

def map_tests(requirements: list[Requirement], test_names: list[str], min_overlap: int=1) -> dict:
    matrix=[]
    for req in requirements:
        req_terms=words(req.text)
        matches=[]
        for name in test_names:
            overlap=req_terms & words(name.replace("_"," "))
            if len(overlap)>=min_overlap:
                matches.append({"test_name":name,"matched_terms":sorted(overlap)})
        matrix.append({"requirement_id":req.requirement_id,"requirement":req.text,"tests":matches,"covered":bool(matches)})
    return {"requirements":matrix,"coverage":sum(row["covered"] for row in matrix)/len(matrix) if matrix else 0.0,
            "uncovered":[row["requirement_id"] for row in matrix if not row["covered"]]}
