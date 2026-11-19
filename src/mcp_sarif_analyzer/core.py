from parser import load_and_parse
from normalizer import normalize_severity
from analyzer import deduplicate, filter_findings, paginate
import review_store
import config
from dataclasses import asdict
from parser import load_sarif

_findings = None
_rules = None
_store = None # словарь вердиктов LLM

def _load_data():
    global _findings, _rules, _store

    if _findings is None:
        findings_list, rules = load_and_parse(config.SARIF_PATH)
        findings_list = normalize_severity(findings_list, rules)
        findings_list = deduplicate(findings_list)

        _findings = {f.finding_id: f for f in findings_list}
        _rules = rules
        _store = review_store.load(config.SARIF_PATH.stem)


def get_summary():
    _load_data()
    findings_list = list(_findings.values())

    total = len(findings_list)
    remaining = sum(1 for f in findings_list if f.finding_id not in _store) #

    by_severity = {}
    for f in findings_list:
        by_severity[f.severity] = by_severity.get(f.severity, 0) + 1

    return {"total": total, "remaining": remaining, "by_severity": by_severity}


def get_results(severity=None, status=None, has_comment=None, has_review=None, offset=0, limit=20):
    _load_data()
    findings_list = list(_findings.values())
    filtered = filter_findings(findings_list, severity, status, has_comment)

    if has_review is not None:
        filtered = [f for f in filtered if (f.finding_id in _store) == has_review]

    result = paginate(filtered, offset, limit)
    result["items"] = [asdict(f) for f in result["items"]]
    return result


def get_result(finding_id):
    _load_data()
    finding = _findings.get(finding_id)
    if not finding:
        return {"error": f"Finding {finding_id} не найден"}
    return asdict(finding)


def get_rule(rule_id): # описание правила
    _load_data()
    rule = _rules.get(rule_id)
    if not rule:
        return {"error": f"Правило {rule_id} не найдено"}
    return asdict(rule)


def save_reviews(records):
    _load_data()
    result = review_store.save(_store, records, _findings, config.SARIF_PATH.stem)
    remaining = sum(1 for f in _findings.values() if f.finding_id not in _store)
    result["remaining"] = remaining
    return result

def export_report():
    _load_data()
    return review_store.export(_store, _findings, config.SARIF_PATH.stem)

def export_sarif_report():
    _load_data()
    original_data = load_sarif(config.SARIF_PATH)
    return review_store.export_sarif(_store, original_data, config.SARIF_PATH.stem)
