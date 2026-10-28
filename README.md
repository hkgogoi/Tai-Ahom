# Tai-Ahom Research Atlas

A mobile-friendly research archive for the Tai-Ahom manuscript collection. Release **0.2.1**, 28 October 2026.

The repository preserves source identifiers, bibliographical references, coverage and uncertainty. It indexes **4,637 records** across seven working collections and links **124 source files**. Original manuscripts and existing Drive files are preserved.

## Public archive and private readings

**The public repository contains metadata, not the complete third-party transcriptions or scans.** The optional private reading pack contains the genuine Unicode readings and corresponding English from the user's existing collection. Load it in **Load readings**; it is searched on the device, without an upload. The private offline edition already includes it.

The collection's 14 October catalogue lists 118 PDFs and three other files. Later additions are two links to the 19 October Bar Amra revision and the 32-page [Tai-Ahom and Nanzhao research study](https://drive.google.com/file/d/1_FhHnRLXQVE4gyfxnVRxzDeVyU0t1Z_W/view), completed 28 October. These are dated inventory figures, not a claim that every linked file is publicly accessible.

Search Sources for **Nanzhao**, migration or historical geography. The catalogue includes the report's full title, date, bibliographical description and subjects. Research presents an attributed summary distinguishing documented regional contact and continuity, plausible transmission mechanisms and unverified dynastic descent. The PDF and its source plates remain linked in Drive; no redistribution permission is inferred.

| Collection | Numbered records | Source revision |
|---|---:|---|
| Ming Mvng Lung Phai | 551 | 14 October 2026 |
| Nemi Mang Phura | 1,653 | 14 October 2026 |
| Pvn Ko Mvng | 536 | 14 October 2026 |
| Ma Likha Lit | 460 | 14 October 2026 |
| Lakni | 191 | 14 October 2026 |
| Kham Kau Phi Dam | 10 | 14 October 2026 |
| Bar Amra | 1,236 | 19 October 2026 |

Kham Kau Phi Dam is an oral ritual text, not a manuscript. Lakni is a partial manuscript transcription. Record counts include source placeholders and do not imply complete translations.

## Features

- Search by collection, manuscript identifier, historical subject, entry ID, exact folio and confidence.
- Unicode Tai-Ahom, English meaning and romanization search after loading the private pack.
- Separate Tai-Ahom headwords, formulae, Assamese in Ahom script, English glosses, editorial notes and source alternatives.
- Bar Amra coverage navigator: 61 supplied images, four whole-folio gaps, 55 missing numbered IDs and six later additions.
- Stable record links, source citations, local search exports, accessible mobile layout and bundled Ahom font.
- Optional device-local storage for imported readings; no login, analytics, backend or upload endpoint.
- The earlier Lengdon–Nimi dossier is retained as an explicitly inherited interpretive layer.
- The Nanzhao study is discoverable through Sources and Research, with separate evidence and hypothesis labels.

## Run locally

Python 3.10+ and Node 18+ are sufficient. No dependencies need to be installed.

```sh
python3 scripts/build.py
python3 scripts/validate.py
node --test scripts/core.test.cjs
python3 -m http.server 8080 --directory dist
```

Open `http://localhost:8080`. The generated `dist/index.html` also supports ordinary file opening where the browser permits local scripts. For phones that restrict local HTML, use the hosted archive and load the JSON reading pack.

## GitHub Pages

Repository: <https://github.com/hkgogoi/Tai-Ahom>.

The workflow `.github/workflows/pages.yml` builds and validates metadata, runs search/import tests, then deploys `dist`. In repository **Settings → Pages**, the source must be **GitHub Actions**. Use the URL from a successful deployment; a committed workflow alone is not evidence that the site is live.

Keep the existing history. Do not force-push or delete the earlier `import/ahom-atlas` branch. It contains the prior 0.1.0 build; it was not merged because its scan derivatives and older samples need separate rights review.

## Reproduce the import

Obtain these existing user-owned working packages from the linked Drive collection and name local copies as follows:

| Local input | Existing source |
|---|---|
| `unicode.zip` | [Tai Ahom Unicode Working Package](https://drive.google.com/file/d/1fs_sNS6JYAbdd85D2PhCDVX6qhHql7gn/view) |
| `ming.zip` | [Ming Mvng Lung Phai working package](https://drive.google.com/file/d/1ykAqODvRr4EqMUllfPdAdNz1F45foAH9/view) |
| `baramra.zip` | [Bar Amra revision 2 working package](https://drive.google.com/file/d/1a2oU6jqAAHTRo2ti_vIdTNRGbuw_GvVa/view) |
| `catalogue.json` | [Collection catalogue JSON](https://drive.google.com/file/d/1_OQpNpQbBkzD1erLFKSM0uCC8Qq5d5Nh/view) |

The input files are not redistributed here. Their SHA-256 fingerprints are recorded in `data/source-fingerprints.json`.

```sh
python3 scripts/import_collection.py /absolute/path/to/inputs /absolute/path/outside-repository/private-reading
python3 scripts/verify_private.py /absolute/path/to/inputs /absolute/path/outside-repository/private-reading/Tai_Ahom_Reading_Pack_20261026.json
python3 scripts/build.py --private-pack /absolute/path/outside-repository/private-reading/Tai_Ahom_Reading_Pack_20261026.json --private-output /absolute/path/outside-repository/private-reading/offline
```

The import script reads JSON members; it does not execute any supplied archive scripts. The private output includes each original master record. No new characters or English translations are generated. The public build always emits an empty reading-data stub, even when a separate private offline copy is built.

## Repository structure

- `data/catalogue.json`: dated bibliography and links; `catalogue-additions.json` preserves post-inventory additions during re-import.
- `data/works.json`: collection IDs, source credits, scope and subject tags.
- `data/index/*.json`: public record locators and review metadata, without inherited readings.
- `data/bar-amra-coverage.json`: counts, folios and all 65 research targets.
- `data/rights.json`: source-specific publication decisions and evidence.
- `data/research.json`: the inherited historical dossier, explicitly labelled, plus separately attributed research-study summaries.
- `dist/`: mobile interface, local importer and licensed font.
- `scripts/`: deterministic build, import, preservation audit and tests.
- `schema/`: reading-pack schema; runtime validation additionally checks against known record IDs.
- `docs/`: editorial policy, rights, data model and release validation.

## Scholarly limits

Bar Amra has **819 B** and **417 C** records. Four selected headwords have A-level visual checks; **no complete entry is certified A**. Folios **1r, 10r, 26r and 26v** remain untranscribed. The 55 missing-number count concerns entry IDs, not every missing word or character. The six other editions are not assigned Bar Amra's confidence rubric.

Unicode validation establishes machine readability, not philological accuracy. Five unresolved glyph markers in Ma Likha Lit and all inherited uncertainty remain visible. The archive makes no new claim that Lengdon derives from Nimi or that any unverified translation has been completed.

## Rights and privacy

See [rights review](docs/RIGHTS.md) and [editorial policy](docs/EDITORIAL.md). Application code is MIT; Noto Serif Ahom uses its bundled SIL Open Font License. Neither licence extends to source transcriptions, translations, scans or papers. **Never place the private reading directory in a public Git repository.**
