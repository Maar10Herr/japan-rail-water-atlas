# Attribution and licensing

The application and its data are different things, with different licenses.

| Material | Terms / attribution |
| --- | --- |
| Original application code, build tools and documentation | [MIT](LICENSE) |
| OpenStreetMap-derived rail, coastline, water-route and station database | © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright), [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/) |
| Ferry geometry from `kametaro7/japan-ferry-map` | Upstream documents its OSM-derived geometry as ODbL; retain [upstream attribution](https://github.com/kametaro7/japan-ferry-map#データの出典とライセンス) |
| MLIT rail reference and historical suspension alignments | 国土交通省 / Ministry of Land, Infrastructure, Transport and Tourism, [National Land Numerical Information](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N02-v3_1.html), 2022 rail baseline; observe the source's applicable public-data terms |
| Operator and municipality references | Factual service information with original URLs in route metadata and inventories; upstream material retains its applicable terms |
| MapLibre GL JS and included upstream code | BSD-3-Clause and included notices: [full bundled license](LICENSES/MapLibre-BSD-3-Clause.txt) |
| Optional live street-context tiles | 地理院タイル / Geospatial Information Authority of Japan; [tile catalogue and usage terms](https://maps.gsi.go.jp/development/ichiran.html) |

The repository's MIT license does **not** relicense the database, third-party
renderer, source material or map tiles. OSM-derived data in `data/` is provided
under ODbL, with separately credited source components. Preserve attribution
and applicable database share-alike terms when redistributing derived databases.

Generated maps should retain visible source attribution. The single-file build
includes renderer notices and attribution links. Street-context tiles are not
bundled or bulk-downloaded by this project.

See [sources](docs/SOURCES.md) for provenance and
[coverage](docs/COVERAGE.md) for the limits of the assembled inventory.
