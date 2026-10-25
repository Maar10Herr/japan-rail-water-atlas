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

Bus and air networks are outside the project. Freight-only tracks, yards,
sidings, ski-only lifts and charter-only boats are excluded. Minor heritage
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

The map includes 11,251 searchable station and terminal objects. The selected
OSM baseline included 9,335 railway station/stop objects; 9,051 had an English
name. A small number of existing unnamed objects were matched to nearby MLIT
names. The station CSV records the name source. Remaining unnamed objects are
identified explicitly rather than given invented names.

Interchanges can contain multiple operator objects or overlapping platform
representations. A count of point objects is not a count of distinct commercial
stations. Similarly, route groups and way sections are not service counts or
unique route-kilometres.

The station popup's nearby-line list uses geographic proximity. It does not
establish a boarding opportunity or a scheduled stop. The dataset contains
neither a timetable nor a routable connection graph.

## Where better evidence is especially useful

Small river crossings, current public-ropeway calendars, minor heritage
operations, recently changed ferry schedules, unnamed objects and incomplete
water geometry remain priorities. Corrections should carry an official
operator, municipality or transport-bureau source.
