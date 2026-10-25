#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 MH
"""Validate dataset hashes, geometry, counts, and lookup relationships offline."""

from __future__ import annotations

import gzip
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def coordinates(value):
    if value and isinstance(value[0], (float, int)):
        yield value
    else:
        for child in value:
            yield from coordinates(child)


def main() -> None:
    manifest = json.loads((ROOT / "data/manifest.json").read_text(encoding="utf-8"))
    for filename, expected in manifest["files"].items():
        raw = (ROOT / filename).read_bytes()
        require(len(raw) == expected["bytes"], f"Size mismatch: {filename}")
        require(hashlib.sha256(raw).hexdigest() == expected["sha256"], f"Hash mismatch: {filename}")

    data = json.loads(gzip.decompress((ROOT / "data/atlas.json.gz").read_bytes()))
    require(data["count"] == manifest["counts"], "Manifest counts disagree with payload")
    lines, stations = data["lines"]["features"], data["stations"]["features"]
    require(len(lines) == len(data["meta"]) == data["count"]["route_groups"], "Line index mismatch")
    require(len(stations) == len(data["search"]) == data["count"]["station_objects"], "Station index mismatch")

    for i, (feature, metadata) in enumerate(zip(lines, data["meta"])):
        require(feature["id"] == metadata["i"] == i, f"Broken route ID: {i}")
        require(feature["properties"]["m"] in data["modes"], f"Unknown route mode: {i}")
        require(feature["geometry"]["type"] in ("LineString", "MultiLineString"), f"Unexpected geometry: {i}")
        require(bool(metadata["name"]), f"Missing route name: {i}")
        require(bool(metadata.get("source_ids")), f"Missing source identities: {i}")
        require(feature["properties"]["n"] == metadata["name"], f"Route label mismatch: {i}")
        # A generic mode name is a display fallback, not a nationwide route identity.
        if not feature["properties"]["label"]:
            require(len(metadata["source_ids"]) == 1, f"Unrelated unnamed ways grouped together: {i}")
        for lon, lat in coordinates(feature["geometry"]["coordinates"]):
            require(math.isfinite(lon) and math.isfinite(lat), f"Nonfinite coordinate: {i}")
            require(-180 <= lon <= 180 and -90 <= lat <= 90, f"Invalid longitude/latitude: {i}")

    for i, (feature, item) in enumerate(zip(stations, data["search"])):
        require(feature["id"] == item["i"] == i, f"Broken station ID: {i}")
        require(feature["geometry"]["coordinates"] == item["xy"], f"Search point mismatch: {i}")
        require(bool(item["n"]), f"Missing station label: {i}")
        require(feature["properties"]["n"] == item["n"], f"Station label mismatch: {i}")
        require(feature["properties"]["en"] == item["en"], f"Latin label mismatch: {i}")
        require(feature["properties"]["m"] == item["mode"], f"Station mode mismatch: {i}")
        require(all(0 <= rid < len(lines) for rid in item["near"]), f"Broken nearby-line reference: {i}")

    by_id = {item["id"]: item for item in data["search"]}
    require(len(by_id) == len(stations), "Duplicate station source identity")
    review = json.loads((ROOT / "data/reviews/station_coverage.json").read_text(encoding="utf-8"))
    rope_review = json.loads((ROOT / "data/reviews/ropeway_selection.json").read_text(encoding="utf-8"))
    selected_way_ids = {wid for metadata in data["meta"] for wid in metadata["source_ids"]}
    for rejected in review["remove_stations"] + rope_review["corrections"]:
        require(rejected["id"] not in by_id, f"Excluded nonpublic/inactive stop reappeared: {rejected['id']}")
    for restored in review["add_stations"]:
        require(restored["id"] in by_id, f"Verified passenger station missing: {restored['id']}")
        require(by_id[restored["id"]]["near"], f"Restored station lacks line context: {restored['id']}")
    for rejected in review["remove_ways"]:
        require(rejected["id"] not in selected_way_ids, f"Amusement/works alignment reappeared: {rejected['id']}")
    for restored in review["add_ways"]:
        require(restored["id"] in selected_way_ids, f"Verified passenger alignment missing: {restored['id']}")
    for modified in review["update_ways"]:
        if modified.get("mode") == "rail_suspended":
            require(all(item["mode"] == "rail_suspended" for item in data["meta"] if modified["id"] in item["source_ids"]), f"Suspended alignment shown as active: {modified['id']}")

    # The actual nine-station Linimo service must survive guideway filtering.
    linimo_names = {"藤が丘", "はなみずき通", "杁ヶ池公園", "長久手古戦場", "芸大通", "公園西", "愛・地球博記念公園", "陶磁資料館南", "八草"}
    visible_linimo = {item["n"] for item in data["search"] if item["mode"] == "guideway" and 137 <= item["xy"][0] <= 137.12 and 35.16 <= item["xy"][1] <= 35.20}
    require(linimo_names <= visible_linimo, "Operating Linimo stations are missing from the guideway layer")

    print(f"Validated {len(lines):,} route groups and {len(stations):,} station/terminal objects")
    print(f"Verified {len(manifest['files'])} data files against SHA-256 manifest")


if __name__ == "__main__":
    main()
