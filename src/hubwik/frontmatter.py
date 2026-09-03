from __future__ import annotations

import json
import re
from pathlib import Path


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _coerce(value: str):
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    if value in {"true", "false"}:
        return value == "true"
    if value in {"null", "~"}:
        return None
    return value


def parse_document(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n?", text, flags=re.S)
    if not match:
        return {}, text
    raw = match.group(1).strip()
    body = text[match.end() :]
    if raw.startswith("{") or raw.startswith("["):
        meta = json.loads(raw)
        if not isinstance(meta, dict):
            raise ValueError("frontmatter JSON must be an object")
        return meta, body
    return _parse_simple_yaml(raw), body


def parse_path(path: Path) -> tuple[dict, str]:
    return parse_document(path.read_text(encoding="utf-8"))


def _parse_simple_yaml(raw: str) -> dict:
    data: dict = {}
    lines = raw.splitlines()
    i = 0
    n = len(lines)

    def indent(line: str) -> int:
        return len(line) - len(line.lstrip(" "))

    while i < n:
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if indent(line) != 0 or ":" not in line or line.lstrip().startswith("-"):
            i += 1
            continue
        key, rest = line.split(":", 1)
        key = key.strip()
        rest = rest.strip()
        if rest.startswith("[") and rest.endswith("]"):
            inner = rest[1:-1].strip()
            data[key] = [_unquote(part) for part in inner.split(",") if part.strip()]
            i += 1
            continue
        if rest:
            data[key] = _coerce(_unquote(rest))
            i += 1
            continue
        i += 1
        items: list = []
        strings: list[str] = []
        saw_map = False
        while i < n:
            ln = lines[i]
            if not ln.strip() or ln.lstrip().startswith("#"):
                i += 1
                continue
            if indent(ln) == 0:
                break
            if ln.lstrip().startswith("-"):
                payload = ln.lstrip()[1:].strip()
                i += 1
                if payload and ":" not in payload:
                    strings.append(_unquote(payload))
                    continue
                item: dict = {}
                saw_map = True
                if payload and ":" in payload:
                    item_key, item_val = payload.split(":", 1)
                    item[item_key.strip()] = _coerce(_unquote(item_val))
                while i < n:
                    sub = lines[i]
                    if not sub.strip():
                        i += 1
                        continue
                    if indent(sub) == 0 or sub.lstrip().startswith("-"):
                        break
                    if ":" in sub:
                        sub_key, sub_val = sub.split(":", 1)
                        item[sub_key.strip()] = _coerce(_unquote(sub_val))
                    i += 1
                items.append(item)
            else:
                i += 1
        data[key] = strings if strings and not saw_map else items
    return data
