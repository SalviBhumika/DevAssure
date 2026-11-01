from __future__ import annotations
import re
from dataclasses import dataclass

SENSITIVE_PATH_PARTS={".env", "secrets", "credentials", "private", ".git", ".venv", "venv", "node_modules"}
STOP_WORDS={"the","and","for","with","from","that","this","shall","must","should","system","service","user"}


@dataclass
class ContextChunk:
    path: str
    start_line: int
    text: str


def _terms(text: str) -> set[str]:
    return {term for term in re.findall(r"[a-z0-9]+",text.lower())
            if len(term)>2 and term not in STOP_WORDS}


class ProjectContextRetriever:
    """Small lexical retriever over explicitly supplied, path-labelled source snippets."""
    def __init__(self, chunk_lines: int=35):
        if chunk_lines<1: raise ValueError("chunk_lines must be positive")
        self.chunk_lines=chunk_lines
        self.chunks: list[ContextChunk]=[]

    @staticmethod
    def _allowed(path: str) -> bool:
        parts={part.lower() for part in path.replace("\\","/").split("/")}
        suffix=path.lower().rsplit(".",1)[-1] if "." in path else ""
        if parts & SENSITIVE_PATH_PARTS: return False
        if suffix in {"pem","key","p12","pfx","env"}: return False
        return True

    def index_files(self, files: list[dict]) -> int:
        self.chunks=[]
        for file in files:
            path=str(file.get("path",""))
            content=str(file.get("content",""))
            if not self._allowed(path) or not content.strip(): continue
            lines=content.splitlines()
            for offset in range(0,len(lines),self.chunk_lines):
                section="\n".join(lines[offset:offset+self.chunk_lines]).strip()
                if section:
                    self.chunks.append(ContextChunk(path,offset+1,section))
        return len(self.chunks)

    def search(self, query: str, top_k: int=3) -> list[dict]:
        q=_terms(query)
        if not q: return []
        scored=[]
        for chunk in self.chunks:
            terms=_terms(chunk.text)
            overlap=len(q & terms)
            if overlap:
                score=overlap/(len(q)**0.5 * max(len(terms),1)**0.5)
                scored.append((score,chunk))
        scored.sort(key=lambda item:item[0],reverse=True)
        return [{"score":score,"path":chunk.path,"start_line":chunk.start_line,"text":chunk.text}
                for score,chunk in scored[:top_k]]
