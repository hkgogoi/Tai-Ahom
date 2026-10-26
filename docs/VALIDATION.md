# Release validation

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
