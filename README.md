# Ahom Research Atlas

A mobile-friendly static research website for Tai-Ahom sources, lexical records, and historical evidence. Prepared 23 October 2026. Release 0.1.0.

## Included in this release

- All **394 pages** of the supplied 1930 *Ahom-Buranji* scan, preserved in scan order as WebP reading images.
- **12 original Ahom passage crops** with checked page locations. Scan numbers and printed page labels are separate.
- **12 Bar Amra lexical sample records**, with real Ahom Unicode, source explanations in Assamese written in Ahom script, and inherited confidence labels.
- A **Lengdon–Nimi Jātaka research dossier**, with six evidence cards separating observations, comparisons, and hypotheses.
- Collection and lexicon search; page navigation, zoom, full-page and left-column views; bookmarks; source-reference copying.
- Browser-local notes, dated JSON backups, validated import and merge, and deletion with session undo.
- A service worker that stores the app shell and up to 40 recently fetched source pages for reuse. Unvisited pages still need a connection.
- Portable JSON data and a GitHub Pages deployment workflow.

**This is a complete scan reader, not a completed fresh translation.** No whole Buranji passage is independently certified as transcribed or translated in this release. Pending fields are explicitly empty. Lexical samples are inherited readings, not newly certified entries. No historical derivation is presented as proved.

## Read locally

The public website is the `dist` directory. It has no build dependencies or server-side component.

From the project root:

```sh
python3 -m http.server 8080 --directory dist
```

Open `http://localhost:8080`. Stop the local server with Ctrl+C. A local HTTP server is recommended for service workers and browser features; opening `dist/index.html` directly also shows the core reader, but browser persistence and secure-context features vary.

## Publish on GitHub Pages

The project repository is [hkgogoi/Tai-Ahom](https://github.com/hkgogoi/Tai-Ahom). Publication is managed by the included workflow; check its deployment result before treating a website URL as live.

1. Use the existing public repository `hkgogoi/Tai-Ahom`.
2. Push this project's files to its `main` branch. Include `dist`, `scripts`, and `.github/workflows/pages.yml`. Do not upload only the ZIP.
3. In repository **Settings → Pages**, choose **GitHub Actions** as the build source.
4. In **Actions**, run **Publish Ahom Research Atlas**, or push a change to `main`.
5. Open the URL shown by the successful deployment. Do not assume deployment succeeded until that workflow is green.

For a machine with Git installed, from the unpacked project directory:

```sh
git init -b main
git add .
git commit -m "Create Ahom Research Atlas"
git remote add origin https://github.com/hkgogoi/Tai-Ahom.git
git push -u origin main
```

Use your normal GitHub sign-in flow. No token or password belongs in this repository or its frontend. If the repository already has commits, reconcile the histories instead of force-pushing.

The workflow uses the official GitHub Pages actions, validates the dataset and runs the notebook/search tests before deployment. The site is about 54 MiB, well below the documented 1 GiB Pages site limit. Individual page images load only when needed.

## Edit the collection

- `dist/data/source-manifest.json`: source fingerprint, image inventory, checked anchors, and explicit pending translations.
- `dist/data/lexicon.json`: the 12 attributed Bar Amra sample records.
- `scripts/build_data.py`: catalogue, research cards, source references, and static bundle assembly.
- `dist/data.js`: generated bundle used by the browser. Regenerate after editing data.
- `dist/app.js`, `core.js`, `styles.css`: reader, local notebook, navigation, search, and presentation.
- `docs/EDITORIAL.md`: editorial rules and source distinctions.
- `docs/VALIDATION.md`: release checks and publication status.

After changing source data:

```sh
python3 scripts/build_data.py
python3 scripts/validate.py
node --test scripts/core.test.cjs
```

Never fill untranslated fields by copying Barua's historical English and calling it a fresh translation. Preserve alternative readings, evidence and reviewer attribution.

## Reproduce source images

The original PDF is not duplicated in this package. Its SHA-256 fingerprint is in the source manifest. A corresponding archived source is linked in the site. To regenerate from the exact supplied scan, use Python with PyMuPDF and Pillow:

```sh
python3 scripts/prepare_source.py /absolute/path/to/ahom.pdf
python3 scripts/build_data.py
```

`--anchors-only` regenerates passage crops without rendering all 394 pages. These are viewing derivatives; preserve the original scan as the source of record.

## Privacy and access

The website has no account system, analytics script, API key, AI endpoint, or external database. Notes stay on the visitor's device until the visitor exports them. Public source data is versioned in the repository. A link to the existing Bar Amra Drive edition retains that file's existing permissions; publishing this site does not change them.

## Licensing

The newly written application code is MIT-licensed. See `LICENSE`. The bundled Noto Serif Ahom font retains the SIL Open Font License in `dist/assets/OFL-Ahom.txt`. Source scans, inherited lexical material and linked works keep their own provenance and rights; the code license does not override them. Source credits and review status appear on the site's Sources & editorial method page.
