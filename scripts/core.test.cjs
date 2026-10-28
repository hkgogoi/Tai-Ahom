const {test}=require('node:test');
const assert=require('node:assert/strict');
const C=require('../dist/core.js');
const fs=require('node:fs');
const path=require('node:path');
const A=String.fromCodePoint(0x11700,0x11727),B=String.fromCodePoint(0x11700,0x11726);
const works=[{id:'test',title:'Test manuscript',identifier:'TEST',subjects:['ritual']}];
const index=[{id:'test:1',work:'test',source_record_id:'1',folio:'1r',confidence:'B',headword_confidence:'A'},
{id:'test:2',work:'test',source_record_id:'2',folio:'11r',confidence:'C',headword_confidence:'C'}];
const rows=index.map((r,i)=>({...r,layers:{inherited_transcription:i?B:A,english:i?'water':'FOWL',assamese_in_ahom_script:i?A:B},notes:[],reading_status:'Test fixture',source_record:{fixture:true}}));
const readings=new Map(rows.map(r=>[r.id,r]));
const pack=()=>({schema:'tai-ahom-reading-pack',version:1,records:structuredClone(rows)});
test('Ahom vowel signs remain distinct',()=>{assert.notEqual(C.fold(A),C.fold(B));assert.equal(C.hasPUA(A),false);});
test('Text search includes distinct language fields',()=>{assert.equal(C.filterRecords(index,works,readings,{q:A}).length,2);assert.equal(C.filterRecords(index,works,readings,{q:'fowl'})[0].id,'test:1');});
test('Exact folio filtering never matches 11r for 1r',()=>assert.deepEqual(C.filterRecords(index,works,readings,{folio:'1R'}).map(r=>r.id),['test:1']));
test('Search combines query and subject/work/confidence',()=>{assert.equal(C.filterRecords(index,works,readings,{q:'water manuscript',subject:'ritual',work:'test',confidence:'C'}).length,1);assert.equal(C.filterRecords(index,works,readings,{q:'water',confidence:'B'}).length,0);});
test('Public metadata does not pretend to contain English',()=>assert.equal(C.filterRecords(index,works,new Map(),{q:'fowl'}).length,0));
test('Imported entries preserve values and field-level confidence',()=>{const r=C.validatePack(pack(),index);assert.equal(r[0].layers.inherited_transcription,A);assert.equal(r[0].headword_confidence,'A');assert.equal(r[0].confidence,'B');});
test('Duplicate, unknown, conflicting IDs reject before mutation',()=>{for(const edit of [p=>p.records.push(p.records[0]),p=>p.records[0].id='bad',p=>p.records[0].confidence='A',p=>p.records[0].folio='2r']){const p=pack();edit(p);assert.throws(()=>C.validatePack(p,index));}});
test('PUA and replacement glyphs cannot enter searchable Ahom',()=>{for(const text of ['\ue001','\ufffd']){const p=pack();p.records[0].layers.inherited_transcription=text;assert.throws(()=>C.validatePack(p,index));}});
test('Empty supplied text remains empty, not reconstructed',()=>{const p=pack();p.records[0].layers.inherited_transcription='';assert.equal(C.validatePack(p,index)[0].layers.inherited_transcription,'');});
test('Rendered strings escape active HTML',()=>assert.equal(C.escapeHtml('<img src=x onerror="x">'),'&lt;img src=x onerror=&quot;x&quot;&gt;'));
test('Unsupported schema and invalid layer types reject',()=>{const p=pack();p.version=2;assert.throws(()=>C.validatePack(p,index));const t=pack();t.records[0].layers.english={html:'x'};assert.throws(()=>C.validatePack(t,index));});
test('Research source discovery searches description, subjects, bibliography and date',()=>{
  const sources=JSON.parse(fs.readFileSync(path.join(__dirname,'../data/catalogue.json'),'utf8'));
  const id='1_FhHnRLXQVE4gyfxnVRxzDeVyU0t1Z_W';
  for(const q of ['Nanzhao','Yuan shi','historical geography','Hemanta Gogoi','2026-10-28','Shan migration']){
    assert.ok(C.filterSources(sources,{q}).some(s=>s.id===id),q);
  }
  assert.equal(C.filterSources(sources,{q:'Nanzhao',category:'06_Other_Editions_and_Research'})[0].id,id);
  assert.equal(C.filterSources(sources,{q:'Nanzhao',category:'02_Original_Manuscripts'}).length,0);
  assert.equal(C.filterSources(sources,{q:'nonexistent research xyz'}).length,0);
});
test('Older sources remain searchable without new optional metadata',()=>{
  const sources=[{title:'Bar Amra',filename:'Bar_Amra.pdf',category:'03_Source_Transcriptions'}];
  assert.deepEqual(C.filterSources(sources,{q:'Bar Amra'}),sources);
});
