from __future__ import annotations

import json
from pathlib import Path

from hubwik.frontmatter import parse_path
from hubwik.paths import content_dir, data_dir, repo_root


def load_profile(root: Path | None = None, profile_id: str = "thh") -> dict:
    path = data_dir(root) / "profiles" / f"{profile_id}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def load_crops(root: Path | None = None) -> list[dict]:
    crops = []
    for path in sorted((data_dir(root) / "crops").glob("*.md")):
        meta, body = parse_path(path)
        meta["_path"] = path.as_posix()
        meta["_body"] = body
        crops.append(meta)
    return crops


def load_treatises(root: Path | None = None) -> list[dict]:
    treatises = []
    for path in sorted((content_dir(root) / "treatises").glob("*.md")):
        meta, body = parse_path(path)
        meta["_path"] = path.as_posix()
        meta["_body"] = body
        treatises.append(meta)
    return treatises


def crop_by_handle(crops: list[dict]) -> dict[str, dict]:
    return {str(crop["handle"]): crop for crop in crops}


def load_workspace(root: Path | None = None, profile_id: str = "thh") -> dict:
    root = root or repo_root()
    crops = load_crops(root)
    return {
        "root": root,
        "profile": load_profile(root, profile_id),
        "crops": crops,
        "crops_by_handle": crop_by_handle(crops),
        "treatises": load_treatises(root),
    }
