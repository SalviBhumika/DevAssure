# Security and trust boundaries

Requirements and source files are untrusted input. Never execute commands proposed by a model. The current runner accepts only an existing Python file within a caller-supplied workspace, invokes a fixed pytest command without a shell and applies a timeout. Python test code still has the process user's permissions. A hardened container or disposable VM is required for untrusted generated tests. Keep secrets out of the indexed workspace.


Project context is supplied explicitly in the request rather than read from arbitrary paths. Obvious secret paths (for example `.env`, `.pem`, credentials and virtual-environment directories) are skipped, but callers should still avoid transmitting secrets and review selected context before indexing.
