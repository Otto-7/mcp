def _parse_trace(result):
    trace_steps = []
    for code_flow in result.get("codeFlows", []):
        for thread_flow in code_flow.get("threadFlows", []):
            for loc_wrapper in thread_flow.get("locations", []):
                loc = loc_wrapper.get("location", loc_wrapper)
                phys = loc.get("physicalLocation", {})
                trace_steps.append({
                    "file": phys.get("artifactLocation", {}).get("uri", "unknown"),
                    "line": phys.get("region", {}).get("startLine", 0),
                    "message": loc.get("message", {}).get("text", "")
                })
    return trace_steps

def _parse_error(result):
    locations = result.get("locations", [])
    if locations:
        phys = locations[0].get("physicalLocation", {})
        file_uri = phys.get("artifactLocation", {}).get("uri", "")
        line_num = phys.get("region", {}).get("startLine", 0)
    else:
        file_uri = ""
        line_num = 0

    return {
        "file": file_uri,
        "line": line_num,
        "level": result.get("level", "warning"),
        "message": result.get("message", {}).get("text", ""),
        "rule_id": result.get("ruleId", ""),
        "trace": _parse_trace(result)
    }

def parse_sarif(data):
    errors = []
    for run in data.get("runs", []):
        for result in run.get("results", []):
            errors.append(_parse_error(result))
    return errors
