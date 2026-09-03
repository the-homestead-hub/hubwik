from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "pyproject.toml").exists() and (parent / "data" / "crops").exists():
            return parent
    raise RuntimeError("cannot locate HubWīk repository root")


def data_dir(root: Path | None = None) -> Path:
    return (root or repo_root()) / "data"


def content_dir(root: Path | None = None) -> Path:
    return (root or repo_root()) / "content"


def dist_dir(root: Path | None = None) -> Path:
    return (root or repo_root()) / "dist"
