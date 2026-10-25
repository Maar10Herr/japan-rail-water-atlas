#!/usr/bin/env python3
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
        for lon, lat in coordinates(feature["geometry"]["coordinates"]):
            require(math.isfinite(lon) and math.isfinite(lat), f"Nonfinite coordinate: {i}")
            require(-180 <= lon <= 180 and -90 <= lat <= 90, f"Invalid longitude/latitude: {i}")

    for i, (feature, item) in enumerate(zip(stations, data["search"])):
        require(feature["id"] == item["i"] == i, f"Broken station ID: {i}")
        require(feature["geometry"]["coordinates"] == item["xy"], f"Search point mismatch: {i}")
        require(bool(item["n"]), f"Missing station label: {i}")
        require(all(0 <= rid < len(lines) for rid in item["near"]), f"Broken nearby-line reference: {i}")

    print(f"Validated {len(lines):,} route groups and {len(stations):,} station/terminal objects")
    print(f"Verified {len(manifest['files'])} data files against SHA-256 manifest")


if __name__ == "__main__":
    main()
