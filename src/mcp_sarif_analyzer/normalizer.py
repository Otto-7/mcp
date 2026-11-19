def normalize_severity(findings, rules):
    for f in findings:
        if (not f.severity or f.severity == "Unknown") and f.rule_id in rules:
            f.severity = rules[f.rule_id].severity
        if not f.severity:
            f.severity = "Unknown"
    return findings
