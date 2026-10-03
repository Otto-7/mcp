import json

def parse_sarif(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    errors=[]
    for result in data["runs"][0]["results"]:
        trace_steps=[]
        for code_flow in result.get("codeFlows", []):
            for thread_flow in code_flow.get("threadFlows", []):
                for loc_wrapper in thread_flow.get("locations", []):
                    loc=loc_wrapper.get("location", loc_wrapper)
                    phys=loc.get("physicalLocation", {})
                    trace_steps.append({
                        "file": phys.get("artifactLocation", {}).get("uri", "unknown"),
                        "line": phys.get("region", {}).get("startLine", 0),
                        "message": loc.get("message", {}).get("text", "")
                    })

        errors.append({
            "file": result["locations"][0]["physicalLocation"]["artifactLocation"]["uri"],
            "line": result["locations"][0]["physicalLocation"]["region"]["startLine"],
            "level": result["level"],
            "message": result["message"]["text"],
            "rule_id": result["ruleId"],
            "trace": trace_steps
        })

    return errors

if __name__=="__main__":
    result=parse_sarif(r"C:\Users\User\Documents\Проект сервер\zlib-git-master-09a1572.sarif")
    print(f"Всего ошибок: {len(result)}")