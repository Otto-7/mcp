from dataclasses import dataclass, field


@dataclass
class Comment:
    text: str
    created_by: str = ""
    created_ts: str = ""


@dataclass
class TraceStep:
    file: str
    line: int
    message: str


@dataclass
class Rule:
    rule_id: str
    name: str = ""
    description: str = ""
    severity: str = "Unknown"
    reliability: str = ""
    cwe: list = field(default_factory=list)


@dataclass
class Finding:
    finding_id: str
    file: str
    line: int
    level: str
    severity: str
    status: str | None
    message: str
    rule_id: str
    comments: list[Comment] = field(default_factory=list)
    trace: list[TraceStep] = field(default_factory=list)
