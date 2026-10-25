# Japan Rail & Water Atlas

**A geographic atlas of Japan's passenger railways, guided transport and scheduled passenger boats.**

Follow the Shinkansen across the country, inspect the parallel tracks around
Shinjuku, or trace the ferries out to Ogasawara. The islands stay where they
belong. Station labels stay readable as you zoom.

**[Explore the live atlas](https://maar10herr.github.io/japan-rail-water-atlas/)** ·
**[Download the single-file map](https://github.com/Maar10Herr/japan-rail-water-atlas/releases/download/v0.1.0/japan-rail-water-atlas.html)** ·
**[Maps & releases](https://github.com/Maar10Herr/japan-rail-water-atlas/releases)**

![Station-level detail in the Japan Rail & Water Atlas](docs/assets/atlas-preview.png)

The cartography comes with receipts: source URLs, inventories, coverage audits
and SHA-256 checksums are included.

## What you can explore

- **JR and Shinkansen**, alongside private and third-sector railways, including
  Hankyu, Kintetsu, Nankai, Meitetsu, Tobu, Seibu and the other mapped operators.
- **Metro, tram, monorail, AGT and maglev** networks, plus funiculars and curated
  public ropeways and lifts.
- **Scheduled water transport** on the sea, lakes and rivers: ferries,
  passenger launches, waterbuses and sightseeing boats, with selectable
  Japan-serving international routes.
- **Japanese and English station search**, including romanized operator aliases.
- **Clickable stations and lines**, with nearby mapped geometry and available
  operator, timetable and OpenStreetMap links.
- **Layer filters, language selection and PNG export**. A separate option shows
  long-term suspensions; another adds live GSI street context.

The project aims for broad nationwide coverage. It does **not** claim that every
passenger service has been individually verified or that the inventory is
literally exhaustive. Geometry uncertainty is represented in the map and
documented in the [coverage notes](docs/COVERAGE.md).

## The network, by the numbers

| Dataset component | Count | What the number means |
| --- | ---: | --- |
| Interactive route groups | 1,846 | Groups of geometry sharing a mode, operator, name and geometry-quality class |
| Source line sections | 96,099 | Mapped geometry sections, including parallel tracks and suspension context |
| Station and terminal objects | 11,251 | Searchable point objects; an interchange can have several |
| Railway stop/station objects in the selected baseline | 9,335 | OSM station/stop objects, not distinct commercial stations |
| Water-service records | 587 | 565 marked active and 22 marked suspended in the assembled inventory |
| MLIT passenger-operator directory entries cross-matched | 204 | Operator-level matches, not independent verification of every route |

**Object counts are not service counts or route-kilometres.** Two parallel
tracks are two pieces of geometry. Two operators at one interchange may be two
station objects. One ferry service may contain several legs.

The input baselines are the Geofabrik/OSM snapshot from **2026-10-24**, MLIT's
**2022** national railway inventory and the upstream ferry inventory from
**2026-09-13**, supplemented by selected operator checks. This is a versioned
dataset, not a live transport feed.

## Using the map

Choose **All Japan** for the national view or one of the regional presets.
Search for a station, port, line or operator in Japanese or English. Selecting
a station zooms to it and shows nearby mapped lines.

Station names appear from zoom 10.5. At zoom 16.7 and above, all visible mapped
station names are allowed to appear. **Show overlapping station names** enables
that behavior sooner. Very close station objects can still overlap; zoom
further or select one to isolate its label. English names fall back to Japanese
where an English value is missing.

Water routes use dashes. Short dashes distinguish approximate, partial or direct
connections from mapped geometry. A hollow diamond identifies a sightseeing
departure whose fixed circuit is unavailable. Grey suspension layers are off
by default.

**Street context** loads pale map tiles from the Geospatial Information Authority
of Japan. Everything needed for the transport map, search and coastline is
already embedded in the page; this optional layer needs internet access.

**Save this view as PNG** exports the current map canvas with source attribution.

## Run locally

The repository includes a ready-to-serve `index.html`. Python's standard library
is enough:

```sh
git clone https://github.com/Maar10Herr/japan-rail-water-atlas.git
cd japan-rail-water-atlas
python3 -m http.server 8000 --bind 127.0.0.1
```

Open [localhost:8000](http://localhost:8000). A current desktop browser with
WebGL support is recommended. The renderer, worker, compressed dataset and
styles are bundled; the core map does not require an account or API key.

## Build and check

Edit the application in `src/`, then rebuild the single-file site:

```sh
python3 tools/build.py
python3 tools/build.py --check
python3 tools/validate.py
node --check src/app.mjs
```

The builder uses Python's standard library and makes no network requests.
`--check` compares the generated bytes with the committed `index.html`.
Validation checks dataset hashes, geometry types, point/search alignment,
counts and station-to-route references. GitHub Actions runs the same checks.

The checked-in payload makes the **web build** reproducible. Re-creating the
national GIS compilation from raw upstream data is a separate operation;
sources change, and several classifications were manually reviewed. See
[methods](docs/METHODS.md) before replacing the data.

## Under the hood

```text
data/atlas.json.gz + src/ + vendor/
                  │
           tools/build.py
                  │
              index.html
                  │
     browser decompression + MapLibre worker
                  │
       GeoJSON → in-browser vector tiles
                  │
         WebGL lines + local-font labels
```

MapLibre tiles the embedded GeoJSON in a worker and renders it with WebGL.
Labels are drawn for the current zoom rather than baked into a national image.
The app uses local fonts, including CJK fallbacks, instead of requiring a remote
glyph service. Map coordinates use WGS84; the interactive projection is Web
Mercator.

The static national export uses Lambert conformal conic with standard parallels
30°N and 46°N and a central meridian of 136°E. Its **36,000 × 44,000** pixels add
up to **1.584 gigapixels**. An uncompressed RGBA buffer at that size is about
**5.9 GiB**. The interactive map is the more convenient way to inspect a station;
the raster is there for the large-format cartography crowd.

## Downloads and data

| Artifact | Location |
| --- | --- |
| Self-contained interactive HTML | [Release download](https://github.com/Maar10Herr/japan-rail-water-atlas/releases/download/v0.1.0/japan-rail-water-atlas.html) |
| 36,000 × 44,000 national PNG | [Release download](https://github.com/Maar10Herr/japan-rail-water-atlas/releases/download/v0.1.0/japan-national-36000x44000.png) |
| Nine 10,000 × 12,600 regional PNGs | [Regional atlas ZIP](https://github.com/Maar10Herr/japan-rail-water-atlas/releases/download/v0.1.0/japan-regional-details.zip) |
| Interactive payload | [`data/atlas.json.gz`](data/atlas.json.gz) |
| Selected line sections as compressed WGS84 GeoJSON | [`data/network.geojson.gz`](data/network.geojson.gz) |
| Ground lines, station/terminal points and water services | [`data/inventories/`](data/inventories/) |
| Historical rail comparison and ferry-operator matching | [`data/audits/`](data/audits/) |
| Snapshot metadata and SHA-256 checksums | [`data/manifest.json`](data/manifest.json) |

The regional sheets cover Tokyo/Kanto, Osaka–Kyoto–Kobe, Nagoya, the Seto Inland
Sea, northern Kyushu, Sapporo/southern Hokkaido, Okinawa/Sakishima, the central
mountains/Fuji/Hakone and Izu/Ogasawara.

To inspect the payload without installing a GIS stack:

```python
import gzip
import json

with gzip.open("data/atlas.json.gz", "rt", encoding="utf-8") as stream:
    atlas = json.load(stream)

print(atlas["count"])
print(atlas["search"][0])  # Original object ID, bilingual name, coordinates, nearby route IDs
```

## What the map does not tell you

The geometry is useful for exploring networks. It is not a timetable, a routing
graph or proof that a particular train calls at a station. Nearby mapped lines
are selected by geographic proximity. A ferry's drawn connection is not a
navigational track.

Some current service states, minor crossings, public lifts and heritage
operations still need better evidence. Of the 565 active water-service records,
104 have no fixed circuit geometry and are represented by departure markers.
The [coverage report](docs/COVERAGE.md) separates that limitation from geometry
and naming quality.

## Sources, attribution and licenses

The principal sources are [OpenStreetMap](https://www.openstreetmap.org/copyright),
[Geofabrik](https://download.geofabrik.de/asia/japan.html),
[MLIT National Land Numerical Information](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N02-v3_1.html),
the [MLIT passenger-operator directory](https://www.mlit.go.jp/maritime/bosai_shipslink.html),
and [kametaro7/japan-ferry-map](https://github.com/kametaro7/japan-ferry-map).
The optional street map is supplied by [GSI Japan](https://maps.gsi.go.jp/development/ichiran.html).
The renderer is [MapLibre GL JS](https://maplibre.org/).

Original application code and documentation are MIT licensed. OSM-derived
data is ODbL; the bundled renderer and other source components retain their
own terms. **The code license does not relicense the data.** Read
[NOTICE.md](NOTICE.md) and [source provenance](docs/SOURCES.md) before reusing it.

Missing a railway, a little crossing, or a better station name? Contributions
with primary-source evidence are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).
