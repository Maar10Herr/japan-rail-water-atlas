# Coverage and uncertainty

This atlas assembles a substantial nationwide network. Completeness has not
been certified, and coverage of a transport category is not proof that every
service in that category is present.

## Scope

The dataset includes JR conventional passenger rail, Shinkansen, private and
third-sector rail, metro, tram/light rail, monorail, AGT/maglev, funiculars,
curated public ropeways/lifts, scheduled passenger ferries, waterbuses and
scheduled sightseeing boats. Japan-serving international ferries are selectable.
Seasonal scheduled boat services are retained. Long-term suspensions are a
separate reference layer.

Bus and air networks are outside the project. The current passenger-network
selection excludes freight-only tracks, yards, sidings, ski-only lifts and
charter-only boats. The historical layer has a broader railway scope, including
former industrial and freight infrastructure. Minor heritage
operations and park transport without positive passenger/schedule evidence
have not been exhaustively verified.

## Water-service geometry

| Geometry source for active records | Records | Interpretation |
| --- | ---: | --- |
| OSM | 408 | Mapped source geometry, not necessarily a surveyed vessel track |
| Direct connection | 23 | Port-to-port connection rather than an exact course |
| Approximate | 20 | Estimated alignment, explicitly marked |
| Partial | 10 | Incomplete available geometry |
| No fixed circuit | 104 | Departure marker only |
| **Total marked active** | **565** | Service status is an inventory classification |

Another 22 records are marked suspended. An annual or seasonal service
classification does not establish that a vessel is operating on a particular day.
Operator timetables have not all been individually rechecked.

The missing-circuit services are not drawn as invented loops. A hollow diamond
marks the departure. That means the service inventory is broader than the set
of fixed paths that can be rendered.

### Operator cross-check

All 204 operator links in MLIT's scheduled passenger-operator directory were
matched to the ferry inventory: 191 by URL/domain and 13 by explicit
operator/route-name aliases. The evidence is in
[`mlit_ferry_operator_audit.csv`](../data/audits/mlit_ferry_operator_audit.csv).

This is an operator-level cross-check. The directory itself covers scheduled
operators with websites; it is not a complete list of every small crossing,
every sightseeing service or every route operated by each company.

## Railway geometry cross-check

The MLIT 2022 rail inventory contains 595 operator/line pairs. In the initial
comparison against selected current OSM passenger geometry:

- 584 pairs had at least 90% of sampled 2022 geometry within 250 metres of
  selected current passenger track.
- 580 pairs had at least 99% nearby.
- The length-weighted proximity was approximately 99.0%.

These figures measure **proximity to a historical geometry baseline**. They are
not a network-completeness percentage. The tolerance is intentionally much
larger than the line simplification used for rendering. It accommodates
alignment and source differences and is unsuitable as a survey-accuracy test.

See [`rail_2022_coverage_audit.csv`](../data/audits/rail_2022_coverage_audit.csv).
Most large residual gaps corresponded to closures, bus conversions or long-term
disaster suspensions. Current OSM also includes openings after the 2022 baseline.

## Examples of explicit audit handling

- Closed Rumoi, Furano–Shintoku, Hiroshima Skyrail and Myoken remnants were not
  promoted to active services merely because an old inventory contained them.
- Hita-Hikosan BRT, Nagoya guideway bus and the former Tateyama trolleybus/e-bus
  segment were excluded from the rail network.
- Mine, northern Hisatsu, northern Tsugaru and the affected Kururi end section
  are contextual long-term suspensions. Their historical alignments may differ
  from current infrastructure.
- Kurobe Gorge Railway was added after a missing-route-relation audit and a
  check of the operator's published timetable.
- Naha–Kumejima Ocean Jet and Jogashima Sanshiro were added through supplementary
  checks. Ocean Jet geometry is approximate; its Motobu branch suspension is
  documented in the inventory.
- Ishigaki–Keelung was changed to suspended based on the available status evidence.
- Unmatched OSM ferry ways were reviewed rather than automatically included.
  Candidates contained obsolete Miyako–Muroran, Saruhama–Hirara, Garve and
  Shinjima services, Expo shuttles and demand-only boats.
- Metro through-running relations do not automatically reclassify a private
  or JR operator's infrastructure as municipal metro track.

## Names, objects and operational meaning

The current-network map includes 11,103 searchable station and terminal objects,
of which 9,304 are railway station/stop objects in the public selection. Station CSV
rows carry Japanese-name and Latin-label provenance separately.

The [review ledger](../data/reviews/) records 99 supported names and 370 applied
Latin-label corrections. 133 objects still lack a supported name; 1,426 lack a
supported Latin label. Those gaps remain explicit in the downloadable audits.

Station selection checks lifecycle, access, usage and freight/signal tags,
with operator evidence for restorations. The independent MLIT station-geometry
comparison produced 91 distant candidates, which included closures, suspended
services, bus conversions and relocated stations. Four verified omissions were
restored: Doai, Tennoji-Ekimae, Kikugaoka and Sarakurayama Sanroku. The nine
Linimo stations retain distinct operator identities at Fujigaoka and Yakusa.
Nearby subway and Aichi Loop boarding places are preserved as separate objects.

A broad guideway class does not imply magnetic levitation. The real Linimo
service is maglev; other members include monorails, automated guideways and
public access slope cars. Pedal cycles, go-karts and amusement-only circuits
are outside the public transport selection. Funaoka's documented multi-year
suspension is represented in the suspension layer.

Ropeway point selection is tied to the curated network. Six scheduled public
sightseeing lifts have positive operator evidence of non-ski operation. A
rejected raw chairlift point is not a claim that the installation never carries
sightseers; unknown calendars and unselected networks remain review priorities.

Interchanges can contain multiple operator objects or overlapping platform
representations. A count of point objects is not a count of distinct commercial
stations. Similarly, route groups and way sections are not service counts or
unique route-kilometres.

The station popup's nearby-line list uses geographic proximity plus a small
number of explicitly reviewed station-to-line identities. It does not
establish a boarding opportunity or a scheduled stop. The dataset contains
neither a timetable nor a routable connection graph.

## Historical railways

The optional historical layer combines **all recorded eras**. It is neither a
single-year map nor a claim that every displayed railway operated at the same
time. It includes former passenger railways, tramways, industrial and forest
railways, coal lines and rural light railways where source geometry exists.
Historical point objects can include earlier station locations, boarding
places and former freight/signal sites. They are not all public passenger
stations.

| Historical selection | Objects | Interpretation |
| --- | ---: | --- |
| Line features | 5,712 | Source paths, sections or remnants; not distinct railways or unique route-kilometres |
| Station objects | 2,267 | Former point locations after cross-source reconciliation |
| Station objects in Hokkaido | 803 | Geographic subset; not an exhaustive count of Hokkaido's closed stations |
| Industrial-site markers | 3 | Representative locations without a supported complete track alignment |
| Approximate Minami-Daitō line features | 7 | Subset of the line features, adapted from a schematic |

Brown dashes show historical lines. Hollow circles show former station
objects, and hollow squares identify site-only locations. Popups identify the
source, geometry quality, available dates and source-specific limits.
Approximate Minami-Daitō geometry is drawn more faintly. High-zoom detail does
not make reconstructed or schematic alignments survey-accurate.

### Geographic and industrial coverage

Hokkaido draws on the Naeboworks reconstruction and mapped OSM/OHM features.
This includes closed national/private railways and smaller rural, coal and
forest systems. Eight further Naeboworks regional datasets supplement the
nationwide remnant selection. Coverage remains uneven, and some former lines
are represented by disconnected fragments or only a site marker.

Minami-Daitō's sugar railway has seven approximate sections adapted from
Tamurono157's freely licensed network diagram. Its declared **1,000-metre
positional uncertainty** is a conservative display allowance, not a measured
statistical accuracy. The diagram is undated, and its branches need not be
contemporary. The documented 1983 closure applies to the network; it is not an
independently established closure date for each branch. Cane-loading sidings
and individual loading places are not reconstructed.

Miyako's prewar sugar railway is documented in architectural historical
research, including **9,085 metres of track around 1939**. The map shows the
factory location with a site marker. It does not infer a railway alignment,
passenger stations or loading places from that fact. The factory itself can
remain active while its railway is historical. Kitadaitō's phosphate-tramway
heritage is also shown as a site-only marker; its documented industrial-site
period is not presented as a surveyed track operating interval.

### Dates, lifecycle tags and exclusions

OSM lifecycle tags describe mapped physical or operational status. A removed
track, disused structure or flood-damaged railway is not, by itself, proof of
permanent closure. Exact current/history overlaps and affected Hisatsu/Kumagawa
objects were reviewed against operator and reconstruction evidence. The old
Kawamura location is historical; the operating replacement Sagara-Toshima
remains in the current selection. Futamata's documented 2026 closure is
retained with its source evidence.

OHM start/end dates can describe an operator, station identity or alignment
period. Ended identities on current track are screened out conservatively;
remaining dates still retain their source scope. Multiple historical names on
identical geometry are stored as separate source periods rather than extra
parallel lines. Missing dates and unsupported romanizations remain absent.

Never-opened railway projects and planned station sites are excluded. Reviews
separate operated portions from unbuilt extensions and distinguish industrial
operation from later unfinished public railway projects. Remnants are not
connected across missing geometry. Cross-source duplicates are reconciled by
source identity and documented spatial/name tests, but nearby or separately
mapped objects can still remain distinct.

The freely downloadable MLIT N05 time-series data is **not redistributed**.
Its source-specific terms restrict noncommercial use and exclude
redistribution of copies. Its absence is a material coverage limitation,
especially for systematic historical station inventories.

The [component files and audits](../data/history/) preserve both source-level
coverage and integration decisions. Source component counts can exceed the
final interactive counts because exclusions and duplicate reconciliation
are applied when the combined layer is built.

## Where better evidence is especially useful

Small river crossings, current public-ropeway calendars, minor heritage
operations, recently changed ferry schedules, unnamed objects and incomplete
water geometry remain priorities. Historical railway gaps benefit from dated
maps, archives and freely reusable alignment data with clear source rights.
Corrections should carry an official
operator, municipality or transport-bureau source.
