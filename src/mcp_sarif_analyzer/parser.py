import json

from config import SARIF_PATH
from models import Comment, Finding, Rule, TraceStep


class SarifError(Exception):
    """ Ошибка """


def load_sarif(path):
    try:
        text = path.read_text(encoding="utf-8")
        data = json.loads(text)
    except FileNotFoundError:
        raise SarifError(f"Файл не найден: {path}")
    except json.JSONDecodeError as e:
        raise SarifError(f"Битый JSON: {e}")

    if data.get("version") != "2.1.0":
        raise SarifError(f"Неверная версия SARIF: {data.get('version')}")
    if not isinstance(data.get("runs"), list):
        raise SarifError("В SARIF нет массива 'runs'")
    return data


def _parse_trace(result):
    steps = []
    for code_flow in result.get("codeFlows") or []:
        for thread_flow in code_flow.get("threadFlows") or []:
            for loc_wrapper in thread_flow.get("locations") or []:
                loc = loc_wrapper.get("location") or loc_wrapper
                phys = loc.get("physicalLocation") or {}
                artifact = phys.get("artifactLocation") or {}
                region = phys.get("region") or {}
                message = loc.get("message") or {}

                steps.append(TraceStep(
                    file=artifact.get("uri", "unknown"),
                    line=region.get("startLine", 0),
                    message=message.get("text", ""),
                ))
    return steps


def _parse_comments(result):
    comments = []
    props = result.get("properties") or {}
    for c in props.get("comments") or []:
        comments.append(Comment(
            text=c.get("text", ""),
            created_by=c.get("createdBy", ""),
            created_ts=c.get("createTs", "")
        ))
    return comments


def _parse_error(result):
    locations = result.get("locations", [])
    if locations:
        phys = locations[0].get("physicalLocation") or {}
        file_uri = (phys.get("artifactLocation") or {}).get("uri", "")
        line_num = (phys.get("region") or {}).get("startLine", 0)
    else:
        file_uri = ""
        line_num = 0

    finding_id = (result.get("fingerprints") or {}).get("invariant")
    if not finding_id:
        raise SarifError(
            f"Нет fingerprints.invariant: {result.get('ruleId')} {file_uri}:{line_num}"
        )

    props = result.get("properties") or {}
    message_text = (result.get("message") or {}).get("text", "")

    return Finding(
        finding_id=finding_id,
        file=file_uri,
        line=line_num,
        level=result.get("level", "warning"),
        severity=props.get("checker_severity", "Unknown"),
        status=props.get("status"),
        message=message_text,
        rule_id=result.get("ruleId", ""),
        comments=_parse_comments(result),
        trace=_parse_trace(result),
    )


def _parse_rules(data):
    rules = {}
    for run in data.get("runs", []):
        for r in run.get("tool", {}).get("driver", {}).get("rules", []):
            rule_id = r.get("id")
            if not rule_id:
                continue
            props = r.get("properties") or {}
            cwe_list = props.get("cwe") or []
            rules[rule_id] = Rule(
                rule_id=rule_id,
                name=r.get("name", ""),
                description=r.get("shortDescription", {}).get("text", ""),
                severity=props.get("severity", "Unknown"),
                reliability=props.get("reliability", ""),
                cwe=cwe_list,
            )
    return rules


def parse_sarif(data):
    findings = []
    for run in data.get("runs", []):
        for result in run.get("results", []):
            findings.append(_parse_error(result))
    return findings, _parse_rules(data)


def load_and_parse(path):
    data = load_sarif(path)
    return parse_sarif(data)
