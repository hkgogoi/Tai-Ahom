#!/usr/bin/env python3
"""Validate the publication boundary, source index and Bar Amra coverage."""
import collections
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from build import verify_document
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
assert len(catalogue)==126
assert len({s['id'] for s in catalogue})==126
additions=read('catalogue-additions.json')
assert catalogue[121:]==additions and len(additions)==5
sources={s['id']:s for s in catalogue}
documents=read('public-documents.json')
dist=ROOT/'dist'
assert documents and documents.keys() <= sources.keys()
assert len({d['filename'] for d in documents.values()})==len(documents)
expected_documents=set()
for source_id, document in documents.items():
    assert sources[source_id]['format']=='application/pdf'
    assert re.fullmatch(r'[a-z0-9-]+\.pdf',document['filename'])
    assert document['rights'] and document['credit']
    assert all(url.startswith('https://') and 'drive.google.com' not in url for url in document.get('origins', []))
    path=dist/'documents'/document['filename']
    verify_document(path, document)
    expected_documents.add(path)
public_data=(dist/'catalogue-data.js').read_text(encoding='utf-8')
public_catalogue=json.loads(public_data.removeprefix('window.ARCHIVE = ').removesuffix(';\n'))['catalogue']
assert len(public_catalogue)==len(catalogue)
assert {source['id']:source['download']['href'] for source in public_catalogue if 'download' in source}=={
    source_id:'documents/'+document['filename'] for source_id,document in documents.items()
}
assert all('url' not in source for source in public_catalogue)
for work in works:
    assert work['edition_id'] in sources
    assert work.get('source_url') or work['source_id'] in sources
for source in catalogue:
    related=source.get('related_source_ids',[])
    assert len(related)==len(set(related)) and source['id'] not in related
    assert all(sid in sources for sid in related)
studies=read('research.json')['studies']
assert len({s['id'] for s in studies})==len(studies)
for study in studies:
    source=sources[study['source_id']]
    assert source['research_id']==study['id'] and source['id'] in documents
    assert source['bibliography'] and source['description'] and source['subjects']
    assert {c['category'] for c in study['claims']}=={'observation','hypothesis'}
nanzhao=next(s for s in studies if s['id']=='tai-ahom-nanzhao')
source=sources[nanzhao['source_id']]
assert source['id']=='1_FhHnRLXQVE4gyfxnVRxzDeVyU0t1Z_W'
assert source['date']=='2026-10-28' and source['pages']==32
assert {c['label'] for c in nanzhao['claims']}=={'Documented regional evidence','Plausible historical connections','Unverified genealogy'}
for sid,pages,research_id in [
    ('1U4IjtMHnzWU6TEysVibvMow2yO_6ibz6',9,'ahom-chinese-coin-report'),
    ('1CwUu79NjBFvqEbm5AFzvcvEarN1aNrLC',15,'ahom-chinese-coin-supplement'),
]:
    source=sources[sid]
    assert source['date']=='2026-10-29' and source['pages']==pages
    assert source['catalogued_on']=='2026-11-01'
    assert source['research_id']==research_id
    assert {'1rtU1igWWyxK_bFQ-2_ZVlAv3JGr3tdpc','1sf8-bRc5whuxgWyMCJ_oXqSgD7-PbLtx'}<=set(source['related_source_ids'])
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
    if file.suffix.lower() in {'.pdf','.epub','.webp','.jpg','.jpeg','.zip'}:
        assert file in expected_documents,f'Unlisted public document or image: {file}'
    if file.is_file() and file.suffix in {'.js','.html','.css'}:
        page=file.read_text(encoding='utf-8').lower()
        assert not re.search(r'https?://(?:drive|docs)\.google\.com/',page),f'Unexpected Drive link: {file}'
        assert 'se=2026-' not in page,f'Unexpected temporary download credential: {file}'
print(f'PASS: 4,637 locators; 126 catalogue records; {len(documents)} verified public downloads; coverage and research preserved.')
