# Contributing

Useful contributions include a missing passenger line, a closure, an operator
correction, better geometry, an English station name, or a reproducible UI bug.

For a data correction, include:

1. The line, station or service name in Japanese where possible.
2. An official operator, municipality or transport-bureau source.
3. The relevant OSM object or coordinates.
4. Whether the issue concerns geometry, service status, naming or classification.

Please distinguish a seasonal timetable from a long-term suspension, a freight
line from a mixed passenger/freight line, and a departure point from a published
sightseeing circuit. An old rail alignment is not evidence of an active service.

Edit application code in `src/`, then regenerate the checked-in single-file site:

```sh
python3 tools/build.py
python3 tools/build.py --check
python3 tools/validate.py
node --check src/app.mjs
```

For data changes, update the relevant payload, CSV inventory, audit evidence and
SHA-256 manifest together. Route IDs and station IDs are array indexes; changing
their order requires updating all cross-references. Avoid committing raw PBFs,
temporary extraction caches, credentials, personal filesystem paths or giant
rendered images. Exported maps belong in release assets.

Preserve upstream attribution. Do not copy geometry from proprietary railway
maps or infer an exact ferry track from a timetable alone.
