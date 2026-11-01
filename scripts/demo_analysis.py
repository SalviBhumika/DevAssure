from devassure.workflow import DevelopmentWorkflow
spec="""
The API must validate incoming request payloads and return a structured error for invalid input.
The service shall write an audit record for each accepted request.
The operator should be able to export a report in Markdown format.
"""
if __name__=="__main__":
    import json
    print(json.dumps(DevelopmentWorkflow().analyze(spec,["test_payload_validation","test_audit_record","test_report_export_markdown"]),indent=2))
