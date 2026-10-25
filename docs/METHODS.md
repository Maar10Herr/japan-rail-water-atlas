# From infrastructure to a browser atlas

## 1. Acquire geometry and reference inventories

The primary geometry is a Geofabrik Japan OSM PBF with replication timestamp
`2026-10-24T20:20:51Z`. The MLIT N02 2022 rail sections and station inventory
provide an independent historical comparison. The water-service checklist
starts with `kametaro7/japan-ferry-map` and is supplemented by selected
official-operator checks.

An existing-map search preceded compilation. AllRailMap was the closest
discovered rail-plus-ferry reference. Railmap.jp documents exclusions of
ropeways/lifts. None of the inspected maps established the entire requested
passenger ground-and-water scope in one verified export. Their original
cartography was not copied. See [source references](SOURCES.md).

## 2. Extract without caching every OSM node

The original compilation used pyosmium to select rail/aerialway/ferry ways,
route relations, station/terminal objects, coastlines and major lake boundaries.
It stored tags, memberships and node IDs in SQLite, then made a second pass
for the coordinates needed by the selected ways.

That pass retained 3,761,373 coordinate nodes, with no missing selected node
coordinates. Sorted IDs and coordinate arrays allowed bounded-memory lookup
without building an all-Japan node-location cache.

## 3. Select passenger infrastructure

Selection uses positive passenger evidence: passenger route membership,
passenger or mixed traffic tags, active main/branch line tags, known passenger
operators and inventory comparison. Freight-only infrastructure, yards,
sidings and inactive/proposed infrastructure are filtered separately.

OSM route membership alone is insufficient. A through-running service can
traverse several operators and transport classes. The mapped infrastructure
operator takes precedence over a service relation containing the word
“subway”. Some historical and operator-tag ambiguities remain.

Public ropeways are curated from the aerialway inventory. Ski-only and
clearly inactive installations are excluded; a small set of public year-round
lifts is explicitly retained. Current seasonal calendars are not all verified.

## 4. Reconcile water services with geometry

The upstream ferry checklist carries operator/source URLs and encoded path
geometry. Paths are decoded, reprojected and retained with their geometry
quality: mapped, direct, approximate, partial or unavailable.

The compilation cross-matched the MLIT passenger-operator directory and
reviewed unmatched current OSM ferry ways. An unmatched way is an audit
candidate, not proof of an active scheduled passenger service. Known stale,
demand-only and event-only candidates were not blindly added.

Variable sightseeing services without a published circuit use departure
markers. Approximate connections are kept distinguishable from mapped paths.

## 5. Keep the geography

The national compilation uses a WGS84 Lambert conformal conic working
projection:

```text
+proj=lcc +lat_1=30 +lat_2=46 +lat_0=36 +lon_0=136
+datum=WGS84 +units=m +no_defs
```

OSM coastline endpoints are joined and polygonized. Land geometry is simplified
to approximately 25 metres for the atlas; selected lake boundaries are retained.
The national static map and its regional sheets use this projected geometry.
Okinawa, Izu and Ogasawara are not relocated into convenient insets.

The browser payload is transformed back to WGS84 longitude/latitude. Line
geometry is simplified at approximately 1.2 metres in the projected working
space and serialized to six decimal places. Decimal precision is not a claim
of survey accuracy. The interactive view uses Web Mercator.

## 6. Build a smaller interactive representation

The source network has 96,099 geometry sections. The interactive payload groups
them by mode, operator, cleaned name, geometry quality and water-service ID,
then merges compatible line segments. It preserves parallel tracks rather than
turning an entire railway corridor into a schematic stroke.

The resulting 1,846 route groups have matching metadata indexes. Point-feature
IDs match the search index. Nearby ground routes are selected within roughly
150 metres of a station object. A nearby-line result is geometric context,
not timetable or interchange evidence.

Station objects are deduplicated by name and short-distance proximity during
compilation. English names are retained where available. A limited fallback
matches existing unnamed current objects to nearby MLIT station names; the
source is recorded.

## 7. Render locally in the browser

`tools/build.py` embeds the gzip-compressed payload, MapLibre module, worker,
styles, application and license notices into `index.html`.

The browser decompresses the payload, creates the MapLibre worker and indexes
GeoJSON into vector tiles. The renderer draws lines and labels for the current
zoom. Local-font glyph generation handles Japanese and Latin names without a
remote glyph server. Optional GSI raster tiles provide street context.

The web build is deterministic from checked-in inputs. Re-running the original
GIS compilation against “latest” upstream data can produce a different network;
manual selection and service-status review are part of that compilation.

## 8. Export rasters without a multi-gigabyte framebuffer

The national PNG is 36,000 × 44,000 pixels. Rendering uses spatial indexes,
overlapping tiles, antialiasing and a streaming PNG writer. Only a strip of
the image is assembled at once. This avoids allocating the entire 1.584-billion-
pixel RGB/RGBA image in a single in-memory canvas.

The nine regional sheets are 10,000 × 12,600 pixels. Those images are release
assets rather than part of Git history. The web application's PNG export is
independent: it captures the current map view and adds attribution.
