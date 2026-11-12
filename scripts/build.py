#!/usr/bin/env python3
"""Assemble the buildless public site from metadata. Optional private output never changes dist."""
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
def load(name): return json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))

def verify_document(path, document):
    if path.stat().st_size != document['bytes']:
        raise ValueError(f'Unexpected size for {document["filename"]}')
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        if stream.read(5) != b'%PDF-':
            raise ValueError(f'Expected a PDF for {document["filename"]}')
        stream.seek(0)
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    if digest.hexdigest() != document['sha256']:
        raise ValueError(f'SHA-256 mismatch for {document["filename"]}')

def stage_document(dist, document):
    filename = document['filename']
    if Path(filename).name != filename or not filename.endswith('.pdf'):
        raise ValueError(f'Invalid document filename: {filename}')
    directory = dist / 'documents'
    directory.mkdir(exist_ok=True)
    target = directory / filename
    source = ROOT / 'documents' / filename
    if source.is_file():
        verify_document(source, document)
        shutil.copyfile(source, target)
        return
    if target.is_file():
        try:
            verify_document(target, document)
            return
        except ValueError:
            target.unlink()
    errors = []
    for url in document.get('origins', []):
        with TemporaryDirectory(dir=directory) as temporary:
            pending = Path(temporary)/filename
            try:
                subprocess.run([
                    'curl', '--fail', '--silent', '--show-error', '--location',
                    '--proto', '=https', '--proto-redir', '=https', '--connect-timeout', '15',
                    '--max-time', '90', '--max-filesize', str(document['bytes']),
                    '--output', str(pending), url,
                ], check=True)
                verify_document(pending, document)
                pending.replace(target)
                return
            except (subprocess.CalledProcessError, OSError, ValueError) as error:
                errors.append(f'{url}: {error}')
    raise RuntimeError(f'Could not stage {filename}: ' + ('; '.join(errors) or 'local copy missing'))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--private-pack',type=Path)
    parser.add_argument('--private-output',type=Path)
    args=parser.parse_args()
    if bool(args.private_pack) != bool(args.private_output): parser.error('Private pack and private output must be provided together.')
    version=json.loads((ROOT/'package.json').read_text(encoding='utf-8'))['version']
    data={'version':version,'date':'2026-11-12','works':load('works.json'),'catalogue':load('catalogue.json'),
          'coverage':load('bar-amra-coverage.json'),'research':load('research.json'),'rights':load('rights.json'),'report':load('import-report.json')}
    dist=ROOT/'dist'
    documents=load('public-documents.json')
    source_ids={s['id'] for s in data['catalogue']}
    if not documents.keys() <= source_ids:
        raise ValueError('A public document has no catalogue record')
    filenames={document['filename'] for document in documents.values()}
    if len(filenames)!=len(documents):
        raise ValueError('Public download filenames must be unique')
    for file in (dist/'documents').glob('*.pdf'):
        if file.name not in filenames:
            file.unlink()
    for source in data['catalogue']:
        document=documents.get(source['id'])
        if document:
            stage_document(dist, document)
            source['download']={key: document[key] for key in ('filename','bytes','credit','rights','evidence_url') if key in document}
            source['download']['href']='documents/'+document['filename']
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
    print(f'Built {len(records)} locators, {len(data["catalogue"])} catalogue records and {len(documents)} public downloads.')
if __name__=='__main__': main()
