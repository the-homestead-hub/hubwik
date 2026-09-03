from __future__ import annotations

import re
from pathlib import Path


def _join(*parts: str) -> str:
    return "".join(parts)


# Patterns are assembled so this file does not itself contain merchant tokens.
FORBIDDEN = (
    re.compile(r"shpat_[0-9a-zA-Z]+"),
    re.compile(r"shpca_[0-9a-zA-Z]+"),
    re.compile(r"shpss_[0-9a-zA-Z]+"),
    re.compile(_join("gid://", "shopify/", r"(Product|ProductVariant)/") + r"\d+"),
    re.compile(_join("gq", "2ktw", "-cj")),
    re.compile(_join("my", "shopify", r"\.com")),
    re.compile(r"account_id\"?\s*[:=]\s*\"[0-9a-f]{32}\""),
    re.compile(r"/Users/[A-Za-z0-9._-]+"),
    re.compile(_join("vault", " snapshot"), re.I),
    re.compile(_join("Observed live ", "price on 20") + r"\d\d"),
    re.compile(_join("THH-CON-", "SEED-")),
    re.compile(_join("BAS", "25-01")),
    re.compile(_join("204980", "453708")),
    re.compile(_join("200610", "414924")),
    re.compile(_join("f9bca67ea215", "7109ddc493b5d865fd12")),
    re.compile(_join("Auk", " Mini")),
)

SKIP_DIRS = {".git", ".venv", "dist", "__pycache__", "LICENSES", ".pytest_cache"}
SKIP_NAMES = {"docs/BOUNDARY.md"}


def scan_tree(root: Path) -> list[str]:
    hits: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        rel = path.relative_to(root).as_posix()
        if rel in SKIP_NAMES or rel.endswith(".png") or rel.endswith(".jpg"):
            continue
        if path.suffix not in {".md", ".py", ".json", ".jsonc", ".js", ".liquid", ".css", ".yml", ".yaml", ".toml", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in FORBIDDEN:
            if pattern.search(text):
                hits.append(f"{rel}: {pattern.pattern}")
    return hits
