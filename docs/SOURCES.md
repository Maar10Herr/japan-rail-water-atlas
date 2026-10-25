# Source provenance

## Primary geometry and inventories

| Source | Baseline | Use |
| --- | --- | --- |
| [OpenStreetMap / Geofabrik Japan](https://download.geofabrik.de/asia/japan.html) | OSM replication timestamp `2026-10-24T20:20:51Z` | Passenger-positive rail geometry, route relations, aerialways, coastlines, lakes and station/terminal objects |
| [MLIT N02 rail data](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N02-v3_1.html) | 2022-12-31 | Historical rail sections and stations; geometry comparison, limited name fallback and suspension context |
| [MLIT passenger/ferry operator directory](https://www.mlit.go.jp/maritime/bosai_shipslink.html) | Retrieved for the compiled snapshot | Scheduled passenger-operator cross-match |
| [kametaro7/japan-ferry-map](https://github.com/kametaro7/japan-ferry-map) | Inventory marked 2026-09-13 | Water-service checklist, original source URLs and credited OSM-derived path geometry |
| [GSI tile catalogue](https://maps.gsi.go.jp/development/ichiran.html) | Live, optional | Pale street-context tiles requested only when the map option is enabled |

The latest MLIT rail inventory inspected was historical, not a current service
register. MLIT N09 ferry geometry was from 2012 and was not used as a current
network. The newer Project LINKS ferry material is a sample and was not treated
as nationwide route geometry.

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
