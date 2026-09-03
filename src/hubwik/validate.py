from __future__ import annotations

from hubwik.compile import compile_all
from hubwik.load import load_workspace
from hubwik.paths import repo_root
from hubwik.secrets import scan_tree

REQUIRED_CROP = (
    "crop_id",
    "handle",
    "crop_name",
    "latin",
    "sow",
    "harvest",
    "flavour",
    "claim_provenance",
    "status",
)


def validate(root=None, profile_id: str = "thh") -> list[str]:
    root = root or repo_root()
    errors: list[str] = []
    workspace = load_workspace(root, profile_id)
    profile = workspace["profile"]
    handles = set(workspace["crops_by_handle"])
    if len(profile["knowledge_catalogue"]) != 18:
        errors.append(f"catalogue must be 18, got {len(profile['knowledge_catalogue'])}")
    if len(profile["four_by_four"]) != 16:
        errors.append(f"four_by_four must be 16, got {len(profile['four_by_four'])}")
    if len(profile["three_by_four"]) != 12:
        errors.append(f"three_by_four must be 12, got {len(profile['three_by_four'])}")
    if set(profile["four_by_four"]) & {"dill", "pea"}:
        errors.append("dill and pea are not verified in Four by Four")
    if set(profile["three_by_four"]) - set(profile["four_by_four"]):
        errors.append("Three by Four membership must be a subset of Four by Four")
    if set(profile["four_by_four"]) - set(profile["knowledge_catalogue"]):
        errors.append("Four by Four membership must be a subset of the catalogue")
    for handle in profile["knowledge_catalogue"]:
        if handle not in handles:
            errors.append(f"missing crop for catalogue handle {handle}")
    seen_ids = set()
    for crop in workspace["crops"]:
        cid = crop.get("crop_id")
        if cid in seen_ids:
            errors.append(f"duplicate crop_id {cid}")
        seen_ids.add(cid)
        for field in REQUIRED_CROP:
            if crop.get(field) in (None, ""):
                errors.append(f"{crop.get('handle')}: missing {field}")
        flavour = str(crop.get("flavour") or "")
        if flavour.endswith(("more", "slig", "whol")):
            errors.append(f"{crop.get('handle')}: flavour looks truncated: {flavour!r}")
        source = str(crop.get("source") or "")
        if any(token in source.lower() for token in ("truncat", "yield empty", "not verified")):
            errors.append(f"{crop.get('handle')}: source field still holds a reconciliation note")
        ymin, ymax = crop.get("yield_min_g"), crop.get("yield_max_g")
        if ymin not in (None, "") and ymax not in (None, "") and ymin > ymax:
            errors.append(f"{crop.get('handle')}: yield_min_g > yield_max_g")
        if crop.get("status") == "complete":
            for field in ("yield_min_g", "yield_max_g", "germination_days_min", "germination_days_max"):
                if crop.get(field) in (None, ""):
                    errors.append(f"{crop.get('handle')}: complete crop missing {field}")
    try:
        compiled = compile_all(root, profile_id)
    except Exception as exc:
        errors.append(f"compile failed: {exc}")
        return errors
    for rec in compiled["rooms"]:
        if rec["kind"] == "seed" and not rec.get("flavour"):
            errors.append(f"{rec['handle']}: empty flavour")
        if ("vault" + " snapshot") in rec["article"].lower():
            errors.append(f"{rec['handle']}: article still has a reconciliation note")
        types = {obj.get("@type") for obj in rec["ld_objects"]}
        if rec["kind"] == "seed" and "HowTo" not in types:
            errors.append(f"{rec['handle']}: seed page missing HowTo JSON-LD")
        if "Article" not in types:
            errors.append(f"{rec['handle']}: missing Article JSON-LD")
    errors.extend(scan_tree(root))
    return errors
