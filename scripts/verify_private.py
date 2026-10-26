#!/usr/bin/env python3
"""Compare every retained source object and normalized text field with supplied archives."""
import json
import sys
from pathlib import Path
from zipfile import ZipFile
inputs,pack_path=map(Path,sys.argv[1:3])
pack=json.loads(pack_path.read_text());records={r['id']:r for r in pack['records']}
checked=0
with ZipFile(inputs/'unicode.zip') as z:
    for key in ('nemi','pvn','ma_likha','lakni','kham_kau'):
        for original in json.loads(z.read(key+'/Unicode_Master.json')):
            r=records[key.replace('_','-')+':'+str(original['n'])]
            assert r['source_record']==original
            assert r['layers']['inherited_transcription']==original['ahom']
            assert r['layers']['english']==original['english']
            checked+=1
with ZipFile(inputs/'ming.zip') as z:
    for original in json.loads(z.read('Ming_Mvng_Lung_Phai_Unicode/tmp/passages_unicode.json')):
        r=records['ming:'+str(original['n'])]
        assert r['source_record']==original
        assert r['layers']['inherited_transcription']==original['ahom']
        assert r['layers']['english']==original['english']
        checked+=1
with ZipFile(inputs/'baramra.zip') as z:
    originals=json.loads(z.read('output/working/Transcription_Master.json'))
    baseline=json.loads(z.read('sources/baseline_20261014/Transcription_Master.json'))
    by_id={r['id']:r for r in originals}
    assert all(by_id[r['id']]==r for r in baseline)
    for original in originals:
        r=records['bar-amra:'+original['id']]
        assert r['source_record']==original
        for target,source in [('inherited_transcription','headword_unicode'),('english','english'),('assamese_in_ahom_script','assamese_unicode'),('formula','formula_unicode')]:
            assert r['layers'][target]==original.get(source,'')
        checked+=1
assert checked==4637
print('PASS: every original record and normalized reading preserved; all 1,230 baseline Bar Amra objects unchanged.')
