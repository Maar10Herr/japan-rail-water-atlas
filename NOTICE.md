# Attribution and licensing

The application and its data are different things, with different licenses.

| Material | Terms / attribution |
| --- | --- |
| Original application code, build tools and documentation | [GNU GPL v3 only](LICENSE) |
| OpenStreetMap-derived rail, coastline, water-route and station database | © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright), [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/) |
| Ferry geometry from `kametaro7/japan-ferry-map` | Upstream documents its OSM-derived geometry as ODbL; retain [upstream attribution](https://github.com/kametaro7/japan-ferry-map#データの出典とライセンス) |
| MLIT rail reference and historical suspension alignments | 国土交通省 / Ministry of Land, Infrastructure, Transport and Tourism, [National Land Numerical Information](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N02-v3_1.html), 2022 rail baseline; observe the source's applicable public-data terms |
| Operator and municipality references | Factual service information with original URLs in route metadata and inventories; upstream material retains its applicable terms |
| MapLibre GL JS and included upstream code | BSD-3-Clause and included notices: [full bundled license](LICENSES/MapLibre-BSD-3-Clause.txt) |
| Optional live aerial imagery | 地理院タイル / Geospatial Information Authority of Japan; [tile catalogue and usage terms](https://maps.gsi.go.jp/development/ichiran.html) |

The repository's GPL license does **not** relicense the database, third-party
renderer, source material or map tiles. OSM-derived data in `data/` is provided
under ODbL, with separately credited source components. Preserve attribution
and applicable database share-alike terms when redistributing derived databases.

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
