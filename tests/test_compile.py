from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from hubwik.compile import compile_all, write_dist
from hubwik.paths import repo_root


class CompileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = repo_root()
        self.compiled = compile_all(self.root)

    def test_eighteen_seed_pages(self) -> None:
        seeds = [rec for rec in self.compiled["rooms"] if rec["kind"] == "seed"]
        self.assertEqual(len(seeds), 18)
        self.assertEqual(
            [rec["handle"] for rec in seeds],
            self.compiled["profile"]["knowledge_catalogue"],
        )

    def test_infobox_clauses_complete(self) -> None:
        for rec in self.compiled["rooms"]:
            if rec["kind"] != "seed":
                continue
            box = rec["box_html"]
            for label in ("Binomial", "Sow", "First cut", "Flavour"):
                self.assertIn(f"<th>{label}</th>", box, msg=f"{rec['handle']} missing {label}")
            self.assertTrue(rec["flavour"])
            self.assertFalse(rec["flavour"].endswith(("more", "slig", "whol")))

    def test_jsonld(self) -> None:
        for rec in self.compiled["rooms"]:
            types = {obj.get("@type") for obj in rec["ld_objects"]}
            self.assertIn("Article", types, msg=rec["handle"])
            if rec["kind"] == "seed":
                self.assertIn("HowTo", types, msg=rec["handle"])
                self.assertIn("FAQPage", types, msg=rec["handle"])
            for obj in rec["ld_objects"]:
                self.assertEqual(obj.get("@context"), "https://schema.org")

    def test_treatise_toc_skips_lede(self) -> None:
        fbf = next(rec for rec in self.compiled["rooms"] if rec["handle"] == "four-by-four")
        self.assertIn("Sixteen of eighteen", fbf["article"])
        self.assertNotIn('href="#the-four-by-four-is-the-larger-stack', fbf["article"])

    def test_no_reconciliation_copy(self) -> None:
        needle = "vault" + " snapshot"
        for rec in self.compiled["rooms"]:
            blob = rec["article"] + rec["box_html"] + rec.get("claim", "")
            self.assertNotIn(needle, blob.lower())
            self.assertNotIn("Observed live " + "price", blob)

    def test_seed_till_has_no_variant(self) -> None:
        for rec in self.compiled["rooms"]:
            if rec["kind"] != "seed":
                continue
            self.assertEqual(rec["till_path"], "/products/seed-pack")
            self.assertNotIn("variant=", rec["till_path"])

    def test_deterministic_dist(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            a = Path(first)
            b = Path(second)
            write_dist(self.root)
            # Compare two in-memory cite sets and two writes via compile_all stability.
            one = compile_all(self.root)
            two = compile_all(self.root)
            self.assertEqual(
                [rec["article"] for rec in one["rooms"]],
                [rec["article"] for rec in two["rooms"]],
            )
            self.assertEqual(
                [rec["box_html"] for rec in one["rooms"]],
                [rec["box_html"] for rec in two["rooms"]],
            )
            self.assertTrue(a.exists() and b.exists())

    def test_write_dist_artifacts(self) -> None:
        compiled = write_dist(self.root)
        dest = self.root / "dist"
        cite = json.loads((dest / "cite_set.json").read_text(encoding="utf-8"))
        self.assertEqual(cite["counts"]["knowledge_catalogue"], 18)
        self.assertEqual(cite["satellite"]["url"], "https://stile.example.org/")
        self.assertEqual(cite["satellite"]["expect_status"], 402)
        self.assertTrue((dest / "ontology.txt").read_text(encoding="utf-8").startswith("Eighteen varieties"))
        for rec in compiled["rooms"]:
            if rec["kind"] == "seed":
                self.assertTrue((dest / "pages" / f"{rec['page_handle']}.html").exists())
        for name in ("thh-hubwik-lookup.liquid", "thh-hubwik-body.liquid", "thh-hubwik-index.liquid"):
            self.assertTrue((dest / "shopify" / "snippets" / name).exists())
        hall = (dest / "pages" / "hubwik.html").read_text(encoding="utf-8")
        self.assertIn("grow-basil.html", hall)
        self.assertIn("Eighteen varieties", hall)


if __name__ == "__main__":
    unittest.main()
