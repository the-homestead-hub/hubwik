from __future__ import annotations

import argparse
import json
import sys

from hubwik.compile import write_dist
from hubwik.paths import repo_root
from hubwik.validate import validate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="hubwik", description="Compile HubWīk records to cite-face output.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    build = sub.add_parser("build", help="write dist/")
    build.add_argument("--profile", default="thh")
    check = sub.add_parser("check", help="validate records, licences boundary, and a clean compile")
    check.add_argument("--profile", default="thh")
    args = parser.parse_args(argv)
    root = repo_root()
    if args.cmd == "check":
        errors = validate(root, args.profile)
        if errors:
            print("hubwik check failed:", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
            return 1
        print("hubwik check: ok")
        return 0
    compiled = write_dist(root, args.profile)
    print(json.dumps({
        "crops": len(compiled["workspace"]["crops"]),
        "rooms": len(compiled["rooms"]),
        "ontology": compiled["profile"]["ontology"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
