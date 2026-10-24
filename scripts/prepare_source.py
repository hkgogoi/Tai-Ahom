#!/usr/bin/env python3
"""Render the supplied Ahom-Buranji scan; retain source identity and page order."""
import argparse, hashlib, json
from pathlib import Path
import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ANCHORS = [
 ('ab-p001-01',7,1,'Opening passage · §1',[.02,.23,.48,.36]),
 ('ab-p001-02',7,1,'Opening passage · §2',[.02,.365,.48,.480]),
 ('ab-p001-03',7,1,'Opening passage · §3',[.02,.486,.48,.565]),
 ('ab-p001-04',7,1,'Opening passage · §4',[.02,.575,.48,.740]),
 ('ab-p001-05',7,1,'Opening passage · §5',[.02,.816,.48,.95]),
 ('ab-p004-10',10,4,'Mungthila context · §10',[.02,.063,.48,.275]),
 ('ab-p004-11',10,4,'Genealogical passage · §11',[.02,.312,.48,.57]),
 ('ab-p004-12',10,4,'Descent passage · §12',[.02,.58,.48,.68]),
 ('ab-p004-13',10,4,'Bithila context · §13',[.02,.680,.48,.800]),
 ('ab-p007-05',13,7,'Shared-throne context · §5',[.02,.12,.48,.45]),
 ('ab-p007-06',13,7,'Envoy passage · §6',[.02,.503,.48,.715]),
 ('ab-p007-07',13,7,'Reception passage · §7',[.02,.725,.48,.90]),
]

def render(pdf_path, anchors_only=False):
    source = Path(pdf_path)
    doc = fitz.open(source)
    pages = ROOT / 'dist/pages'
    passages = ROOT / 'dist/assets/passages'
    pages.mkdir(parents=True,exist_ok=True); passages.mkdir(parents=True,exist_ok=True)
    for i,page in enumerate(doc):
        if anchors_only: break
        out=pages/f'{i+1:03d}.webp'
        scale=850/page.rect.width
        pix=page.get_pixmap(matrix=fitz.Matrix(scale,scale),colorspace=fitz.csGRAY)
        Image.frombytes('L',(pix.width,pix.height),pix.samples).save(out,'WEBP',quality=68,method=4)
        if (i+1)%80==0: print(f'Rendered {i+1}/{len(doc)}',flush=True)
    records=[]
    for ident,pno,printed,title,box in ANCHORS:
        page=doc[pno-1]; w,h=page.rect.width,page.rect.height
        clip=fitz.Rect(box[0]*w,box[1]*h,box[2]*w,box[3]*h)
        pix=page.get_pixmap(matrix=fitz.Matrix(3,3),clip=clip,colorspace=fitz.csGRAY)
        Image.frombytes('L',(pix.width,pix.height),pix.samples).save(passages/f'{ident}.webp','WEBP',quality=88)
        records.append({'id':ident,'scanPage':pno,'printedPage':printed,'label':title,'image':f'assets/passages/{ident}.webp','bbox':box,'status':'Source anchor','transcription':None,'translation':None,'review':'Crop location checked against the supplied printed scan. Unicode transcription and independent translation are not yet certified.'})
    manifest={'title':'Ahom-Buranji','editor':'Golap Chandra Barua','year':1930,'sourceType':'Original-language printed edition with parallel English','pages':len(doc),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'pageImageWidth':850,'pageImageFormat':'webp','sourceUrl':'https://archive.org/details/in.ernet.dli.2015.450867','verifiedPrintedLabels':{'7':'1','10':'4','13':'7','16':'10','26':'20'},'anchors':records}
    (ROOT/'dist/data/source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    print(json.dumps({'pages':len(doc),'anchors':len(records),'imageMB':round(sum(x.stat().st_size for x in pages.iterdir())/1024**2,2)}))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('pdf');parser.add_argument('--anchors-only',action='store_true');args=parser.parse_args();render(args.pdf,args.anchors_only)
