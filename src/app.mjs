// SPDX-License-Identifier: GPL-3.0-only
// Copyright (C) 2026 MH
const $=id=>document.getElementById(id), status=$('map-status');
function fail(e){console.error(e);status.hidden=false;status.textContent='The map could not start: '+(e.message||e)+'. Open this file in a current desktop browser with WebGL enabled.';status.classList.add('error');}
try {
const decode=id=>Uint8Array.from(atob($(id).textContent.trim()),c=>c.charCodeAt(0));
const libraryURL=URL.createObjectURL(new Blob([decode('map-code')],{type:'text/javascript'}));
const workerURL=URL.createObjectURL(new Blob([decode('worker-code')],{type:'text/javascript'}));
const ml=await import(libraryURL);ml.setWorkerUrl(workerURL);ml.setWorkerCount(2);
const decompressed=new Blob([decode('map-data')]).stream().pipeThrough(new DecompressionStream('gzip'));
const D=JSON.parse(await new Response(decompressed).text());
const modeRows=[['shinkansen','Shinkansen'],['jr','JR conventional'],['private','Private / third-sector'],['metro','Metro'],['tram','Tram / light rail'],['guideway','Monorail / automated transit'],['funicular','Funicular'],['ropeway','Public ropeway / lift'],['ferry','Ferries / passenger boats'],['boat','Waterbus / sightseeing'],['international','International ferries'],['suspended','Long-term suspensions']];
const active=new Set(modeRows.map(r=>r[0]).filter(x=>x!=='suspended'));
const font=['Arial Unicode MS','Hiragino Kaku Gothic ProN','Noto Sans CJK JP','Arial','sans-serif'];
let map,ready=false,popup=null,selectedStation=null,currentView='tokyo';
const bounds={japan:[[122.45,23.75],[146.3,46.0]],hokkaido:[[139.1,41.1],[145.9,45.7]],kyushu:[[128.4,30.8],[132.35,34.1]],okinawa:[[122.6,23.8],[130.0,27.2]]};
const presets={tokyo:{center:[139.753,35.688],zoom:12.4},osaka:{center:[135.501,34.687],zoom:12.3},nagoya:{center:[136.906,35.17],zoom:12.5}};
const style={version:8,sources:{land:{type:'geojson',data:D.land,maxzoom:13,tolerance:0.7},lakes:{type:'geojson',data:D.lakes,maxzoom:13,tolerance:0.7},lines:{type:'geojson',data:D.lines,maxzoom:17,tolerance:0.45,buffer:128},stations:{type:'geojson',data:D.stations,maxzoom:18,buffer:128}},layers:[{id:'ocean',type:'background',paint:{'background-color':'#e9f1f2'}},{id:'land',type:'fill',source:'land',paint:{'fill-color':'#fbfaf4','fill-outline-color':'#b9c8c8'}},{id:'lakes',type:'fill',source:'lakes',paint:{'fill-color':'#e9f1f2','fill-outline-color':'#c0d0d1'}}]};
map=new ml.Map({container:'map',style,center:presets.tokyo.center,zoom:presets.tokyo.zoom,minZoom:3,maxZoom:22,prefetchZoomDelta:0,localIdeographFontFamily:'"Arial Unicode MS", "Hiragino Kaku Gothic ProN", sans-serif',maxPitch:0,attributionControl:false,preserveDrawingBuffer:true,renderWorldCopies:false,dragRotate:false,touchPitch:false});
map.scrollZoom.setWheelZoomRate(1/200);
map.scrollZoom.setZoomRate(1/60);
map.addControl(new ml.NavigationControl({showCompass:false}),'top-right');map.addControl(new ml.ScaleControl({maxWidth:160,unit:'metric'}),'bottom-left');map.addControl(new ml.AttributionControl({compact:false,customAttribution:'© <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap contributors</a> · MLIT · <a href="https://github.com/kametaro7/japan-ferry-map" target="_blank">kametaro7</a> · ODbL'}),'bottom-right');
const backgrounds={
 osm:{tiles:['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],minzoom:0,maxzoom:19,opacity:55,saturation:-0.45,attribution:''},
 aerial:{tiles:['https://cyberjapandata.gsi.go.jp/xyz/seamlessphoto/{z}/{x}/{y}.jpg'],minzoom:2,maxzoom:18,opacity:65,saturation:-0.2,attribution:'<a href="https://maps.gsi.go.jp/development/ichiran.html" target="_blank" rel="noopener">地理院タイル / GSI Japan</a> · Landsat8 (GSI, TSIC, GEO Grid/AIST; USGS) · GEBCO · NASA/USGS LP DAAC · GRUS © Axelspace'}
};
let background='none';
function applyBackground(){
 if(!ready)return;
 const choice=$('background').value,spec=backgrounds[choice];
 if(background!==choice){
  if(map.getLayer('background-tiles'))map.removeLayer('background-tiles');
  if(map.getSource('background-tiles'))map.removeSource('background-tiles');
  if(spec){
   map.addSource('background-tiles',{type:'raster',tiles:spec.tiles,tileSize:256,minzoom:spec.minzoom,maxzoom:spec.maxzoom,attribution:spec.attribution});
   map.addLayer({id:'background-tiles',type:'raster',source:'background-tiles',paint:{'raster-opacity':0,'raster-saturation':spec.saturation,'raster-fade-duration':150}},'line-ferry_suspended');
  }
  background=choice;
 }
 const opacity=Number($('background-opacity').value)/100;
 $('background-opacity').disabled=!spec;
 $('background-opacity-value').value=Math.round(opacity*100)+'%';
 $('background-opacity').setAttribute('aria-valuetext',Math.round(opacity*100)+' percent');
 if(spec)map.setPaintProperty('background-tiles','raster-opacity',opacity);
 const url=new URL(location.href);
 if(spec){url.searchParams.set('background',choice);url.searchParams.set('opacity',String(Math.round(opacity*100)));}
 else{url.searchParams.delete('background');url.searchParams.delete('opacity');}
 try{history.replaceState(null,'',url);}catch{}
 updateStatus();
}
$('background').onchange=()=>{const spec=backgrounds[$('background').value];if(spec)$('background-opacity').value=String(spec.opacity);applyBackground();};
$('background-opacity').oninput=applyBackground;
window.atlas={map,data:D,ready:false,selectStation,chooseView,active,applyFilters};
const c=D.count;$('coverage').textContent=`${c.rail_station_objects.toLocaleString()} mapped rail-station objects; ${c.station_objects.toLocaleString()} station and terminal objects overall. ${c.water_services} water-service records, of which ${c.active_water_services} are marked active in the assembled inventory. 104 active sightseeing services have no fixed circuit geometry and are shown at their departure points.`;
function modeFilter(m){return ['==',['get','m'],m]}
function shownModes(){return [...active].filter(x=>x!=='suspended').concat(active.has('suspended')?['rail_suspended','ferry_suspended']:[])}
function chooseView(view){if(!ready)return;currentView=view;if(popup)popup.remove();if(bounds[view])map.fitBounds(bounds[view],{padding:{top:50,bottom:60,left:40,right:40},duration:800});else if(presets[view])map.flyTo({...presets[view],duration:900});$('views').querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===view)));if(innerWidth<760)$('sidebar').classList.remove('open');}
function applyFilters(){if(!ready)return;for(const [m] of modeRows){if(m==='suspended')continue;for(const suffix of ['','-casing','-approx'])if(map.getLayer('line-'+m+suffix))map.setLayoutProperty('line-'+m+suffix,'visibility',active.has(m)?'visible':'none');}for(const m of ['rail_suspended','ferry_suspended']){map.setLayoutProperty('line-'+m,'visibility',active.has('suspended')?'visible':'none');if(map.getLayer('line-'+m+'-approx'))map.setLayoutProperty('line-'+m+'-approx','visibility',active.has('suspended')?'visible':'none');}map.setFilter('line-names',['in',['get','m'],['literal',shownModes()]]);const sf=['any',['in',['get','m'],['literal',shownModes()]],...(active.has('ferry')||active.has('boat')||active.has('international')?[['==',['get','m'],'water']]:[])];for(const layer of ['station-dots','station-names','service-points'])map.setFilter(layer,layer==='service-points'?['all',sf,['==',['get','point'],1]]:sf);map.setFilter('selected-line',['==',['get','i'],-999]);updateStatus();}
function updateNames(){if(!ready)return;const lang=$('language').value;let field=['get','n'];if(lang==='en')field=['case',['all',['has','en'],['!=',['get','en'],'']],['get','en'],['get','n']];if(lang==='both')field=['case',['all',['has','en'],['!=',['get','en'],''],['!=',['get','en'],['get','n']]],['concat',['get','n'],'\n',['get','en']],['get','n']];map.setLayoutProperty('station-names','text-field',field);map.setLayoutProperty('selected-name','text-field',field);const overlap=$('all-labels').checked||map.getZoom()>=16.7;map.setLayoutProperty('station-names','text-allow-overlap',overlap);map.setLayoutProperty('station-names','text-ignore-placement',overlap);}
function updateStatus(){if(!ready)return;status.hidden=true;status.classList.remove('error');}
for(const [m,label] of modeRows){const row=document.createElement('label');row.className='mode';const cb=document.createElement('input');cb.type='checkbox';cb.checked=active.has(m);cb.dataset.mode=m;cb.addEventListener('change',()=>{cb.checked?active.add(m):active.delete(m);applyFilters();});const sw=document.createElement('span');sw.className='swatch';sw.style.setProperty('--c',D.colors[m]||'#999fa6');if(m==='suspended')sw.style.borderTopStyle='dashed';const txt=document.createElement('span');txt.textContent=label;row.append(cb,sw,txt);$('filters').append(row);}
function el(tag,cls,text){const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined)e.textContent=text;return e;}
function link(container,label,url){if(!/^https?:\/\//i.test(url||''))return;const a=el('a','popup-link',label);a.href=url;a.target='_blank';a.rel='noopener';container.append(a);}
function routeContent(i){const r=D.meta[i],content=el('div');content.append(el('div','popup-kicker',r.type),el('div','popup-title',r.name));if(r.en&&r.en!==r.name)content.append(el('div','popup-en',r.en));if(r.operator)content.append(el('div','popup-detail',r.operator));if(r.quality&&!['mapped','osm'].includes(r.quality))content.append(el('div','quality',r.quality));if(r.seasonal)content.append(el('div','popup-detail','Seasonal schedule'+(r.season_note?' · '+r.season_note:'')));if(r.frequency)content.append(el('div','popup-detail',r.frequency));if(r.status&&r.status!=='active')content.append(el('div','popup-detail','Service status: '+r.status));if(r.notes)content.append(el('div','popup-detail',r.notes));link(content,'Operator / route',r.route_url||r.operator_url||r.sources[0]);link(content,'OSM geometry',r.osm);return content;}
function showRoute(i,xy,fly=false){const f=D.lines.features[i];if(!f)return;if(fly){const b=featureBounds(f);map.fitBounds(b,{padding:80,maxZoom:14.5,duration:800});xy=[(b[0][0]+b[1][0])/2,(b[0][1]+b[1][1])/2];}map.setFilter('selected-line',['==',['get','i'],i]);map.setFilter('selected-dot',['==',['get','i'],-999]);map.setFilter('selected-name',['==',['get','i'],-999]);if(popup)popup.remove();popup=new ml.Popup({maxWidth:'345px',closeOnClick:false}).setLngLat(xy).setDOMContent(routeContent(i)).addTo(map);}
function selectStation(i,fly=true){if(!ready)return;const s=D.search[i];if(!s)return;selectedStation=i;const content=el('div');content.append(el('div','popup-kicker',s.point_only?'Sightseeing departure · fixed circuit unavailable':s.mode==='water'?'Passenger boat terminal':'Passenger station'),el('div','popup-title',s.n));if(s.en&&s.en!==s.n)content.append(el('div','popup-en',s.en));if(s.o)content.append(el('div','popup-detail',s.o));if(s.point_only)content.append(el('div','popup-detail','This source identifies a scheduled sightseeing service here, but supplies no fixed route geometry.'));if(s.near.length){content.append(el('div','popup-kicker','Nearby mapped lines'));const near=el('div','popup-near');for(const rid of s.near){const r=D.meta[rid],b=el('button','popup-line',r.name);b.style.setProperty('--c',D.colors[r.mode]);b.onclick=()=>showRoute(rid,s.xy);near.append(b);}content.append(near);}if(s.id.startsWith('n'))link(content,'Station source','https://www.openstreetmap.org/node/'+s.id.slice(1));else if(/^w\d+$/.test(s.id))link(content,'Station source','https://www.openstreetmap.org/way/'+s.id.slice(1));const reference=(s.sources||[]).find(url=>/^https?:\/\//i.test(url)&&!/(openstreetmap\.org|github\.com)/i.test(url));if(reference)link(content,'Operator / reference',reference);if(s.route){const rid=D.meta.findIndex(r=>r.route_id===s.route);if(rid>=0)link(content,'Operator / timetable',D.meta[rid].route_url||D.meta[rid].sources[0]);}if(popup)popup.remove();popup=new ml.Popup({maxWidth:'345px',closeOnClick:false}).setLngLat(s.xy).setDOMContent(content).addTo(map);map.setFilter('selected-dot',['==',['get','i'],i]);map.setFilter('selected-name',['==',['get','i'],i]);map.setFilter('selected-line',['==',['get','i'],-999]);if(fly)map.flyTo({center:s.xy,zoom:Math.max(map.getZoom(),16),duration:900});$('results').replaceChildren();if(innerWidth<760)$('sidebar').classList.remove('open');}
function featureBounds(f){let minx=180,miny=90,maxx=-180,maxy=-90;function visit(c){if(typeof c[0]==='number'){minx=Math.min(minx,c[0]);maxx=Math.max(maxx,c[0]);miny=Math.min(miny,c[1]);maxy=Math.max(maxy,c[1]);}else c.forEach(visit);}visit(f.geometry.coordinates);return [[minx,miny],[maxx,maxy]];}
const norm=s=>(s||'').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^\p{L}\p{N}]+/gu,' ').trim();const index=[...D.search.map(s=>({type:'station',i:s.i,n:s.n,en:s.en,o:s.o,m:s.mode,key:norm(s.n+' '+s.en+' '+s.o)})),...D.meta.map(s=>({type:'line',i:s.i,n:s.name,en:s.en||'',o:s.operator,m:s.mode,key:norm(s.name+' '+(s.en||'')+' '+s.operator+' '+(s.aliases||[]).join(' '))}))];let searchMatches=[];
function search(){const q=norm($('search').value);$('results').replaceChildren();if(q.length<1)return;const tokens=q.split(' ');searchMatches=index.filter(s=>tokens.every(t=>s.key.includes(t))).sort((a,b)=>((norm(b.n)===q||norm(b.en)===q)?10:0)-((norm(a.n)===q||norm(a.en)===q)?10:0)||(a.type==='station'?-1:1)).slice(0,12);for(const s of searchMatches){const b=el('button','result',s.n+(s.en&&s.en!==s.n?' · '+s.en:''));b.append(el('small','',s.type==='line'?(D.modes[s.m]+' · '+s.o):((s.m==='water'?'Port / departure':'Station')+(s.o?' · '+s.o:''))));b.onclick=()=>s.type==='station'?selectStation(s.i):showRoute(s.i,null,true);$('results').append(b);}if(!searchMatches.length)$('results').append(el('div','result','No matching mapped name. Try Japanese or a shorter spelling.'));}
$('search').addEventListener('input',search);$('search').addEventListener('keydown',e=>{if(e.key==='Enter'&&searchMatches.length){e.preventDefault();const s=searchMatches[0];s.type==='station'?selectStation(s.i):showRoute(s.i,null,true);}if(e.key==='Escape')$('results').replaceChildren();});
$('views').addEventListener('click',e=>{const b=e.target.closest('button[data-view]');if(b)chooseView(b.dataset.view);});$('language').onchange=updateNames;$('all-labels').onchange=()=>{updateNames();updateStatus();};$('about').onclick=()=>$('about-dialog').showModal();$('close-about').onclick=()=>$('about-dialog').close();$('mobile-handle').onclick=()=>$('sidebar').classList.add('open');$('close-menu').onclick=()=>$('sidebar').classList.remove('open');
map.on('error',e=>{console.warn('Map source:',e.error?.message||e);if(!ready&&e.error?.message?.includes('WebGL'))fail(e.error);});
map.on('load',()=>{
 const width=['interpolate',['linear'],['zoom'],4,0.7,7,1.3,10,2.0,13,3.0,16,4.0,20,7.0];
 for(const m of ['ferry_suspended','rail_suspended','international','ferry','boat','jr','private','shinkansen','metro','guideway','tram','funicular','ropeway']){
  const isWater=['ferry','boat','international','ferry_suspended'].includes(m),susp=m.endsWith('suspended');
  const w=m==='shinkansen'?['interpolate',['linear'],['zoom'],4,1.0,7,1.9,10,2.8,13,4.0,16,5.0,20,8]:isWater?['interpolate',['linear'],['zoom'],4,.7,8,1.1,12,1.8,16,3,20,5]:width;
  if(!isWater&&!susp)map.addLayer({id:'line-'+m+'-casing',type:'line',source:'lines',filter:modeFilter(m),layout:{'line-cap':'round','line-join':'round'},paint:{'line-color':'#fffef8','line-opacity':.86,'line-width':['+',w,1.8]}});
  const paint={'line-color':D.colors[m],'line-width':w,'line-opacity':susp?.7:1};if(isWater||susp)paint['line-dasharray']=isWater?[5,3]:[2,2];
  map.addLayer({id:'line-'+m,type:'line',source:'lines',filter:isWater?['all',modeFilter(m),['in',['get','q'],['literal',['osm','mapped']]]]:modeFilter(m),layout:{'line-cap':'round','line-join':'round',visibility:susp?'none':'visible'},paint});if(isWater){map.addLayer({id:'line-'+m+'-approx',type:'line',source:'lines',filter:['all',modeFilter(m),['!', ['in',['get','q'],['literal',['osm','mapped']]]]],layout:{'line-cap':'round','line-join':'round',visibility:susp?'none':'visible'},paint:{...paint,'line-dasharray':[2,2]}});}
 }
 // A second fine pattern distinguishes indicative ferry paths from mapped paths.
 map.addLayer({id:'line-names',type:'symbol',source:'lines',minzoom:8,filter:['in',['get','m'],['literal',shownModes()]],layout:{'symbol-placement':'line','symbol-spacing':350,'text-field':['get','label'],'text-font':font,'text-size':12,'text-max-angle':40,'text-padding':8,'text-keep-upright':true},paint:{'text-color':['get','c'],'text-halo-color':'#fffef8','text-halo-width':1.8}});
 map.addLayer({id:'selected-line',type:'line',source:'lines',filter:['==',['get','i'],-999],layout:{'line-cap':'round','line-join':'round'},paint:{'line-color':'#172f45','line-width':7,'line-opacity':.5}});
 map.addLayer({id:'station-dots',type:'circle',source:'stations',minzoom:7.5,paint:{'circle-radius':['interpolate',['linear'],['zoom'],7,1,11,2,15,3.6,20,6],'circle-color':['case',['==',['get','m'],'water'],'#e9f1f2','#fffefa'],'circle-stroke-color':['case',['==',['get','m'],'water'],'#148795','#27495c'],'circle-stroke-width':['interpolate',['linear'],['zoom'],7,.5,14,1.3,20,2]}});
 map.addLayer({id:'service-points',type:'symbol',source:'stations',minzoom:7,filter:['==',['get','point'],1],layout:{'text-field':'◇','text-font':font,'text-size':21,'text-allow-overlap':true},paint:{'text-color':'#148795','text-halo-color':'#fffef8','text-halo-width':1.5}});
 map.addLayer({id:'station-names',type:'symbol',source:'stations',minzoom:10.5,layout:{'text-field':['get','n'],'text-font':font,'text-size':['interpolate',['linear'],['zoom'],10,11,13,12,16,14,20,17],'text-anchor':'left','text-offset':[.6,0],'text-max-width':18,'text-padding':4,'symbol-sort-key':['case',['==',['get','major'],1],0,1]},paint:{'text-color':'#183b51','text-halo-color':'#fffef8','text-halo-width':2.1,'text-halo-blur':.3}});
 map.addLayer({id:'major-place-names',type:'symbol',source:'stations',minzoom:4,maxzoom:10.5,filter:['==',['get','major'],1],layout:{'text-field':['case',['!=',['get','en'],''],['concat',['get','n'],' / ',['get','en']],['get','n']],'text-font':font,'text-size':12,'text-anchor':'left','text-offset':[.5,0],'text-padding':12},paint:{'text-color':'#254452','text-halo-color':'#fffef8','text-halo-width':2}});
 map.addLayer({id:'selected-dot',type:'circle',source:'stations',filter:['==',['get','i'],-999],paint:{'circle-radius':7,'circle-color':'#fffefa','circle-stroke-color':'#173348','circle-stroke-width':3}});
 map.addLayer({id:'selected-name',type:'symbol',source:'stations',filter:['==',['get','i'],-999],layout:{'text-field':['get','n'],'text-font':font,'text-size':16,'text-anchor':'left','text-offset':[.7,0],'text-allow-overlap':true,'text-ignore-placement':true},paint:{'text-color':'#102f44','text-halo-color':'#fffefa','text-halo-width':3}});
 ready=true;window.atlas.ready=true;
 const params=new URLSearchParams(location.search),requested=params.get('background');
 if(backgrounds[requested]){$('background').value=requested;const opacity=Number(params.get('opacity'));$('background-opacity').value=params.has('opacity')&&Number.isFinite(opacity)?String(Math.min(100,Math.max(0,opacity))):String(backgrounds[requested].opacity);}
 applyBackground();document.documentElement.dataset.ready='true';$('export').disabled=false;updateNames();updateStatus();applyFilters();
 const hash=location.hash.match(/^#([\d.]+)\/([-\d.]+)\/([-\d.]+)$/);if(hash)map.jumpTo({zoom:+hash[1],center:[+hash[3],+hash[2]]});else $('views').querySelector('[data-view=tokyo]').setAttribute('aria-pressed','true');
});
map.on('zoomend',()=>{updateNames();updateStatus();});map.on('moveend',()=>{if(!ready)return;try{const c=map.getCenter();history.replaceState(null,'',`#${map.getZoom().toFixed(2)}/${c.lat.toFixed(5)}/${c.lng.toFixed(5)}`);}catch{} });
map.on('click',e=>{if(!ready)return;const hits=map.queryRenderedFeatures([[e.point.x-7,e.point.y-7],[e.point.x+7,e.point.y+7]],{layers:['station-dots','station-names','service-points','selected-dot']});if(hits.length){selectStation(+hits[0].properties.i,false);return;}const layers=modeRows.filter(r=>r[0]!=='suspended').flatMap(r=>['line-'+r[0],...(map.getLayer('line-'+r[0]+'-approx')?['line-'+r[0]+'-approx']:[])]);if(active.has('suspended'))layers.push('line-rail_suspended','line-ferry_suspended','line-ferry_suspended-approx');const line=map.queryRenderedFeatures([[e.point.x-5,e.point.y-5],[e.point.x+5,e.point.y+5]],{layers});if(line.length)showRoute(+line[0].properties.i,[e.lngLat.lng,e.lngLat.lat]);});
map.on('mousemove',e=>{if(!ready)return;const h=map.queryRenderedFeatures(e.point,{layers:['station-dots','line-names','station-names']});map.getCanvas().style.cursor=h.length?'pointer':'';});
$('export').onclick=async()=>{
 const button=$('export');button.disabled=true;button.textContent='Saving…';
 try{
  map.triggerRepaint();await new Promise(resolve=>map.once('render',resolve));
  const src=map.getCanvas(),out=document.createElement('canvas'),ratio=src.width/map.getContainer().clientWidth;
  out.width=src.width;
  const ctx=out.getContext('2d'),rows=[];
  function wrap(text,size){
   ctx.font=`${size*ratio}px sans-serif`;
   let line='';
   for(const word of text.split(' ')){
    const candidate=line?line+' '+word:word;
    if(line&&ctx.measureText(candidate).width>out.width-32*ratio){rows.push({text:line,size});line=word;}
    else line=candidate;
   }
   if(line)rows.push({text:line,size});
  }
  wrap('JAPAN · Passenger rail & water atlas',15);
  wrap('© OpenStreetMap contributors · openstreetmap.org/copyright · MLIT · kametaro7 · ODbL',10);
  if(background==='aerial'){
   wrap('地理院タイル / GSI Japan · maps.gsi.go.jp/development/ichiran.html',10);
   wrap('Landsat8 (GSI, TSIC, GEO Grid/AIST; USGS) · GEBCO · NASA/USGS LP DAAC · GRUS © Axelspace',10);
  }
  wrap('Ferry paths may be approximate. Complete coverage is not certified.',10);
  out.height=src.height+Math.ceil((24+rows.reduce((height,row)=>height+row.size+6,0))*ratio);
  ctx.drawImage(src,0,0);ctx.fillStyle='#fcfcf8';ctx.fillRect(0,src.height,out.width,out.height-src.height);
  ctx.fillStyle='#173348';let y=src.height+18*ratio;
  for(const row of rows){y+=row.size*ratio;ctx.font=`${row.size*ratio}px sans-serif`;ctx.fillText(row.text,16*ratio,y);y+=6*ratio;}
  const blob=await new Promise(resolve=>out.toBlob(resolve,'image/png'));
  if(!blob)throw new Error('The browser could not encode the PNG.');
  const link=document.createElement('a');link.download='japan-passenger-map-view.png';link.href=URL.createObjectURL(blob);link.click();
  status.hidden=false;status.textContent=`PNG ready · ${out.width.toLocaleString()} × ${out.height.toLocaleString()} pixels`;
  setTimeout(()=>URL.revokeObjectURL(link.href),2000);
 }catch(error){alert('Could not export this view: '+error.message);}
 finally{button.disabled=false;button.textContent='Save this view as PNG';}
};
}catch(e){fail(e);}
