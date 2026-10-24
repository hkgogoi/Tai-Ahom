(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.AtlasCore = factory();
})(typeof window !== 'undefined' ? window : globalThis, function () {
  'use strict';
  const escapeHtml = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  // Strip Latin accent marks only. Ahom vowel signs must remain significant.
  const fold = value => String(value ?? '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/\s+/g, ' ').trim();
  const matches = (query, fields) => fold(query).split(' ').filter(Boolean).every(word => fold(fields.join(' ')).includes(word));
  function pageNumber(value, count = 394, fallback = 7) {
    const n = Number(value);
    return Number.isInteger(n) && n >= 1 && n <= count ? n : fallback;
  }
  const emptyNotebook = () => ({schema:'ahom-atlas-notebook',version:1,notes:[],bookmarks:[]});
  function validateNotebook(input, anchors = []) {
    if (!input || input.schema !== 'ahom-atlas-notebook' || input.version !== 1 || !Array.isArray(input.notes) || !Array.isArray(input.bookmarks)) throw new Error('This file is not an Ahom Atlas notebook (version 1).');
    if (input.notes.length > 5000 || input.bookmarks.length > 5000) throw new Error('This notebook is too large to import.');
    const ids = new Set(); const markIds = new Set();
    const notes=input.notes.map(n=>{
      if(!n || typeof n.id!=='string' || !/^(page-[0-9]{1,3}|anchor-ab-p[0-9]{3}-[0-9]{2}|lex-ba-[0-9]+[rv]-[0-9]+|research-lengdon-nimi)$/.test(n.id) || typeof n.text!=='string' || n.text.length>20000 || typeof n.updated!=='string' || !Number.isFinite(Date.parse(n.updated)) || ids.has(n.id)) throw new Error('A note has an invalid or duplicate record. Nothing was changed.');
      if (n.id.startsWith('page-') && pageNumber(n.id.slice(5),394,0)===0) throw new Error('A note refers to an invalid scan page.');
      if(n.id.startsWith('anchor-') && !anchors.includes(n.id.slice(7))) throw new Error('A note refers to an unknown passage.');
      ids.add(n.id);return {id:n.id,text:n.text,updated:new Date(n.updated).toISOString()};
    });
    const bookmarks=input.bookmarks.map(b=>{
      const page=pageNumber(b?.page,394,0);
      if (!b || !page || typeof b.id!=='string' || b.id!==`page-${page}` || markIds.has(b.id)) throw new Error('A bookmark has an invalid or duplicate page. Nothing was changed.');
      markIds.add(b.id); return {id:b.id,page};
    });
    return {...emptyNotebook(),notes,bookmarks};
  }
  function mergeNotebooks(current, incoming) {
    const notes=new Map(current.notes.map(n=>[n.id,n]));
    for(const n of incoming.notes){const old=notes.get(n.id);if(!old || Date.parse(n.updated)>Date.parse(old.updated))notes.set(n.id,n);}
    const bookmarks=new Map(current.bookmarks.map(n=>[n.id,n]));
    for(const b of incoming.bookmarks)bookmarks.set(b.id,b);
    return {...emptyNotebook(),notes:[...notes.values()],bookmarks:[...bookmarks.values()].sort((a,b)=>a.page-b.page)};
  }
  return {escapeHtml,fold,matches,pageNumber,emptyNotebook,validateNotebook,mergeNotebooks};
});
