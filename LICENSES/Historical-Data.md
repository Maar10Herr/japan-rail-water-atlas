# Historical data: component licenses and attribution

The historical layer is assembled from separately licensed source components.
The application license is GPL-3.0-only. It does not replace the licenses of
these data components or license source artwork that is merely cited.

The [combined payload](../data/history.json.gz) retains per-record credits,
license identifiers, source links and source component IDs. Its
[`records`](../docs/METHODS.md#7-assemble-the-historical-record) metadata and the
[component provenance files](../data/history/) should accompany redistribution.
Generated maps and view exports should preserve visible attribution.

## OpenStreetMap

© [OpenStreetMap contributors](https://www.openstreetmap.org/copyright).
Historical railway and station geometry derived from the Geofabrik Japan OSM
extract is provided under the
[Open Database License 1.0](https://opendatacommons.org/licenses/odbl/1-0/).

Component: [`osm.geojson.gz`](../data/history/osm.geojson.gz).
Adaptations include lifecycle selection, exclusion of never-opened projects,
operational-status review, duplicate reconciliation and rendering metadata.
Attribution and applicable database share-alike obligations remain in effect.

## Naeboworks / 苗穂工房

**北海道廃線路線図 © 2007–2026 苗穂工房 / naeboworks — mapped from aerial
photographs by GSI of Japan. Adapted.**

Source: [北海道廃線路線図](https://naeboworks.com/haisen/).
The author's [KML-data reuse terms](https://naeboworks.com/haisen/about.htm)
license both KML data and modified data under
[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).

Components:

- [`naeboworks-hokkaido.geojson.gz`](../data/history/naeboworks-hokkaido.geojson.gz)
- [`naeboworks-regions.geojson.gz`](../data/history/naeboworks-regions.geojson.gz)

Adaptations include KML-to-GeoJSON conversion, former-station/status selection,
reviewed exclusion or trimming of unbuilt extensions, source metadata
normalization, duplicate reconciliation and map styling. Individual changes
and original data hashes are recorded in the corresponding provenance files.
The source's independent website, interface and background map are not copied.
This remains a CC BY 4.0 component; inclusion does not turn it into OSM data.

## OpenHistoricalMap

Historical map data courtesy of
[OpenHistoricalMap contributors](https://www.openhistoricalmap.org/copyright).
OHM dedicates feature data to the public domain under
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) unless an
individual feature specifies another license. This selection excludes explicit
non-CC0 feature licenses pending separate review and excludes references to
known restricted sources. Original source tags and feature URLs are retained.

Component: [`ohm.geojson.gz`](../data/history/ohm.geojson.gz).
Adaptations include ended-period selection, current-identity screening,
duplicate station reconciliation and collapsing repeated old identities of
identical geometry while retaining their source periods.

## Minami-Daitō sugar-railway diagram

**Minami-Daito-Sugartrain-line.gif — Tamurono157, CC BY 3.0; adapted.**

Source: [Wikimedia Commons file page](https://commons.wikimedia.org/wiki/File:Minami-Daito-Sugartrain-line.gif).
Commons' creator metadata names Tamurono157; its attribution field links the
Japanese Wikipedia user [Tamrono157](https://ja.wikipedia.org/wiki/User:Tamrono157).
The diagram is available under
[Creative Commons Attribution 3.0 Unported](https://creativecommons.org/licenses/by/3.0/).

Component: seven approximate line features in
[`okinawa-sugar.geojson.gz`](../data/history/okinawa-sugar.geojson.gz).
The source lines were manually transcribed and georeferenced using island-frame
controls and OSM geography. The output retains a conservative 1,000-metre
positional uncertainty and does not assert a common date for every branch.
© OpenStreetMap contributors, ODbL 1.0, is separately credited for geographic
registration. Both source credits and applicable terms should be retained.

The [Okinawa provenance](../data/history/okinawa-sugar-provenance.json) records
the transcription, controls, transformation and limitations. Scholarly and
municipal references support historical facts; their artwork is not reproduced.

## Representative industrial-site markers

The Miyako factory marker uses a GSI address-geocoding coordinate under
[GSI's Public Data License 1.0 terms](https://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html).
Historical facts are summarized from the cited Tsujihara & Imamura research;
the papers' maps and figures are not reproduced. The marker is not an inferred
track alignment. The Daitō factory-site marker retains its OSM credit and ODbL
provenance in the same component file.

The Kitadaitō marker is an original factual annotation using the
[Agency for Cultural Affairs heritage register](https://kunishitei.bunka.go.jp/heritage/detail/401/00003973),
dedicated by the atlas author under
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).
No register photograph or map artwork is reproduced. The representative
location does not establish individual station or track positions.

## Excluded MLIT N05 source

No N05 feature data is included. Its source-specific permission is
noncommercial and excludes redistribution of copies. This differs from the
MLIT N02 reference component used by the current-network atlas. The
[source decision](../data/history/excluded-source-decision.json) links the
official conditions and records the exclusion.
