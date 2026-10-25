#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 MH
"""Build the self-contained atlas from checked-in inputs. No network or packages."""

from __future__ import annotations

import argparse
import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build() -> bytes:
    template = (ROOT / "src/template.html").read_text(encoding="utf-8")
    inputs = {
        "MAP_CSS": ("vendor/maplibre-gl.css", False),
        "MAP_CODE": ("vendor/maplibre-gl.mjs", True),
        "WORKER_CODE": ("vendor/maplibre-gl-worker.mjs", True),
        "MAP_DATA": ("data/atlas.json.gz", True),
        "HISTORY_CODE": ("src/history.mjs", True),
        "HISTORY_DATA": ("data/history.json.gz", True),
        "APP_CODE": ("src/app.mjs", False),
        "APP_LICENSE": ("LICENSE", False),
        "DEPENDENCY_LICENSES": ("LICENSES/Renderer-Dependencies.md", False),
    }
    for token, (filename, encoded) in inputs.items():
        contents = (ROOT / filename).read_bytes()
        replacement = (
            base64.b64encode(contents).decode("ascii")
            if encoded else contents.decode("utf-8")
        )
        placeholder = f"__{token}__"
        if template.count(placeholder) != 1:
            raise ValueError(f"Expected exactly one {placeholder}")
        template = template.replace(placeholder, replacement)
    return template.encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "index.html")
    parser.add_argument("--check", action="store_true", help="Check the committed build")
    args = parser.parse_args()
    generated = build()
    if args.check:
        if not args.output.exists() or args.output.read_bytes() != generated:
            raise SystemExit("Build is stale. Run: python3 tools/build.py")
        print(f"Build matches checked-in inputs ({len(generated):,} bytes)")
    else:
        args.output.write_bytes(generated)
        print(f"Built {args.output.name} ({len(generated):,} bytes)")


if __name__ == "__main__":
    main()
