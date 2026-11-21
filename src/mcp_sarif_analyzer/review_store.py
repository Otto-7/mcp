import json
from config import  ALLOWED_VERDICTS, REPORTS_DIR, REVIEWS_DIR
from datetime import datetime, timezone
import os
import sys


def load(source_key: str) -> dict:
    path = REVIEWS_DIR / f"{source_key}.jsonl"
    if not path.exists():
        return {}
    store = {}
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                if not isinstance(rec, dict):
                    print(f"Строка {line_number} в {path.name} не является словарем. Пропущено.",
                          file=sys.stderr)
                    continue
            except json.JSONDecodeError:
                print(f"Битый JSON в {path.name} на строке {line_number}. Пропущено.", file=sys.stderr)
                continue
            if fid := rec.get("finding_id"):
                verdict = rec.get("verdict")
                if verdict in ALLOWED_VERDICTS:
                    store[fid] = {"verdict": verdict, "text": rec.get("text", "")}
                else:
                    print(f"Неверный вердикт '{verdict}' в {path.name} на строке {line_number}.",
                          file=sys.stderr)
    return store

def _validate(rec, findings):
    fid = rec.get("finding_id")
    if not fid:
        return "missing finding_id"
    if fid not in findings:
        return f"unknown finding_id: {fid}"
    verdict = rec.get("verdict")
    if verdict not in ALLOWED_VERDICTS:
        return f"invalid verdict: {verdict!r}"
    if not (rec.get("text") or "").strip():
        return "empty text"
    return None

def _append_to_file(source_key, records):
    path = REVIEWS_DIR / f"{source_key}.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for rec in records:
            f.write(
                json.dumps(
                    {
                        "finding_id": rec["finding_id"],
                        "verdict": rec["verdict"],
                        "text": rec["text"],
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )

def save(store, records, findings, source_key):
    valid = []
    rejected = []
    for rec in records:
        reason = _validate(rec, findings)
        if reason is None:
            valid.append(rec)
        else:
            rejected.append({"finding_id": rec.get("finding_id"), "reason": reason})
    if valid:
        _append_to_file(source_key, valid)
        for rec in valid:
            store[rec["finding_id"]] = {"verdict": rec["verdict"], "text": rec["text"]}
    return {"saved": len(valid), "rejected": rejected}


def export_sarif(store, original_data, source_key):
    for run in original_data.get("runs", []):
        for result in run.get("results", []):
            fid = (result.get("fingerprints") or {}).get("invariant")
            if fid and fid in store:
                rec = store[fid]

                props = result.setdefault("properties", {})
                props["status"] = VERDICT_TO_STATUS.get(rec["verdict"], "Undecided")
                comments_list = props.setdefault("comments", [])
                now_ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                comments_list.append({
                    "text": f"[LLM]: {rec['text']}",
                    "createdBy": "LLM",
                    "createTs": now_ts
                })

    out_path = REPORTS_DIR / f"{source_key}_reviewed.sarif"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = out_path.with_suffix('.sarif.tmp')
    try:
        with tmp_path.open("w", encoding="utf-8") as f:
            json.dump(original_data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, out_path)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()
    return {"path": str(out_path), "count": len(store)}


VERDICT_TO_STATUS = {
    "P0": "Undecided",
    "P1": "Undecided",
    "P2": "Undecided",
    "NA": "Not Applicable",
    "FP": "False Positive",
    "Need_analysis": "Undecided"
}
