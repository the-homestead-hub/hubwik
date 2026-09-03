from __future__ import annotations

import json
import unittest
from pathlib import Path

from hubwik.load import load_workspace
from hubwik.paths import repo_root
from hubwik.validate import REQUIRED_CROP, validate


class SchemaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = repo_root()
        self.workspace = load_workspace(self.root)

    def test_schema_files_are_objects(self) -> None:
        for name in ("crop.schema.json", "observation.schema.json"):
            path = self.root / "data" / "schema" / name
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data.get("type"), "object")
            self.assertIn("required", data)

    def test_observation_schema_keeps_partner_internal(self) -> None:
        data = json.loads(
            (self.root / "data" / "schema" / "observation.schema.json").read_text(encoding="utf-8")
        )
        self.assertNotIn("partner_id", data["required"])
        self.assertIn("Never print", data["properties"]["partner_id"]["description"])

    def test_crop_required_fields(self) -> None:
        for crop in self.workspace["crops"]:
            for field in REQUIRED_CROP:
                self.assertTrue(crop.get(field), msg=f"{crop.get('handle')} missing {field}")

    def test_ids_and_handles(self) -> None:
        seen = set()
        for crop in self.workspace["crops"]:
            cid = crop["crop_id"]
            handle = crop["handle"]
            self.assertRegex(cid, r"^[a-z][a-z0-9_]*$")
            self.assertRegex(handle, r"^[a-z][a-z0-9-]*$")
            self.assertEqual(cid, handle.replace("-", "_"))
            self.assertNotIn(cid, seen)
            seen.add(cid)

    def test_units_and_ranges(self) -> None:
        for crop in self.workspace["crops"]:
            ymin, ymax = crop.get("yield_min_g"), crop.get("yield_max_g")
            if ymin not in (None, "") and ymax not in (None, ""):
                self.assertLessEqual(ymin, ymax, msg=crop["handle"])
            gmin, gmax = crop.get("germination_days_min"), crop.get("germination_days_max")
            if gmin not in (None, "") and gmax not in (None, ""):
                self.assertLessEqual(gmin, gmax, msg=crop["handle"])
            flavour = crop["flavour"]
            self.assertGreaterEqual(len(flavour), 8, msg=crop["handle"])
            self.assertFalse(flavour.endswith(("more", "slig", "whol")))

    def test_source_metadata(self) -> None:
        allowed = {
            "thh_observation",
            "thh_trial",
            "supplier_spec",
            "horticultural_consensus",
            "external_study",
            "working_recommendation",
            "live_treatise",
        }
        for crop in self.workspace["crops"]:
            self.assertIn(crop["claim_provenance"], allowed)
            source = str(crop.get("source") or "")
            self.assertNotIn("truncat", source.lower())
            self.assertNotIn("yield empty", source.lower())

    def test_profile_membership(self) -> None:
        profile = self.workspace["profile"]
        self.assertEqual(len(profile["knowledge_catalogue"]), 18)
        self.assertEqual(len(profile["four_by_four"]), 16)
        self.assertEqual(len(profile["three_by_four"]), 12)
        self.assertTrue(set(profile["three_by_four"]) <= set(profile["four_by_four"]))
        self.assertTrue(set(profile["four_by_four"]) <= set(profile["knowledge_catalogue"]))
        self.assertEqual(set(profile["knowledge_catalogue"]) - set(profile["four_by_four"]), {"dill", "pea"})
        for handle in profile["knowledge_catalogue"]:
            self.assertIn(handle, self.workspace["crops_by_handle"])

    def test_validate_clean(self) -> None:
        self.assertEqual(validate(self.root), [])


if __name__ == "__main__":
    unittest.main()
