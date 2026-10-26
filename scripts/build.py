#!/usr/bin/env python3
"""Assemble the buildless public site from metadata. Optional private output never changes dist."""
import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(name): return json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--private-pack',type=Path)
    parser.add_argument('--private-output',type=Path)
    args=parser.parse_args()
    if bool(args.private_pack) != bool(args.private_output): parser.error('Private pack and private output must be provided together.')
    data={'version':'0.2.0','date':'2026-10-26','works':load('works.json'),'catalogue':load('catalogue.json'),
          'coverage':load('bar-amra-coverage.json'),'research':load('research.json'),'rights':load('rights.json'),'report':load('import-report.json')}
    dist=ROOT/'dist'
    (dist/'catalogue-data.js').write_text('window.ARCHIVE = '+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n')
    records=[]
    for w in data['works']: records.extend(load('index/'+w['id']+'.json'))
    (dist/'records-data.js').write_text('window.RECORD_INDEX = '+json.dumps(records,ensure_ascii=False,separators=(',',':'))+';\n')
    (dist/'reading-data.js').write_text('// Public build: reading texts are loaded locally by the researcher.\n')
    (dist/'.nojekyll').write_text('')
    if args.private_pack:
        output=args.private_output.resolve()
        if output==dist.resolve() or ROOT.resolve() in output.parents: parser.error('Private output must be outside the repository.')
        pack=json.loads(args.private_pack.read_text(encoding='utf-8'))
        assert pack['schema']=='tai-ahom-reading-pack' and pack['version']==1
        shutil.copytree(dist,output,dirs_exist_ok=True)
        (output/'reading-data.js').write_text('window.PRIVATE_READING_PACK = '+json.dumps(pack,ensure_ascii=False,separators=(',',':'))+';\n')
    print(f'Built public metadata: {len(records)} locators; {len(data["catalogue"])} source links. No reading texts included in dist.')
if __name__=='__main__': main()
