#!/usr/bin/env python3
"""Validate the publication boundary, source index and Bar Amra coverage."""
import collections
import json
import re
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(name): return json.loads((ROOT/'data'/name).read_text())
works=read('works.json')
records=[r for w in works for r in read('index/'+w['id']+'.json')]
assert len(records)==4637 and len({r['id'] for r in records})==4637
assert {w['id']:w['records'] for w in works}==dict(collections.Counter(r['work'] for r in records))
for r in records:
    assert not {'layers','english','ahom','headword_unicode','assamese_unicode','source_record','alternatives'} & r.keys(),r['id']
    assert r['confidence'] in ('B','C','unreviewed')
    assert r['work']=='bar-amra' or r['folio'] is None
    assert re.fullmatch(r'[a-z-]+:[0-9]+(?:[rv]-[0-9]+(?:-[a-z0-9]+)?)?',r['id']),r['id']
coverage=read('bar-amra-coverage.json')
assert len(coverage['folios'])==61
assert sum(f['recovered_entries'] for f in coverage['folios'])==1236
assert [f['folio'] for f in coverage['folios'] if not f['recovered_entries']]==['1r','10r','26r','26v']
assert len(coverage['gaps'])==65
assert sum(g['kind']=='numbered_gap' and g['status']=='unresolved' for g in coverage['gaps'])==55
assert sum(g['kind']=='whole_folio' for g in coverage['gaps'])==4
bar=[r for r in records if r['work']=='bar-amra']
assert collections.Counter(r['confidence'] for r in bar)=={'B':819,'C':417}
assert sum(r['headword_confidence']=='A' for r in bar)==4
assert sum('unresolved-glyph' in r['flags'] for r in records if r['work']=='ma-likha')==5
catalogue=read('catalogue.json')
assert len(catalogue)==124
assert len({s['id'] for s in catalogue})==124
assert all(s['url'].startswith('https://drive.google.com/') for s in catalogue)
additions=read('catalogue-additions.json')
assert catalogue[121:]==additions and len(additions)==3
sources={s['id']:s for s in catalogue}
studies=read('research.json')['studies']
assert len({s['id'] for s in studies})==len(studies)
for study in studies:
    source=sources[study['source_id']]
    assert source['research_id']==study['id'] and source['publication']=='link-only'
    assert source['bibliography'] and source['description'] and source['subjects']
    assert {c['category'] for c in study['claims']}=={'observation','hypothesis'}
nanzhao=next(s for s in studies if s['id']=='tai-ahom-nanzhao')
source=sources[nanzhao['source_id']]
assert source['id']=='1_FhHnRLXQVE4gyfxnVRxzDeVyU0t1Z_W'
assert source['date']=='2026-10-28' and source['pages']==32
assert source['url']=='https://drive.google.com/file/d/1_FhHnRLXQVE4gyfxnVRxzDeVyU0t1Z_W/view'
assert {c['label'] for c in nanzhao['claims']}=={'Documented regional evidence','Plausible historical connections','Unverified genealogy'}
assert 'PRIVATE_READING_PACK =' not in (ROOT/'dist/reading-data.js').read_text()
class Assets(HTMLParser):
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='script' or (tag=='link' and attrs.get('rel')=='stylesheet'):
            url=attrs['src' if tag=='script' else 'href']
            version=json.loads((ROOT/'package.json').read_text())['version']
            assert url.endswith('?v='+version),f'Unversioned release asset: {url}'
            assert (ROOT/'dist'/url.split('?')[0]).is_file(),url
Assets().feed((ROOT/'dist/index.html').read_text())
for file in (ROOT/'dist').rglob('*'):
    assert file.suffix.lower() not in {'.pdf','.epub','.webp','.jpg','.jpeg'},f'Unexpected published source image: {file}'
    if file.is_file() and file.suffix in {'.js','.html','.css'}:
        assert 'se=2026-' not in file.read_text(),f'Unexpected temporary download credential: {file}'
print('PASS: 4,637 unique locators; 124 links; research references, coverage, confidence and public-content boundary.')
