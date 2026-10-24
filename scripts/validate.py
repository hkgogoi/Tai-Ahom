#!/usr/bin/env python3
"""Dependency-free validation for publication and future edits."""
from pathlib import Path
import hashlib,json,re,sys
root=Path(__file__).resolve().parents[1];dist=root/'dist'
errors=[]
manifest=json.loads((dist/'data/source-manifest.json').read_text())
lexicon=json.loads((dist/'data/lexicon.json').read_text())
research=json.loads((dist/'data/research.json').read_text())
for i in range(1,manifest['pages']+1):
 p=dist/'pages'/f'{i:03d}.webp'
 if not p.is_file() or p.stat().st_size<100:errors.append(f'Missing or empty scan {i}')
for a in manifest['anchors']:
 if not (dist/a['image']).is_file():errors.append(f'Missing anchor {a["id"]}')
 if not 1<=a['scanPage']<=manifest['pages']:errors.append('Anchor page out of range')
 if a['translation'] is not None:errors.append('Source-only release unexpectedly contains an asserted fresh translation')
ids=[x['id'] for x in lexicon]
if len(ids)!=len(set(ids)):errors.append('Duplicate lexical ID')
for x in lexicon:
 if not any(0x11700<=ord(c)<=0x1174f for c in x['script']):errors.append(f'No Ahom codepoints in {x["id"]}')
 if any(0xe000<=ord(c)<=0xf8ff for c in x['script']+x['explanation']):errors.append('Private-use encoding in lexical data')
 if not x['source']:errors.append('Missing lexical provenance')
source_ids={s['id'] for s in research['sources']}
for c in research['claims']:
 if not set(c['sources']).issubset(source_ids):errors.append('Unknown dossier source')
for path in ['index.html','styles.css','app.js','core.js','data.js','sw.js','manifest.webmanifest','assets/mark.svg','assets/NotoSerifAhom-Regular.ttf','assets/OFL-Ahom.txt','assets/icon-192.png','assets/icon-512.png']:
 if not (dist/path).is_file() or (dist/path).stat().st_size==0:errors.append(f'Missing asset {path}')
for file in [dist/'index.html',dist/'styles.css']:
 content=file.read_text()
 for target in re.findall(r'(?:src|href)=["\']([^"\']+)',content):
  if target.startswith(('http','#','data:')):continue
  if not(dist/target).exists():errors.append(f'Broken file link: {target}')
 if '/workspace/' in content:errors.append('Local workspace path leaked into site')
if errors:
 print('\n'.join(errors));sys.exit(1)
total=sum(p.stat().st_size for p in dist.rglob('*') if p.is_file())
print(f'PASS: {manifest["pages"]} source images; {len(manifest["anchors"])} source anchors; {len(lexicon)} lexical records; {len(research["claims"])} evidence records; {total/1024**2:.2f} MiB site.')
