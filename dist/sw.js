const CACHE='ahom-atlas-0.1.0-r2';
const SHELL=['./','index.html','styles.css','data.js','core.js','app.js','assets/mark.svg','assets/NotoSerifAhom-Regular.ttf','manifest.webmanifest'];
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(SHELL)).then(()=>self.skipWaiting())));
self.addEventListener('activate',event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('ahom-atlas-')&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
async function trimPages(cache){const keys=await cache.keys();const pages=keys.filter(k=>/\/pages\/\d+\.webp$/.test(new URL(k.url).pathname));while(pages.length>40)await cache.delete(pages.shift());}
self.addEventListener('fetch',event=>{
 if(event.request.method!=='GET'||new URL(event.request.url).origin!==self.location.origin)return;
 const url=new URL(event.request.url);
 event.respondWith((async()=>{
  const cache=await caches.open(CACHE);
  if(/\.(webp|ttf|svg|png)$/.test(url.pathname)){
   const stored=await cache.match(event.request);if(stored)return stored;
   const response=await fetch(event.request);if(response.ok){await cache.put(event.request,response.clone());await trimPages(cache);}return response;
  }
  try{const response=await fetch(event.request);if(response.ok)await cache.put(event.request,response.clone());return response;}
  catch(err){const stored=await cache.match(event.request);if(stored)return stored;if(event.request.mode==='navigate'){const index=await cache.match('index.html');if(index)return index;}throw err;}
 })());
});
