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

The source network has 96,088 geometry sections. The interactive payload groups
them by mode, operator, cleaned name, geometry quality and water-service ID,
then merges compatible line segments. It preserves parallel tracks rather than
turning an entire railway corridor into a schematic stroke.

The resulting 2,313 route groups have matching metadata indexes. Point-feature
IDs match the search index. Nearby ground routes are selected within roughly
150 metres of a station object. A nearby-line result is geometric context,
not timetable or interchange evidence.

Initial station extraction used name and short-distance proximity to suppress
redundant source points. Operator identity matters at interchanges: separately
identified boarding places are preserved, including the Linimo terminals
alongside their subway and Aichi Loop counterparts. English names are retained
where available. A limited fallback
matches existing unnamed current objects to nearby MLIT station names; the
source is recorded.

Unnamed lines keep their own raw source identity. They cannot form a single
nationwide group or inherit an English name from a disconnected installation.
Own Japanese/English tags take precedence over generic mode labels. Generic
mode names remain available in details, but are not printed along every
unnamed segment. Route metadata retains every contributing raw object ID.

The evidence-backed station and infrastructure review is documented in
[`data/reviews/`](../data/reviews/). It distinguishes verified operator English,
existing Latin tags, same-station identity transfers, linked CC0 Wikidata
labels and explicit-kana romanization. Arbitrary kanji readings are not guessed.

## 7. Assemble the historical record

Historical data is compiled separately from the current passenger network.
The historical scope includes former freight, forestry, industrial and rural
light railways. It combines OSM lifecycle-tagged geometry, Naeboworks regional
KML reconstructions, selected OpenHistoricalMap feature periods and documented
Okinawan industrial history. Source components retain their own licenses and
provenance rather than being relabeled as one uniformly licensed database.

OSM selection requires positive past-use evidence. Proposed/construction-only
projects and unsupported historic structures are excluded. Lifecycle tags are
reviewed alongside exact current-network overlaps: physical flood damage,
temporary suspension and continuing heritage operation do not alone establish
permanent closure. Station relocations are evaluated separately, preserving
both a supported former location and its operating replacement where relevant.

Naeboworks KML points are classified using the creator's legend. Current and
planned markers are excluded; former station locations and documented closed
passenger places that became signal locations can be retained. Reviewed
never-opened extensions are removed, with cuts made on existing source paths
at the documented operated terminus. Changes, exclusions and source hashes are
recorded in the Hokkaido and regional provenance files. Coordinates are source
reconstructions, not survey positions.

OHM selection requires an explicit ended feature period. Current-track
proximity and identical unended OHM geometry screen out historical names or
operators on extant infrastructure. Same-family station proximity is screened
conservatively, and repeated identities of identical historical track geometry
are collapsed while their source periods remain available. An OHM period end
can describe an identity/alignment change rather than closure of the whole
railway. Explicit non-CC0 feature licenses and known restricted-source
references are excluded from this selection.

For Minami-Daitō, seven line sections are manually transcribed from
Tamurono157's CC BY 3.0 schematic and georeferenced with a thin-plate-spline
transformation using island-frame controls. OSM geography provides the
registration reference. A conservative 1,000-metre display uncertainty and
the diagram's undated, mixed-period character remain explicit. This is not a
surveyed railway centreline. The island network's documented 1983 closure is
kept at network scope, without invented branch operating dates.

Miyako's factory location is geocoded from GSI address data; research supports
the former sugar railway, but no route geometry is inferred from its length
or the factory's location. Kitadaitō likewise uses a representative official
heritage-site location. These are site markers, not reconstructed stations.

Integration reconciles source identifiers, overlapping station names/locations
and duplicate line fragments using the recorded rules. It retains raw source
IDs, source components, credits, licenses, geometry-quality classes and scoped
dates in the metadata. Gaps remain gaps. No missing link or kanji reading is
invented to produce a visually continuous network.

`data/history.json.gz` stores separate line/point GeoJSON collections and a
matching `records` index. Each feature's numeric `i` links to its record;
record fields include `source_component`, `source_ids`, `source_urls`,
`license`, `credit`, `dates`, `notes` and `geometry_quality`. Dates carry a
label and scope rather than silently becoming a common opening/closure field.
The layer combines all recorded eras and does not support a synchronized
historical-year filter. Source components, point CSV and integration audits
are published in [`data/history/`](../data/history/).
`tools/history/build_payload.py` deterministically compiles those checked-in
components and review decisions into the combined payload using Python's
standard library. Fetching and preparing updated upstream components is a
separate research operation.

MLIT N05 was reviewed but not ingested: its source-specific permission and
redistribution restriction are incompatible with publishing copies of its
feature data in this atlas. The source decision is published with the audits.

## 8. Render locally in the browser

`tools/build.py` embeds the gzip-compressed current and historical payloads,
MapLibre module, worker, styles, application and license notices into
`index.html`. The historical payload is decompressed and indexed only when its
toggle is enabled. Historical search entries and attribution are active with
that layer; a separate control governs its station/site markers.

The browser decompresses the payload, creates the MapLibre worker and indexes
GeoJSON into vector tiles. The renderer draws lines and labels for the current
zoom. Local-font glyph generation handles Japanese and Latin names without a
remote glyph server. Optional OpenStreetMap raster tiles provide roads,
buildings and place labels; GSI seamless aerial imagery provides photographic
context. A separate opacity control affects only the background raster layer.
Sources are created on selection and removed when disabled. The browser keeps
normal caching and HTTP referrers; tile prefetch is disabled.

Scroll zoom uses the renderer's native handlers with mouse-wheel rate 1/200 and
trackpad rate 1/60. The view supports zoom levels 3 through 22; source geometry
is overzoomed at close scales rather than requesting nonexistent transport data.

The web build is deterministic from checked-in inputs. Re-running the original
GIS compilation against “latest” upstream data can produce a different network;
manual selection and service-status review are part of that compilation.

## 9. Export rasters without a multi-gigabyte framebuffer

The national PNG is 36,000 × 44,000 pixels. Rendering uses spatial indexes,
overlapping tiles, antialiasing and a streaming PNG writer. Only a strip of
the image is assembled at once. This avoids allocating the entire 1.584-billion-
pixel RGB/RGBA image in a single in-memory canvas.

The nine regional sheets are 10,000 × 12,600 pixels. Those images are release
assets rather than part of Git history. The web application's PNG export is
independent: it captures the current map view and adds attribution.
The published v0.2.0 national/regional rasters are current-network snapshots
without the historical overlay. The view export includes enabled historical
geometry and its source credits.
