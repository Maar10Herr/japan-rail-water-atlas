# Source provenance

## Primary geometry and inventories

| Source | Baseline | Use |
| --- | --- | --- |
| [OpenStreetMap / Geofabrik Japan](https://download.geofabrik.de/asia/japan.html) | OSM replication timestamp `2026-10-24T20:20:51Z` | Passenger-positive rail geometry, route relations, aerialways, coastlines, lakes and station/terminal objects |
| [MLIT N02 rail data](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N02-v3_1.html) | 2022-12-31 | Historical rail sections and stations; geometry comparison, limited name fallback and suspension context |
| [MLIT passenger/ferry operator directory](https://www.mlit.go.jp/maritime/bosai_shipslink.html) | Retrieved for the compiled snapshot | Scheduled passenger-operator cross-match |
| [kametaro7/japan-ferry-map](https://github.com/kametaro7/japan-ferry-map) | Inventory marked 2026-09-13 | Water-service checklist, original source URLs and credited OSM-derived path geometry |
| [OpenStreetMap standard tiles](https://operations.osmfoundation.org/policies/tiles/) | Live, optional | Roads, buildings and place labels; visible-view requests and normal browser caching |
| [GSI tile catalogue](https://maps.gsi.go.jp/development/ichiran.html) | Live, optional | Seamless aerial imagery requested only when enabled, with GSI/Landsat/GRUS credits |

The N02 2022 inventory is a dated comparison baseline, not a current service
register. MLIT N09 ferry geometry was from 2012 and was not used as a current
network. The newer Project LINKS ferry material is a sample and was not treated
as nationwide route geometry.

## Historical geometry and site records

| Source | Use and adaptation | Source terms |
| --- | --- | --- |
| [OSM / Geofabrik Japan](https://download.geofabrik.de/asia/japan.html) | Lifecycle-tagged former tracks and station/site objects from the same OSM snapshot; operational, never-opened and duplicate candidates reviewed | [ODbL 1.0](https://www.openstreetmap.org/copyright) |
| [Naeboworks / 苗穂工房](https://naeboworks.com/haisen/) | Hokkaido and eight regional KML datasets converted to GeoJSON; status selection, reviewed unbuilt-extension removal, metadata normalization and integration | [CC BY 4.0 KML reuse terms](https://naeboworks.com/haisen/about.htm); © 2007–2026 苗穂工房 / naeboworks, mapped from GSI Japan aerial photographs; adapted |
| [OpenHistoricalMap](https://www.openhistoricalmap.org/copyright) | Ended mapped alignment/station periods, with current-identity screening and repeated-geometry period reconciliation | CC0 default; explicit non-CC0 feature licenses and known restricted-source references excluded |
| [Minami-Daito-Sugartrain-line.gif](https://commons.wikimedia.org/wiki/File:Minami-Daito-Sugartrain-line.gif), Tamurono157 | Seven approximate Minami-Daitō sugar-railway sections digitized from the schematic and georeferenced using OSM geography | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/); adapted. OSM geographic registration remains separately credited |
| [Minamidaitō Village school history](https://www.vill.minamidaito.okinawa.jp/uploaded/attachment/28.pdf) | Network history and 1983 closure; network-level facts, not branch-by-branch dates | Factual reference; source artwork not reproduced |
| [Tsujihara & Imamura, 2015](https://www.pu-kumamoto.ac.jp/users_site/m-tsuji/ronbun.html/paper15.html/pap1503.pdf) and [2017](https://www.pu-kumamoto.ac.jp/users_site/m-tsuji/ronbun.html/paper17.html/pap1702.pdf) | Architectural historical research supporting Miyako's former factory railway and Okinawan sugar-railway context | Factual summaries with citations; paper illustrations and map artwork not reproduced |
| [GSI address search and content terms](https://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html) | Representative geocoded Miyako factory location, not a track alignment | Public Data License 1.0; GSI credited |
| [Agency for Cultural Affairs: Kitadaitō phosphate-mine remains](https://kunishitei.bunka.go.jp/heritage/detail/401/00003973) | Representative heritage-site marker and historical facts; no inferred railway line | Original atlas annotation from factual record, dedicated CC0; source artwork not reproduced |

Naeboworks' KML-data license explicitly permits redistributed and modified
data with attribution. Its independent website, interface and background map
are not reproduced. Original dataset links, hashes, status classifications,
adaptations and limits are preserved in the
[Hokkaido provenance](../data/history/naeboworks-hokkaido-provenance.json) and
[regional provenance](../data/history/naeboworks-regions-provenance.json).

OHM extraction uses its documented
[Overpass endpoint](https://wiki.openstreetmap.org/wiki/OpenHistoricalMap/Overpass).
The [provenance record](../data/history/ohm-provenance.json) records the source
timestamp and conservative selection. The
[Okinawa provenance](../data/history/okinawa-sugar-provenance.json) includes
the schematic control points, transcription, geographic registration,
uncertainty and excluded inferences. A modern factory's presence is not used
as evidence for an invented sugar-railway network.

Component files can contain candidates that are omitted during final
integration. The [integration audit](../data/history/integration-audit.json),
[current/history conflict review](../data/history/current-history-conflicts.json),
[station relocation review](../data/history/station-relocation-review.json),
[current/historical station review](../data/history/current_station_closure_review.json)
and [industrial-coal review](../data/history/industrial-coal-review.json)
record these decisions. They include primary operator, museum, municipal and
archive references. The station review links JR Hokkaido's official closure
notices and distinguishes a source update date from an actual service-end
date.

### Reviewed source not redistributed: MLIT N05

[MLIT N05 Railway Time Series, 2025 edition](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N05-2025.html)
was inspected as a possible nationwide historical source. Its source-specific
conditions remain noncommercial, and the linked
[content terms](https://nlftp.mlit.go.jp/ksj/other/agreement_02.html) exclude
redistribution of copies for that category. No N05 line geometry or station
table is included. The public
[source decision](../data/history/excluded-source-decision.json) records the
exclusion. This source is distinct from the N02 reference data used elsewhere
in the atlas.

## Selected supplementary checks

- [Kumejima Ocean Jet](https://ko-jet.com/) — Naha–Kumejima service and timetable.
- [Kurobe Gorge Railway](https://www.kurotetu.co.jp/timetable/) — published operating extent and timetable.
- [Takaotozan Railway](https://www.takaotozan.co.jp/timeprice/index.php) — cable-car and public lift operation.
- [Misaki Marine Center](https://misaki-marinecenter.subaru-kougyou.jp/) — Jogashima Sanshiro ferry.
- [Kagoshima City](https://www.city.kagoshima.lg.jp/shimin/sakurajima/soumu/machizukuri/igai/kokyo/koku/fune.html) — closure of the Shinjima administrative boat.
- [Gifu Prefecture](https://www.pref.gifu.lg.jp/site/pressrelease/481279.html) — Nishinakano crossing closure.
- [Kurobe Dam](https://www.kurobe-dam.com/kankou/) — Garve sightseeing-boat closure.
- [JR East Kururi information](https://traininfo.jreast.co.jp/train_info/line.aspx?gid=1&lineid=kururiline) — affected Kururi end-section service status.

These live pages can change. The compiled records retain available URLs, but
the repository is not an archive of every source page or every timetable.

## Existing-map research

- [AllRailMap](https://allrailmap.com/) — closest discovered nationwide rail-plus-ferry reference; a verified full-scope ultra-resolution export was not established.
- [Railmap.jp introduction](https://railmap.jp/intro.html) — nationwide passenger railway coverage with documented ropeway/lift exclusions and differing regional scales.
- [Railway Information Hall](https://tetsudozyoho.com/tetsudomap/) — national railway categories; the inspected passenger map acknowledged a missing railway.
- [RailsMaps Japan](https://railsmaps.com/japan) — broad infrastructure coverage; full passenger ground-and-water coverage was not established.

These were research references, not sources from which proprietary map
cartography was copied.

## Rendering software

[MapLibre GL JS](https://maplibre.org/) 6.15.0 is bundled from its published npm
package. Its original license notices are retained in the single-file build
and in [`LICENSES/`](../LICENSES/). Original project code and third-party data
have separate licenses; see [NOTICE.md](../NOTICE.md).

## Station review references

The per-object references in [`data/reviews/`](../data/reviews/) include JR East,
Hankai, Kitakyushu Monorail, Linimo, Sarakurayama Cable Car, public-lift
operators, municipalities and official tourism material. Selected operator
English maps and existing OSM/Wikidata identities support Latin labels. The
review files distinguish direct source spellings from explicit-kana
romanizations and translated descriptors. Wikidata structured labels are
[CC0](https://www.wikidata.org/wiki/Wikidata:Licensing).

Licensing references for the application are the FSF's
[GPL-compatible license list](https://www.gnu.org/licenses/license-list.html)
and [GPL FAQ on copyright-holder licensing](https://www.gnu.org/licenses/gpl-faq.en.html#ReleaseUnderGPLAndNF).
MapLibre's BSD notices and dependency notices are retained. The code license
does not change data-source or background-provider terms.
