#!/usr/bin/env python3
"""Read the four supplied archives without executing them; emit metadata and a private reading pack.

Usage: python3 scripts/import_collection.py INPUT_DIRECTORY PRIVATE_OUTPUT_DIRECTORY
INPUT_DIRECTORY contains unicode.zip, ming.zip, baramra.zip and catalogue.json.
No network access. No automatic translation. Public files never contain the imported readings.
"""
import collections
import hashlib
import json
import re
import sys
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-10-26'

def read_json(z, path):
    return json.loads(z.read(path))

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')

def drive(file_id):
    return f'https://drive.google.com/file/d/{file_id}/view'

def private_use(text):
    return any(0xE000 <= ord(c) <= 0xF8FF or 0xF0000 <= ord(c) <= 0xFFFFD or 0x100000 <= ord(c) <= 0x10FFFD for c in text)

def main(inputs, private):
    catalogue = json.loads((inputs / 'catalogue.json').read_text())
    assert len(catalogue) == 121
    assert sum(x['mime_type'] == 'application/pdf' for x in catalogue) == 118
    bibliographical = []
    for row in catalogue:
        title = row['title'].rsplit('.', 1)[0].replace('_', ' ')
        bibliographical.append({'id': row['id'], 'title': title, 'filename': row['title'], 'format': row['mime_type'],
            'category': row['category'], 'url': row['url'], 'catalogued_on': '2026-10-14',
            'access': 'Existing Drive permissions apply', 'publication': 'link-only'})
    # Keep later research additions when rebuilding the dated 121-item inventory.
    bibliographical.extend(json.loads((ROOT / 'data/catalogue-additions.json').read_text()))
    works, records, originals = [], [], {}
    titles = {'ming': 'Ming Mvng Lung Phai', 'nemi': 'Nemi Mang Phura', 'pvn': 'Pvn Ko Mvng', 'ma_likha': 'Ma Likha Lit', 'lakni': 'Lakni', 'kham_kau': 'Kham Kau Phi Dam'}
    subjects = {'ming': ['ritual', 'spirits', 'warfare'], 'nemi': ['Buddhism', 'Jataka', 'narrative'], 'pvn': ['creation', 'cosmology'], 'ma_likha': ['court poetry'], 'lakni': ['calendar', 'divination'], 'kham_kau': ['ritual', 'oral tradition']}
    counts = {'ming': 551, 'nemi': 1653, 'pvn': 536, 'ma_likha': 460, 'lakni': 191, 'kham_kau': 10}
    with ZipFile(inputs / 'unicode.zip') as uz, ZipFile(inputs / 'ming.zip') as mz:
        for key in titles:
            if key == 'ming':
                rows = read_json(mz, 'Ming_Mvng_Lung_Phai_Unicode/tmp/passages_unicode.json')
                config = {'credits': 'English readings and source transcription inherited from the supplied Unicode working edition. Individual translator attribution must be checked in the linked analytical source.',
                    'scope': '551 numbered entries in the supplied edition. Twenty-eight uncertain-reading labels retained; encoding restoration does not certify readings.',
                    'english_basis': 'Existing English readings retained unchanged.',
                    'additional_notes': ['Source audit restores the ending of entries 496 and 551; other 549 Ahom sequences match the analytical source. No new translation is claimed.']}
            else:
                rows = read_json(uz, key + '/Unicode_Master.json')
                config = read_json(uz, key + '/config.json')
            assert len(rows) == counts[key]
            originals[key] = rows
            prefix = titles[key].replace(' ', '_')
            edition = next(x for x in catalogue if x['title'].startswith(prefix + '_Unicode_Bilingual')) if key != 'ming' else next(x for x in catalogue if x['title'].startswith('Ming_Mvng_Lung_Phai_Unicode_Bilingual'))
            source = next(x for x in catalogue if x['title'].startswith(prefix + '_Analytical_Source'))
            wid = key.replace('_', '-')
            works.append({'id': wid, 'title': titles[key], 'identifier': 'TAH-' + key.upper().replace('_', '-'),
                'identifier_type': 'Project identifier, not an archival shelfmark', 'kind': 'oral ritual' if key == 'kham_kau' else 'working edition',
                'records': len(rows), 'subjects': subjects[key], 'source_date': '2026-10-14', 'credits': config['credits'],
                'scope': config['scope'], 'notes': config.get('additional_notes', []), 'translation_basis': config['english_basis'],
                'edition_url': edition['url'], 'source_url': source['url'], 'source_id': source['id'], 'publication': 'metadata-only',
                'folio_mapping': 'Not supplied at record level. Analytical-source page numbers are not manuscript folios.'})
            for row in rows:
                ahom, english = row.get('ahom', ''), row.get('english', '')
                flags = []
                if not re.search(r'[\U00011700-\U0001174F]', ahom): flags.append('no-ahom-text')
                if '[unresolved-50]' in ahom: flags.append('unresolved-glyph')
                if re.search(r'uncertain|unresolved|damaged|placeholder|no (?:standalone|independent)|not translated', english, re.I): flags.append('source-warning')
                if not english.strip(): flags.append('no-english-text')
                if row.get('source_change') not in (None, 'none'): flags.append('encoding-restoration')
                records.append({'id': f'{wid}:{row["n"]}', 'work': wid, 'source_record_id': str(row['n']), 'folio': None,
                    'source_page': row.get('source_page'), 'confidence': 'unreviewed', 'headword_confidence': None,
                    'flags': flags, 'source_id': source['id'], 'has_ahom': bool(re.search(r'[\U00011700-\U0001174F]', ahom)),
                    'has_english': bool(english.strip()), 'layers': {'inherited_transcription': ahom, 'english': english,
                    'editorial_reconstruction': None, 'interpretation': None}, 'notes': [], 'source_record': row,
                    'reading_status': 'Inherited working-edition reading; no new philological certification'})
    with ZipFile(inputs / 'baramra.zip') as bz:
        rows = read_json(bz, 'output/working/Transcription_Master.json')
        coverage = read_json(bz, 'output/working/Coverage_Summary.json')
        folios = read_json(bz, 'output/working/Folio_Register.json')
        gaps = read_json(bz, 'output/working/Gap_Register_20261019.json')
        provenance = read_json(bz, 'output/working/Source_Provenance.json')
    originals['bar-amra'] = rows
    assert len(rows) == 1236
    works.append({'id': 'bar-amra', 'title': 'Bar Amra', 'identifier': 'TAH-BA-JSP', 'identifier_type': 'Project identifier for the working witness',
        'kind': 'lexicon', 'records': 1236, 'subjects': ['lexicography', 'Assamese', 'language contact'], 'source_date': '2026-10-19',
        'credits': 'Inherited readings from the Ahom Dictionary Resource Project and manuscript-referenced SEAlang dictionary supplements; Zeenat Tabassum and Stephen Morey (2010) for two additions.',
        'scope': '1,236 recovered records aligned to 61 supplied images. Four whole folios remain untranscribed; 55 numbered IDs lack accepted readings. No complete entry has confidence A.',
        'notes': ['Tai-Ahom headwords and Assamese explanations written in Ahom script are separate language fields.', 'The four A-rated headwords do not certify their entire entries.', 'Image sequence is not a folio number. EAP373/26/2 canvas 3 matches 1r; canvas 21 matches 10r. No replacement for 26r/26v was established.'],
        'translation_basis': 'Inherited English lexical glosses; unresolved senses remain unresolved.', 'edition_url': drive('16MoqMHeFUkVkadew5LQm473ZmGJsTUP0'),
        'source_url': 'http://sealang.net/archives/ahom/jp.htm', 'source_id': 'bar-amra-source', 'publication': 'metadata-only', 'folio_mapping': 'Explicit folio, image and facsimile-page mappings preserved from the revised source register.'})
    for row in rows:
        flags = []
        if 'Partial' in row.get('coverage', ''): flags.append('partial-record')
        if row['confidence'] == 'C': flags.append('uncertain')
        if row.get('revision_added'): flags.append('added-2026-10-19')
        records.append({'id': 'bar-amra:' + row['id'], 'work': 'bar-amra', 'source_record_id': row['id'], 'folio': row['folio'],
            'source_reference': row.get('source_reference'), 'image': row['image'], 'facsimile_page': row['facsimile_pdf_page'],
            'source_page': None, 'confidence': row['confidence'], 'headword_confidence': row.get('headword_confidence'), 'flags': flags,
            'source_id': 'bar-amra-source', 'has_ahom': bool(row.get('headword_unicode')), 'has_english': bool(row.get('english')),
            'layers': {'inherited_transcription': row.get('headword_unicode', ''), 'formula': row.get('formula_unicode', ''),
                'assamese_in_ahom_script': row.get('assamese_unicode', ''), 'punctuation': row.get('punctuation_unicode', ''),
                'english': row.get('english', ''), 'romanization': row.get('headword_roman', ''), 'assamese_romanization': row.get('assamese_roman', ''),
                'editorial_reconstruction': None, 'interpretation': None}, 'notes': row.get('notes', []), 'source_record': row,
            'reading_status': row.get('review', '')})
    assert len(records) == 4637
    assert len({r['id'] for r in records}) == len(records)
    for r in records:
        for field in ('inherited_transcription', 'formula', 'assamese_in_ahom_script', 'punctuation'):
            value = r['layers'].get(field) or ''
            assert not private_use(value) and '\ufffd' not in value, (r['id'], field)
    public_fields = ('id', 'work', 'source_record_id', 'folio', 'source_page', 'confidence', 'headword_confidence', 'flags', 'source_id', 'has_ahom', 'has_english', 'source_reference', 'image', 'facsimile_page')
    index = [{k: r[k] for k in public_fields if k in r} for r in records]
    safe_gaps = []
    for g in gaps:
        safe_gaps.append({k: g[k] for k in ('id', 'kind', 'image', 'facsimile_pdf_page', 'status') if k in g})
    safe_folios = [{k: f[k] for k in ('image', 'folio', 'facsimile_pdf_page', 'recovered_entries', 'missing_numbered_entries')} for f in folios]
    fingerprints = [{'file': p.name, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in (inputs / 'unicode.zip', inputs / 'ming.zip', inputs / 'baramra.zip', inputs / 'catalogue.json')]
    pack = {'schema': 'tai-ahom-reading-pack', 'version': 1, 'created': DATE, 'publication': 'private-research-only',
        'notice': 'Derived from the user-provided collection. No redistribution permission is granted. Keep this file outside public repositories.',
        'source_fingerprints': fingerprints, 'records': records}
    private.mkdir(parents=True, exist_ok=True)
    dump(private / 'Tai_Ahom_Reading_Pack_20261026.json', pack)
    for key, value in originals.items(): dump(private / 'masters' / (key + '.json'), value)
    dump(private / 'masters' / 'Bar_Amra_Source_Provenance.json', provenance)
    dump(ROOT / 'data/catalogue.json', bibliographical)
    dump(ROOT / 'data/works.json', works)
    # Split public index for readable Git history and bounded uploads.
    for w in works: dump(ROOT / 'data/index' / (w['id'] + '.json'), [r for r in index if r['work'] == w['id']])
    dump(ROOT / 'data/bar-amra-coverage.json', {'summary': coverage, 'folios': safe_folios, 'gaps': safe_gaps})
    dump(ROOT / 'data/source-fingerprints.json', fingerprints)
    report = {'date': DATE, 'records': len(records), 'works': len(works), 'historical_catalogue_items': 121, 'historical_catalogue_pdfs': 118,
        'current_linked_items': len(bibliographical), 'bar_amra_confidence': dict(collections.Counter(r['confidence'] for r in rows)),
        'bar_amra_missing_ids': sum(g['kind'] == 'numbered_gap' and g['status'] == 'unresolved' for g in gaps),
        'bar_amra_untranscribed_folios': [g['id'] for g in gaps if g['kind'] == 'whole_folio'], 'new_translation_claimed': False,
        'public_readings_published': 0, 'unicode_pua_or_replacement_characters': 0, 'original_rows_preserved': True}
    dump(ROOT / 'data/import-report.json', report)
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    if len(sys.argv) != 3: raise SystemExit(__doc__)
    main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
