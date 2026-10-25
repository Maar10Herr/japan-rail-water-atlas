# Attribution and licensing

The application and its data are different things, with different licenses.

| Material | Terms / attribution |
| --- | --- |
| Original application code, build tools and documentation | [GNU GPL v3 only](LICENSE) |
| OpenStreetMap-derived rail, coastline, water-route and station database | © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright), [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/) |
| Ferry geometry from `kametaro7/japan-ferry-map` | Upstream documents its OSM-derived geometry as ODbL; retain [upstream attribution](https://github.com/kametaro7/japan-ferry-map#データの出典とライセンス) |
| MLIT rail reference and historical suspension alignments | 国土交通省 / Ministry of Land, Infrastructure, Transport and Tourism, [National Land Numerical Information](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N02-v3_1.html), 2022 rail baseline; observe the source's applicable public-data terms |
| Historical OSM railway/station selection | © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright), ODbL 1.0; source objects and selection/reconciliation audits retained |
| Naeboworks historical regional reconstructions | 北海道廃線路線図 © 2007–2026 苗穂工房 / naeboworks, mapped from GSI Japan aerial photographs; [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), adapted under the author's [KML reuse terms](https://naeboworks.com/haisen/about.htm) |
| Selected OpenHistoricalMap features | [OpenHistoricalMap contributors](https://www.openhistoricalmap.org/copyright), CC0 by default; explicit non-CC0 feature licenses and known restricted-source references excluded |
| Minami-Daitō sugar-railway schematic adaptation | [Minami-Daito-Sugartrain-line.gif](https://commons.wikimedia.org/wiki/File:Minami-Daito-Sugartrain-line.gif), Tamurono157; [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/), adapted and georeferenced; OSM geographic registration separately credited under ODbL |
| Miyako industrial-site marker | GSI address-coordinate source under [Public Data License 1.0](https://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html); cited historical facts from Tsujihara & Imamura, without reproducing paper/map artwork |
| Kitadaitō industrial-site annotation | Original atlas annotation from [Agency for Cultural Affairs factual heritage record](https://kunishitei.bunka.go.jp/heritage/detail/401/00003973), dedicated CC0; source artwork not reproduced |
| Operator and municipality references | Factual service information with original URLs in route metadata and inventories; upstream material retains its applicable terms |
| MapLibre GL JS and included upstream code | BSD-3-Clause and included notices: [full bundled license](LICENSES/MapLibre-BSD-3-Clause.txt) |
| Optional live aerial imagery | 地理院タイル / Geospatial Information Authority of Japan; [tile catalogue and usage terms](https://maps.gsi.go.jp/development/ichiran.html) |

The repository's GPL license does **not** relicense the database, third-party
renderer, source material or map tiles. OSM-derived data in `data/` is provided
under ODbL, with separately credited source components. Preserve attribution
and applicable database share-alike terms when redistributing derived databases.
Naeboworks, OHM and the adapted Minami-Daitō source remain separate components
under their respective terms; their inclusion does not represent relicensing
them as ODbL or GPL. See the [historical-data notices](LICENSES/Historical-Data.md)
for source files, attribution and the changes made.

MLIT N05 time-series feature data is not included or redistributed. Its
source-specific noncommercial/copy-redistribution restrictions are recorded
in [`excluded-source-decision.json`](data/history/excluded-source-decision.json).

Generated maps should retain visible source attribution. The single-file build
includes renderer notices and attribution links. Background tiles are not
bundled or bulk-downloaded by this project.

See [sources](docs/SOURCES.md) for provenance and
[coverage](docs/COVERAGE.md) for the limits of the assembled inventory.

The original application, build tools and documentation are licensed under
**GPL-3.0-only**, Copyright (C) 2026 MH. The bundled MapLibre code keeps its
BSD and other permissive notices. The database is separate from the application
and remains subject to its data-source terms.

Copies of v0.1.0 already distributed under MIT retain those permissions;
the [original notice](LICENSES/Legacy-MIT.txt) is preserved. A later license
change does not withdraw permissions already granted.

Backgrounds are requested directly from their providers for the visible map.
OpenStreetMap standard tiles follow the [OSMF tile usage policy](https://operations.osmfoundation.org/policies/tiles/).
Browser cache headers and normal HTTP referrers are preserved; no offline tile
archive or area-prefetch feature is provided. GSI aerial imagery follows the
[GSI tile catalogue and source credits](https://maps.gsi.go.jp/development/ichiran.html#seamlessphoto).
The seamless layer includes national aerial photographs, Landsat8 imagery
(GSI, TSIC, GEO Grid/AIST; courtesy of USGS), GEBCO bathymetry and global imagery
from NASA/USGS LP DAAC. GRUS imagery is © Axelspace. Image dates and resolution
vary by location; this is not a live satellite feed.

The corresponding application source is included in this repository and its
release source archive. [Renderer and dependency source](https://github.com/Maar10Herr/japan-rail-water-atlas/releases/download/v0.2.0/renderer-corresponding-source.zip)
is provided alongside the HTML download; see [`vendor/README.md`](vendor/README.md).
