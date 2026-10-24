const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const C=require('../dist/core.js');
const manifest=JSON.parse(fs.readFileSync(path.join(__dirname,'../dist/data/source-manifest.json')));
const anchors=manifest.anchors.map(a=>a.id);
const note=(text,updated='2026-10-23T12:00:00.000Z')=>({id:'page-10',text,updated});
test('Romanized search tolerates diacritics without erasing Ahom vowels',()=>{
 assert.equal(C.matches('mithila',['Mithilā']),true);
 assert.notEqual(C.fold('𑜀𑜩'),C.fold('𑜀𑜧'));
 assert.equal(C.matches('1v fowl',['1v-4','fowl']),true);
});
test('Page navigation rejects missing, negative, fractional and outside pages',()=>{
 for(const v of [null,'',0,-1,395,'abc','4.5','Infinity'])assert.equal(C.pageNumber(v,394,0),0);
 assert.equal(C.pageNumber('394',394,0),394);
});
test('Notebook export can round-trip through validation with Unicode',()=>{
 const data={...C.emptyNotebook(),notes:[note('Compare 𑜀𑜩 with the original.')],bookmarks:[{id:'page-10',page:10}]};
 assert.deepEqual(C.validateNotebook(JSON.parse(JSON.stringify(data)),anchors),data);
});
test('Malformed imports fail before existing records can be changed',()=>{
 const n={...C.emptyNotebook(),notes:[note('x'),note('duplicate')]};
 assert.throws(()=>C.validateNotebook(n,anchors));
 assert.throws(()=>C.validateNotebook({...C.emptyNotebook(),bookmarks:[{id:'page-999',page:999}]},anchors));
 assert.throws(()=>C.validateNotebook({...C.emptyNotebook(),notes:[{id:'anchor-ab-p999-99',text:'x',updated:new Date().toISOString()}]},anchors));
 assert.throws(()=>C.validateNotebook({...C.emptyNotebook(),notes:[note('x','broken-date')]},anchors));
});
test('Merge keeps newer note and combines bookmarks without duplicates',()=>{
 const a={...C.emptyNotebook(),notes:[note('new')],bookmarks:[{id:'page-10',page:10}]};
 const b={...C.emptyNotebook(),notes:[note('old','2026-10-22T12:00:00Z')],bookmarks:[{id:'page-10',page:10},{id:'page-13',page:13}]};
 const merged=C.mergeNotebooks(a,b);assert.equal(merged.notes[0].text,'new');assert.equal(merged.bookmarks.length,2);assert.equal(a.bookmarks.length,1);
});
test('Notes cannot inject executable HTML into rendered cards',()=>{
 assert.equal(C.escapeHtml('<img src=x onerror="alert(1)">'), '&lt;img src=x onerror=&quot;alert(1)&quot;&gt;');
});
test('Provenance does not promote source anchors to translated passages',()=>{
 assert.equal(manifest.pages,394);assert.equal(manifest.anchors.length,12);
 assert.ok(manifest.anchors.every(a=>a.transcription===null&&a.translation===null&&a.status==='Source anchor'));
});
