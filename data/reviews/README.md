# Station and infrastructure review

These files record evidence-backed choices about the public passenger network.
Object IDs refer to the source objects, not the array indexes used by the web
renderer. Source URLs and the original values are retained for inspection.

| Record | Purpose |
| --- | --- |
| [station_names.json](station_names.json) | 99 names: 88 ferry endpoints matched by route topology and 11 operator-confirmed ropeway terminals |
| [romanization.json](romanization.json) | 317 proposed Latin-label corrections; 316 apply to objects retained in the public selection |
| [romanization_followup.json](romanization_followup.json) | 54 sourced Latin labels for newly identified ports and lift terminals |
| [station_coverage.json](station_coverage.json) | Planned, closed, private, freight and attraction exclusions; verified station and track restorations; suspension evidence |
| [linimo_stations.json](linimo_stations.json) | The nine actual Linimo stations, preserving separate subway and Aichi Loop interchange objects |
| [ropeway_selection.json](ropeway_selection.json) | 126 terminal points outside the curated public network, with raw lift memberships and public exceptions |
| [public_lifts.json](public_lifts.json) | Six public sightseeing chairlifts with operator evidence of non-ski passenger operation, geometry and terminal identities |
| [applied_summary.json](applied_summary.json) | Counts from the applied GIS review |

A ferry endpoint receives a name only when its position matches the encoded
inventory port and it belongs to an OSM way whose endpoints match that sourced
route geometry. A nearby name by itself is insufficient for this assignment.

Latin labels come from operator material, existing OSM Latin tags, validated
same-station/name identities, linked Wikidata labels, or explicit kana readings.
Kana transliteration is identified as romanization, rather than official English.
Arbitrary kanji readings are not guessed. Wikidata structured labels are CC0;
OSM-derived records retain ODbL conditions. Operator references supply individual
factual names, not copied map artwork or timetable layouts.

The ropeway exclusion rule establishes consistency with the selected public
network. It does not prove that every excluded installation operates only for
skiers. Public summer sightseeing exceptions with positive operator evidence
are retained, including the Happo Alpen Line lifts.

There are still 133 unnamed point objects and 1,426 labels without supported
Latin text. The [unnamed inventory](../audits/unresolved_station_names.csv) and
[Latin-label inventory](../audits/missing_latin_labels.csv) make those gaps
explicit. These counts describe this dataset, not an independently complete
inventory of Japan's commercial stations.
