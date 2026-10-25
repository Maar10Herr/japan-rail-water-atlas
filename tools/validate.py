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


def validate_history_geometry(geometry: dict, identity: str) -> None:
    """Validate the Point/line subset used by the historical source datasets."""
    kind = geometry.get("type")
    values = geometry.get("coordinates")
    require(kind in ("Point", "LineString", "MultiLineString"), f"Unexpected historical geometry: {identity}")
    require(isinstance(values, list) and bool(values), f"Empty historical geometry: {identity}")
    parts = [values] if kind == "LineString" else (values if kind == "MultiLineString" else [])
    for part in parts:
        require(isinstance(part, list) and len(part) >= 2, f"Historical line has fewer than two vertices: {identity}")
        require(len({tuple(point) for point in part}) >= 2, f"Historical line has zero length: {identity}")
    for point in ([values] if kind == "Point" else [point for part in parts for point in part]):
        require(isinstance(point, list) and len(point) == 2, f"Invalid historical coordinate dimensions: {identity}")
        lon, lat = point
        require(all(isinstance(value, (float, int)) and not isinstance(value, bool) and math.isfinite(value) for value in point), f"Nonfinite historical coordinate: {identity}")
        require(-180 <= lon <= 180 and -90 <= lat <= 90, f"Invalid historical longitude/latitude: {identity}")


def validate_history(data: dict) -> tuple[int, int, int]:
    history = json.loads(gzip.decompress((ROOT / "data/history.json.gz").read_bytes()))
    require(history["schema_version"] == 1, "Unsupported historical dataset schema")
    lines = history["lines"]["features"]
    points = history["points"]["features"]
    records = history["records"]
    counts = history["count"]
    require(history["lines"]["type"] == history["points"]["type"] == "FeatureCollection", "Invalid historical feature collections")
    require(len(lines) + len(points) == len(records), "Historical geometry/record count mismatch")
    require(len({item["id"] for item in records}) == len(records), "Duplicate historical record identity")
    require(counts["line_features"] == len(lines), "Historical line count must count geometry features")
    require("route_groups" not in counts and "routes" not in counts, "Historical feature counts must not be presented as route counts")
    require(counts["station_objects"] == sum(item["kind"] == "station" for item in records), "Historical station-object count mismatch")
    require(counts["site_objects"] == sum(item["kind"] == "site" for item in records), "Historical site-object count mismatch")
    require(len(points) == counts["station_objects"] + counts["site_objects"], "Historical point-kind count mismatch")

    by_source_id = {}
    for i, (feature, record) in enumerate(zip(lines + points, records)):
        props = feature["properties"]
        require(feature["type"] == "Feature", f"Invalid historical feature: {i}")
        require(record["i"] == feature["id"] == props["i"] == i, f"Broken historical record index: {i}")
        require(record["kind"] in ("line", "station", "site"), f"Unknown historical record kind: {i}")
        require(props["kind"] == record["kind"], f"Historical feature-kind mismatch: {i}")
        fallback = "Unnamed former railway" if record["kind"] == "line" else "Unnamed former station"
        require((props["n"] == record["name"] or (not props["n"] and not props["label"] and record["name"] == fallback)) and props["en"] == record["en"], f"Historical label mismatch: {i}")
        require(props["q"] == record["geometry_quality"], f"Historical quality mismatch: {i}")
        validate_history_geometry(feature["geometry"], record["id"])
        if i < len(lines):
            require(record["kind"] == "line" and feature["geometry"]["type"] in ("LineString", "MultiLineString"), f"Historical line record has point geometry: {i}")
        else:
            require(record["kind"] in ("station", "site") and feature["geometry"]["type"] == "Point", f"Historical point record has line geometry: {i}")
            require(record["xy"] == feature["geometry"]["coordinates"], f"Historical lookup coordinates disagree: {i}")
        require(bool(record["name"]), f"Missing historical display name: {i}")
        require(bool(record["license"]) and bool(record["credit"]), f"Missing historical license/credit: {i}")
        require(bool(record["source_urls"]) and all(url.startswith("https://") for url in record["source_urls"]), f"Missing historical source links: {i}")
        require(bool(record["source_component"]) and bool(record["source_ids"]), f"Missing historical source identity: {i}")
        for identity in record["source_ids"]:
            by_source_id.setdefault(identity, []).append(record)
        for date in record["dates"]:
            require(all(isinstance(date.get(key), str) and date[key].strip() for key in ("label", "value", "scope")), f"Historical date lacks an explicit scope: {i}")

    approximate = [record for record in records if record["kind"] == "line" and record["geometry_quality"] == "approximate"]
    require(len(approximate) == counts["approximate_line_features"] == 7, "Expected seven explicitly approximate Daito line features")
    require(all(record.get("positional_uncertainty_m", 0) >= 1000 for record in approximate), "Approximate sugar-railway lines need at least 1 km positional uncertainty")
    require(all(record["id"].startswith("sugar-daito-") for record in approximate), "Unexpected approximate line identity")
    for record in approximate:
        require(any(date["label"] == "Network closure" and date["value"] == "1983" and "Network-level" in date["scope"] for date in record["dates"]), f"Daito closure date lost its network-level scope: {record['id']}")
    miyako = [record for record in records if any(identity.startswith("sugar-miyako-") for identity in record["source_ids"])]
    require(len(miyako) == 1 and miyako[0]["id"] == "sugar-miyako-factory-site", "Miyako must remain a single documented railway-site point")
    require(miyako[0]["kind"] == "site" and miyako[0]["geometry_quality"] == "site_only", "Miyako railway site must not become an invented line or station")
    kitadaito = [record for record in records if record["source_component"] == "kitadaito"]
    require(len(kitadaito) == 1 and kitadaito[0]["id"] == "industrial-kitadaito-phosphate-site" and kitadaito[0]["kind"] == "site" and kitadaito[0]["geometry_quality"] == "site_only", "Kitadaito must remain a documented industrial-site point")
    hokkaido_stations = [record for record in records if record["kind"] == "station" and 139 <= record["xy"][0] <= 146 and 41.3 <= record["xy"][1] <= 46 and (record["xy"][0] <= 140.6 or record["xy"][1] >= 41.65)]
    # The source-specific floor also protects coverage independently of the
    # geographic count, whose southern cut excludes Shimokita across the strait.
    hokkaido_source_stations = [record for record in records if record["kind"] == "station" and record["source_component"] == "naebo_hokkaido"]
    require(len(hokkaido_stations) == counts["hokkaido_station_objects"] and len(hokkaido_source_stations) >= 740, "Hokkaido historical station coverage regressed")

    conflicts = json.loads((ROOT / "data/history/current-history-conflicts.json").read_text(encoding="utf-8"))
    for identity in conflicts["exclude_history_osm_ids"]:
        require(identity not in by_source_id and "osm-history-" + identity not in by_source_id, f"Suspended/active infrastructure reappeared in history: {identity}")
    active_ids = {item["id"] for item in data["search"]}
    require("n265927763" not in active_ids, "Relocated Kawamura station remains in the current layer")
    require("n14203032905" in active_ids, "Operating Sagara-Toshima replacement station is missing")
    old_kawamura = by_source_id.get("osm-history-n265927763", [])
    require(len(old_kawamura) == 1 and old_kawamura[0]["kind"] == "station", "Former Kawamura location is missing from history")
    require(any(date["value"] == "2026-09-20" and "relocation" in date["scope"] for date in old_kawamura[0]["dates"]), "Kawamura relocation date lacks its correct scope")

    require("no simultaneous-network claim" in history["period_policy"], "Historical layer must distinguish all-era coverage from a simultaneous network")
    for key in ("osm", "naeboworks", "ohm", "sugar_diagram"):
        source = history["sources"][key]
        require(bool(source["license"]) and source["url"].startswith("https://"), f"Missing historical source license link: {key}")
    for url in ("https://creativecommons.org/licenses/by/4.0/", "https://creativecommons.org/licenses/by/3.0/", "https://www.openhistoricalmap.org/copyright"):
        require(url in history["attribution_html"], f"Missing historical attribution link: {url}")
    require(all(credit in history["attribution_text"] for credit in ("苗穂工房", "Tamurono157", "OpenHistoricalMap", "OSM", "ODbL")), "Historical export credits are incomplete")

    # Keep the published web layer tied to inspectable source geometry and audits.
    for filename in ("naeboworks-hokkaido.geojson.gz", "naeboworks-regions.geojson.gz", "osm.geojson.gz", "ohm.geojson.gz", "okinawa-sugar.geojson.gz", "kitadaito-site.geojson"):
        path = ROOT / "data/history" / filename
        require(path.is_file(), f"Missing historical source input: {filename}")
        source_data = json.loads(gzip.decompress(path.read_bytes()) if path.suffix == ".gz" else path.read_bytes())
        require(source_data["type"] == "FeatureCollection" and bool(source_data["features"]), f"Empty historical source input: {filename}")
        for feature in source_data["features"]:
            validate_history_geometry(feature["geometry"], filename)
    for filename in ("naeboworks-hokkaido-provenance.json", "naeboworks-regions-provenance.json", "osm-provenance.json", "ohm-provenance.json", "okinawa-sugar-provenance.json", "current-history-conflicts.json", "excluded-source-decision.json", "integration-audit.json"):
        path = ROOT / "data/history" / filename
        require(path.is_file(), f"Missing historical provenance or audit: {filename}")
        json.loads(path.read_text(encoding="utf-8"))
    audit = json.loads((ROOT / "data/history/integration-audit.json").read_text(encoding="utf-8"))
    require(audit["counts"] == counts, "Historical integration-audit counts disagree with payload")
    return len(lines), counts["station_objects"], counts["site_objects"]


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

    history_lines, history_stations, history_sites = validate_history(data)
    print(f"Validated {len(lines):,} route groups and {len(stations):,} station/terminal objects")
    print(f"Validated {history_lines:,} historical line features, {history_stations:,} former station objects and {history_sites:,} railway sites")
    print(f"Verified {len(manifest['files'])} data files against SHA-256 manifest")


if __name__ == "__main__":
    main()
