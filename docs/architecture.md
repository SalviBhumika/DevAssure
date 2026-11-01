# Architecture and workflow

`requirements.py` extracts candidate requirement lines and flags a small set of vague terms. `context.py` performs lexical retrieval over explicitly supplied source snippets, excluding obvious secret/config paths; `generator.py` creates a structured proposal and records the retrieved source references. `traceability.py` maps candidate test names with transparent lexical overlap. `tools.py` exposes an allowlist and `workflow.py` coordinates the bounded tool calls. The planner is deterministic; it is not an autonomous LLM policy. `runner.py` requires explicit approval and confines the selected test path to a workspace before invoking pytest through a subprocess. `api.py` exposes analysis and execution endpoints.

This is intentionally a modular monolith. A future LLM provider can be injected behind an interface without changing the approval policy.
