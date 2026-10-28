# Release validation

## Release 0.2.1, 28 October 2026

- Source catalogue extended to 124 links: the original 123 entries are retained unchanged, followed by the 32-page Nanzhao report with its full title, completion date, bibliographical description, subjects and existing Drive URL.
- Research adds a separately attributed study summary with documented evidence, plausible connections and unverified genealogy labelled distinctly. The earlier Lengdon–Nimi dossier is retained unchanged.
- Source search covers descriptive metadata and subjects; regression tests cover research discovery, category filters and older entries without optional metadata.
- The catalogue supplement is consumed by the original importer, preserving later research additions on re-import.
- Record indexes, work metadata, Bar Amra coverage, source fingerprints and the private reading stub are unchanged. The 26 October import report remains dated historical evidence.
- Build, archive validation, all 13 automated tests and JavaScript syntax checks passed. Render smoke checks passed for Home, Sources, Research, Coverage, Explore and Load readings. A comparison with the 0.2.0 commit confirmed all 123 prior catalogue entries and the earlier dossier unchanged, plus 13 protected files byte-identical. Deployment and live-site results are recorded in the update's completion report.
- The Drive connector successfully read the exact report URL and metadata. Anonymous visitors may still require access; no Drive permissions were changed. No report PDF, source plates, scans or third-party publications are copied into the public tree.

## Earlier release record

Release 0.2.0, 26 October 2026.

## Completed checks

- 4,637 unique, stable record identifiers across seven collections; expected per-work totals match.
- 123 source links: the dated 121-item inventory plus two Bar Amra revision links.
- Every source object and its normalized Ahom and English fields compared with the four supplied inputs; all retained without alteration.
- All 1,230 Bar Amra baseline objects compared with the revised master and retained unchanged.
- 1,236 Bar Amra records, 819 B / 417 C; four selected A-rated headwords and zero A-rated complete entries.
- 61 folio mappings; four empty whole-folio targets and 55 unresolved numbered IDs; all 65 research targets retained.
- No private-use or replacement characters in searchable Ahom fields; all five Ma Likha unresolved-glyph markers retained.
- Public-content validation: no reading layers, full source records, scans or temporary download credentials in published data.
- Eleven automated tests cover Unicode vowel distinction, English and language-field search, exact folio filtering, combined filters, metadata-only search, import integrity, duplicate/unknown IDs, confidence conflicts, invalid encoding, empty text and HTML escaping.
- JavaScript syntax checks passed.
- Desktop home page rendered and visually inspected. Browser file import displayed all 4,637 readings loaded and saved on the device.

## Verification limits

The browser then became unresponsive during the combined English/manuscript/folio UI test. A supported recovery attempt also timed out. Consequently the final combined interaction, mobile viewport screenshot and browser-based GitHub Pages setup were not completed. Automated search/import checks passed; this does not imply that every browser interaction was tested.

No new independent manuscript transcription, new translation, complete visual collation or new reproduction permission is claimed. Source links preserve existing access restrictions and were not exhaustively revalidated individually.

## Publication

The Pages workflow runs the build and checks on main. Deployment is conditional on Pages being enabled; manual workflow dispatch is also supported. A green validation job or a committed workflow does not imply that a live website exists. Check the GitHub deployment result before treating a website URL as live.
