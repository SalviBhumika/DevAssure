from devassure.requirements import extract_requirements,ambiguity_flags

def test_extracts_shall_and_must():
    reqs=extract_requirements("The API must reject invalid input.\nThe service shall log requests.")
    assert len(reqs)==2 and reqs[0].requirement_id=="REQ-001"

def test_flags_ambiguous_language():
    reqs=extract_requirements("The service should be fast for every user.")
    flags=ambiguity_flags(reqs[0])
    assert any("vague performance" in flag for flag in flags)


def test_context_retriever_skips_secret_paths():
    from devassure.context import ProjectContextRetriever
    retriever=ProjectContextRetriever()
    count=retriever.index_files([
        {"path":"src/api.py","content":"validate request payloads"},
        {"path":".env","content":"OPENAI_API_KEY=do-not-index"},
        {"path":"config/private.pem","content":"private key material"},
    ])
    assert count==1
    assert retriever.search("validate request payloads")[0]["path"]=="src/api.py"
