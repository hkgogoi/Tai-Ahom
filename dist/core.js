/* Search helpers adapted from the project's 0.1.0 Atlas build (MIT). */
(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory();else root.ArchiveCore=factory();})(typeof window==='undefined'?globalThis:window,function(){
  'use strict';
  const escapeHtml=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  // Do not strip Ahom combining marks. Only Latin combining accents are folded.
  const fold=value=>String(value??'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/\s+/g,' ').trim();
  const matches=(query,fields)=>fold(query).split(' ').filter(Boolean).every(token=>fold(fields.join(' ')).includes(token));
  function filterRecords(records,works,readings,filters={}){
    const byWork=new Map(works.map(w=>[w.id,w]));
    return records.filter(r=>{
      const w=byWork.get(r.work), p=readings.get(r.id), l=p?.layers||{};
      if(filters.work&&r.work!==filters.work)return false;
      if(filters.folio&&fold(r.folio)!==fold(filters.folio))return false;
      if(filters.confidence&&r.confidence!==filters.confidence)return false;
      if(filters.subject&&!w.subjects.includes(filters.subject))return false;
      return matches(filters.q,[r.id,r.source_record_id,r.folio,w.title,w.identifier,...w.subjects,l.inherited_transcription,l.formula,l.assamese_in_ahom_script,l.english,l.romanization,l.assamese_romanization]);
    });
  }
  const hasPUA=text=>[...text].some(c=>{const n=c.codePointAt(0);return n>=0xE000&&n<=0xF8FF||n>=0xF0000&&n<=0xFFFFD||n>=0x100000&&n<=0x10FFFD;});
  function validatePack(pack,index){
    if(!pack||pack.schema!=='tai-ahom-reading-pack'||pack.version!==1||!Array.isArray(pack.records)||pack.records.length>10000||pack.records.length===0)throw new Error('Choose a Tai-Ahom reading pack, version 1. Nothing was changed.');
    const known=new Map(index.map(r=>[r.id,r])),seen=new Set();
    const fields=['inherited_transcription','formula','assamese_in_ahom_script','punctuation','english','romanization','assamese_romanization','editorial_reconstruction','interpretation'];
    const result=[];
    for(const r of pack.records){
      const k=known.get(r?.id);
      if(!k||seen.has(r.id)||r.work!==k.work||r.source_record_id!==k.source_record_id||r.folio!==k.folio||r.confidence!==k.confidence||r.headword_confidence!==k.headword_confidence)throw new Error('A record is unknown, duplicated, or conflicts with the source index. Nothing was changed.');
      if(!r.layers||typeof r.layers!=='object'||Array.isArray(r.layers))throw new Error('A record has no valid reading layers.');
      const layers={};
      for(const f of fields){const v=r.layers[f]??null;if(v!==null&&(typeof v!=='string'||v.length>200000))throw new Error('A reading field is invalid.');if(['inherited_transcription','formula','assamese_in_ahom_script','punctuation'].includes(f)&&v&&(hasPUA(v)||v.includes('\ufffd')))throw new Error('An Ahom field contains private-use or replacement characters.');layers[f]=v;}
      if(!Array.isArray(r.notes)||r.notes.some(n=>typeof n!=='string'||n.length>20000)||typeof r.reading_status!=='string')throw new Error('A record has invalid notes or status.');
      seen.add(r.id);result.push({...k,layers,notes:r.notes,reading_status:r.reading_status,source_record:r.source_record||null});
    }
    return result;
  }
  return {escapeHtml,fold,matches,filterRecords,validatePack,hasPUA};
});
