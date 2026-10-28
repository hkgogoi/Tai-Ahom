# Data model

## Public records

`data/index/<work>.json` contains stable `id` (`<work>:<source-record-id>`), `work`, `source_record_id`, explicit `folio` or null, analytical `source_page` or null, record `confidence`, `headword_confidence`, flags, source ID and field-presence indicators. Bar Amra additionally retains supplied image number, facsimile page and original reference.

`has_english` indicates that a field exists, not that a complete or accepted translation exists. Placeholders remain source records. A null folio is unknown, not a missing historical leaf.

`works.json` holds source credits, source revision dates, links, scope, subject tags and project identifiers. `catalogue.json` preserves the 121-item historical inventory and appends the dated entries in `catalogue-additions.json`: two Bar Amra revision links and the 28 October 2026 Nanzhao study. The importer reads that supplement rather than discarding later research additions. The original inventory dates are unchanged.

Later catalogue entries may add `date` (publication/completion date), `pages`, `prepared_for`, `bibliography`, `description`, `subjects` and `research_id`. Source search includes the title, filename, category, date, bibliography, description and subjects. `category` retains the existing inventory classification; subject tags provide multiple research categories without changing earlier entries.

`research.json` retains the earlier dossier's `title`, `status`, `claims` and `sources` unchanged. The separate `studies` array links each attributed summary to a catalogue `source_id`; its claims distinguish source observations from hypotheses, with report-page locators. These assessments are not manuscript confidence ratings. The dated 26 October import report remains a record of that earlier import; the current source count comes from the catalogue.

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
