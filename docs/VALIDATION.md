# Release validation

Release 0.1.0, prepared 23 October 2026.

## Automated checks

- `node --check dist/app.js`: passed.
- `node --test scripts/core.test.cjs`: seven tests passed. These cover Latin diacritic search without stripping Ahom vowel marks, page bounds, Unicode notebook backups, malformed imports, merge precedence, HTML escaping, and explicit untranslated source fields.
- `python3 scripts/validate.py`: passed. All 394 page images, 12 passage anchors, 12 lexical records and six evidence cards are present. Source references and required assets resolve within the package.

## Browser checks

Checked in the available Chromium browser using a local HTTP preview:

- Desktop overview, collection, reader, lexicon and research views.
- Overview, reader and lexicon at a 390-pixel content width.
- Ahom Unicode font rendering and source-passage crops.
- Reading-page navigation, selected-passage views and bookmarking.
- Note creation, persistence after reload, deletion and session undo.
- JSON notebook export, file import and merge; one test note and bookmark survived the round trip.
- Research filtering, including the open-hypothesis card.

Temporary test notes and bookmarks were removed. Browser logs inspected at the end showed browser-extension metadata errors; no application-origin errors appeared in that inspected log window.

## Limits and publication status

- The complete image inventory is validated; only selected pages and the twelve passage crops received visual review.
- No whole Ahom-Buranji passage has been independently certified as transcribed or freshly translated. Null transcription and translation fields are intentional.
- The lexical examples retain inherited review status. Their Assamese explanation text is distinguished from the Ahom headwords.
- Real-device Android testing and offline network simulation have not been performed. The service worker caches only visited pages, not the entire scan.
- The GitHub Pages workflow is supplied for the existing hkgogoi/Tai-Ahom repository. The current publication result is recorded in the repository Actions tab; presence of the workflow alone does not certify a successful deployment.

Research claims and their evidential limits are documented in `EDITORIAL.md` and in the website's source notes.

## Recovery verification — 24 October 2026

The saved v1 ZIP was recovered for publication to `hkgogoi/Tai-Ahom`. Its 434 files include 394 scan images, twelve passage crops, and the application. The source-image and data validator passed, all seven notebook/search tests passed, JavaScript syntax passed, and Pillow successfully decoded all 408 WebP/PNG images. Repository references were corrected to `Tai-Ahom`; the Bar Amra samples are explicitly identified as the 14 October snapshot.

The browser checks above are the original package validation record. A new local visual check was not completed in the recovery environment: no browser executable was available, its download failed, and the separate browser could not reach the local preview. Real-device Android and offline simulation remain unchecked.
