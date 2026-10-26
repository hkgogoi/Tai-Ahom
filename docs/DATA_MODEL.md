# Data model

## Public records

`data/index/<work>.json` contains stable `id` (`<work>:<source-record-id>`), `work`, `source_record_id`, explicit `folio` or null, analytical `source_page` or null, record `confidence`, `headword_confidence`, flags, source ID and field-presence indicators. Bar Amra additionally retains supplied image number, facsimile page and original reference.

`has_english` indicates that a field exists, not that a complete or accepted translation exists. Placeholders remain source records. A null folio is unknown, not a missing historical leaf.

`works.json` holds source credits, source revision dates, links, scope, subject tags and project identifiers. `catalogue.json` preserves the 121-item historical inventory and adds two revision links, without overwriting its date.

## Private reading pack

Schema: `tai-ahom-reading-pack`, version 1. Each record adds:

- `layers.inherited_transcription`: genuine Unicode Ahom, including explicit editorial gap markers.
- `layers.english`: inherited English, unchanged.
- `layers.formula`, `assamese_in_ahom_script`, `punctuation`, `romanization` and `assamese_romanization`: Bar Amra's distinct fields.
- `layers.editorial_reconstruction` and `interpretation`: null in this release.
- `notes`, `reading_status`, `source_record`: original uncertainty, review and full source evidence.

The supplied source object is preserved exactly in `source_record`. Legacy strings and alternatives are retained there but are not treated as valid Unicode transcriptions. Search only folds Latin accent marks; Ahom combining vowel signs remain significant.

## Import boundary

Browser import checks schema/version, maximum size, known and unique IDs, work and folio identity, original record IDs, inherited confidence, field types and PUA/replacement characters. Values are escaped before HTML rendering. Data is loaded into memory; optional persistence uses IndexedDB. No network request sends pack contents.

Validation checks structure and provenance consistency, not the truth of a philological claim. A local edited pack may contain a researcher's changes and should not be confused with the fingerprinted distribution. For exact preservation, run `scripts/verify_private.py` against the original archives.
