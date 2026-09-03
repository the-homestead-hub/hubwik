from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from hubwik.paths import repo_root
from hubwik.secrets import scan_tree


class SecretTests(unittest.TestCase):
    def test_tree_is_clean(self) -> None:
        hits = scan_tree(repo_root())
        self.assertEqual(hits, [], msg="\n".join(hits))

    def test_scan_catches_merchant_shapes(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "leak.md").write_text(
                "gid://" + "shopify/" + "Product/1 and " + "my" + "shopify" + ".com\n",
                encoding="utf-8",
            )
            hits = scan_tree(root)
            self.assertTrue(hits)

    def test_scan_catches_private_path(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "note.md").write_text("path /Users/" + "someone/vault\n", encoding="utf-8")
            hits = scan_tree(root)
            self.assertTrue(any("Users" in hit for hit in hits))


if __name__ == "__main__":
    unittest.main()
