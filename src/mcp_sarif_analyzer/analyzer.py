def deduplicate(findings):
    seen = set()
    result = []
    for f in findings:
        if f.finding_id not in seen:
            seen.add(f.finding_id)
            result.append(f)
    return result

def filter_findings(findings, severity=None, status=None, has_comment=None):
    result = findings
    if severity:
        result = [f for f in result if f.severity == severity]
    if status:
        result = [f for f in result if f.status == status]
    if has_comment is not None:
        result = [f for f in result if bool(f.comments) == has_comment]
    return result

def paginate(items, offset=0, limit=20):
    total = len(items)
    page = items[offset:offset + limit]
    has_more = (offset + limit) < total
    return {
        "items": page,
        "total_count": total,
        "has_more": has_more,
        "next_offset": offset + limit if has_more else None
    }
