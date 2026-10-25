// SPDX-License-Identifier: GPL-3.0-only
// Copyright (C) 2026 MH

/** Historical geometry is optional and is decoded only when its layer is enabled. */
export function createHistoricalLayer({map, ml, font, loadData, closeCurrentSelection, onSearchChange, setAttribution}) {
 const $=id=>document.getElementById(id);
 const toggle=$('historical'),pointsToggle=$('historical-points'),child=$('historical-points-row'),status=$('history-status');
 const lineLayers=['historic-lines','historic-selected-line','historic-line-names'];
 const pointLayers=['historic-stations','historic-sites','historic-point-names','historic-selected-point','historic-selected-name'];
 const allLayers=[...lineLayers,...pointLayers];
 const color='#936444',dark='#634027';
 let data=null,pending=null,installed=false,enabled=false,desired=false,revision=0,popup=null,selected=null,language='both',overlap=false,entries=[];
 const norm=s=>(s||'').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^\p{L}\p{N}]+/gu,' ').trim();
 const recordById=new Map(),lineById=new Map();
 const labels={line:'Historic railway',station:'Former station',site:'Railway site'};
 const qualityLabels={mapped:'Mapped historical alignment',source_reconstruction:'Reconstructed from historical sources',approximate:'Approximate alignment',site_only:'Site location only'};
 function element(tag,cls,text){const node=document.createElement(tag);if(cls)node.className=cls;if(text!==undefined)node.textContent=String(text);return node;}
 function sourceLink(parent,label,url){if(!/^https?:\/\//i.test(url||''))return;const node=element('a','popup-link',label);node.href=url;node.target='_blank';node.rel='noopener';parent.append(node);}
 function urlState(){const url=new URL(location.href);if(desired){url.searchParams.set('history','1');if(pointsToggle.checked)url.searchParams.delete('history-points');else url.searchParams.set('history-points','0');}else{url.searchParams.delete('history');url.searchParams.delete('history-points');}try{history.replaceState(null,'',url);}catch{}}
 function clearSelection(){if(popup)popup.remove();popup=null;selected=null;if(installed){for(const id of ['historic-selected-line','historic-selected-point','historic-selected-name'])map.setFilter(id,['==',['get','i'],-999]);}}
 function visible(){if(!installed)return;for(const id of allLayers)map.setLayoutProperty(id,'visibility',enabled&&(!pointLayers.includes(id)||pointsToggle.checked)?'visible':'none');if(selected&&selected.kind!=='line'&&!pointsToggle.checked)clearSelection();}
 function nameField(){const ja=['coalesce',['get','n'],['get','label'],''];const en=['all',['has','en'],['!=',['get','en'],'']];if(language==='ja')return ja;if(language==='en')return ['case',en,['get','en'],ja];return ['case',['all',en,['!=',['get','en'],ja]],['concat',ja,'\n',['get','en']],ja];}
 function updateNames(options={}){language=options.lang||language;overlap=options.overlap??overlap;if(!installed)return;for(const id of ['historic-point-names','historic-selected-name','historic-line-names'])map.setLayoutProperty(id,'text-field',nameField());map.setLayoutProperty('historic-point-names','text-allow-overlap',overlap);map.setLayoutProperty('historic-point-names','text-ignore-placement',overlap);}
 function install(){
  if(installed)return;
  map.addSource('historic-lines',{type:'geojson',data:data.lines,maxzoom:17,tolerance:.4,buffer:128});
  map.addSource('historic-points',{type:'geojson',data:data.points,maxzoom:18,buffer:128});
  const width=['interpolate',['linear'],['zoom'],4,.7,8,1.3,12,2.1,16,3.2,20,5.4];
  const hidden={visibility:'none'};
  map.addLayer({id:'historic-lines',type:'line',source:'historic-lines',layout:{...hidden,'line-cap':'butt','line-join':'round'},paint:{'line-color':color,'line-width':width,'line-dasharray':[3,2],'line-opacity':['case',['==',['get','q'],'approximate'],.5,.8]}},'line-ferry_suspended');
  map.addLayer({id:'historic-selected-line',type:'line',source:'historic-lines',filter:['==',['get','i'],-999],layout:{...hidden,'line-cap':'round','line-join':'round'},paint:{'line-color':dark,'line-width':['+',width,3],'line-dasharray':[3,2],'line-opacity':.7}},'line-ferry_suspended');
  map.addLayer({id:'historic-line-names',type:'symbol',source:'historic-lines',minzoom:10,layout:{...hidden,'symbol-placement':'line','symbol-spacing':460,'text-field':['get','n'],'text-font':font,'text-size':11,'text-max-angle':35,'text-padding':12,'text-keep-upright':true},paint:{'text-color':dark,'text-halo-color':'#fffdf7','text-halo-width':1.8}},'station-names');
  map.addLayer({id:'historic-stations',type:'circle',source:'historic-points',minzoom:6.8,filter:['==',['get','kind'],'station'],layout:hidden,paint:{'circle-radius':['interpolate',['linear'],['zoom'],6.8,1,9,1.6,12,2.8,16,4,20,6],'circle-color':'#fffdf7','circle-opacity':.7,'circle-stroke-color':color,'circle-stroke-width':['interpolate',['linear'],['zoom'],6.8,.7,12,1.3,16,1.5]}},'station-dots');
  map.addLayer({id:'historic-sites',type:'symbol',source:'historic-points',minzoom:9,filter:['==',['get','kind'],'site'],layout:{...hidden,'text-field':'□','text-font':font,'text-size':['interpolate',['linear'],['zoom'],9,12,16,19,20,23],'text-allow-overlap':true,'text-ignore-placement':true},paint:{'text-color':color,'text-halo-color':'#fffdf7','text-halo-width':1}},'station-dots');
  map.addLayer({id:'historic-point-names',type:'symbol',source:'historic-points',minzoom:11.5,layout:{...hidden,'text-field':['get','n'],'text-font':font,'text-size':['interpolate',['linear'],['zoom'],11,10,15,12,20,15],'text-anchor':'left','text-offset':[.65,0],'text-max-width':18,'text-padding':5},paint:{'text-color':dark,'text-halo-color':'#fffdf7','text-halo-width':2}},'station-names');
  map.addLayer({id:'historic-selected-point',type:'circle',source:'historic-points',filter:['==',['get','i'],-999],layout:hidden,paint:{'circle-radius':7,'circle-color':'#fffdf7','circle-stroke-color':dark,'circle-stroke-width':3}},'selected-dot');
  map.addLayer({id:'historic-selected-name',type:'symbol',source:'historic-points',filter:['==',['get','i'],-999],layout:{...hidden,'text-field':['get','n'],'text-font':font,'text-size':16,'text-anchor':'left','text-offset':[.7,0],'text-allow-overlap':true,'text-ignore-placement':true},paint:{'text-color':dark,'text-halo-color':'#fffdf7','text-halo-width':3}},'selected-name');
  installed=true;updateNames();
 }
 function bounds(feature){let minx=180,miny=90,maxx=-180,maxy=-90;function walk(x){if(typeof x[0]==='number'){minx=Math.min(minx,x[0]);maxx=Math.max(maxx,x[0]);miny=Math.min(miny,x[1]);maxy=Math.max(maxy,x[1]);}else x.forEach(walk);}walk(feature.geometry.coordinates);return [[minx,miny],[maxx,maxy]];}
 function popupContent(record){
  const node=element('div');node.append(element('div','popup-kicker',labels[record.kind]||'Historic railway'),element('div','popup-title',record.name||record.en||'Unnamed railway site'));
  if(record.en&&record.en!==record.name)node.append(element('div','popup-en',record.en));
  if(record.operator)node.append(element('div','popup-detail',record.operator));
  const types=[record.railway_kind,record.lifecycle].filter(Boolean).map(x=>String(x).replaceAll('_',' '));if(types.length)node.append(element('div','popup-detail',types.join(' · ')));
  node.append(element('div','quality',qualityLabels[record.geometry_quality]||record.geometry_quality||'Historical source location'));
  if(record.positional_uncertainty_m)node.append(element('div','popup-detail',`Location uncertainty: approximately ${Number(record.positional_uncertainty_m).toLocaleString()} m.`));
  for(const date of record.dates||[]){if(!date.value)continue;const detail=element('div','popup-detail',`${date.label||'Source date'}: ${date.value}`);if(date.scope)detail.append(element('div','popup-date-scope',date.scope));node.append(detail);}
  const notes=Array.isArray(record.notes)?record.notes:record.notes?[record.notes]:[];for(const note of notes)node.append(element('div','popup-detail',note));
  if(record.credit)node.append(element('div','popup-detail',`Source: ${record.credit}`));
  (record.source_urls||[]).forEach((url,i)=>sourceLink(node,i?'Additional source':'Historical source',url));
  const licenses={'ODbL':'https://opendatacommons.org/licenses/odbl/1-0/','ODbL-1.0':'https://opendatacommons.org/licenses/odbl/1-0/','CC-BY-4.0':'https://creativecommons.org/licenses/by/4.0/','CC-BY-3.0':'https://creativecommons.org/licenses/by/3.0/','CC0-1.0':'https://creativecommons.org/publicdomain/zero/1.0/'};
  if(record.license){const url=licenses[record.license]||(/^https?:\/\//.test(record.license)?record.license:null);if(url)sourceLink(node,record.license,url);else node.append(element('div','popup-detail',`License: ${record.license}`));}
  (record.license_urls||[]).forEach((url,i)=>sourceLink(node,i?'Additional license terms':'License terms',url));
  return node;
 }
 function select(i,fly=true,xy=null){
  if(!enabled)return;const record=recordById.get(Number(i));if(!record)return;
  closeCurrentSelection();clearSelection();selected=record;
  if(record.kind==='line'){
   const feature=lineById.get(record.i);if(!feature)return;const box=bounds(feature);
   xy=xy||[(box[0][0]+box[1][0])/2,(box[0][1]+box[1][1])/2];
   map.setFilter('historic-selected-line',['==',['get','i'],record.i]);if(fly)map.fitBounds(box,{padding:80,maxZoom:15,duration:800});
  }else{
   xy=record.xy||data.points.features.find(f=>Number(f.properties.i)===record.i)?.geometry.coordinates;if(!xy)return;
   for(const id of ['historic-selected-point','historic-selected-name'])map.setFilter(id,['==',['get','i'],record.i]);
   if(fly)map.flyTo({center:xy,zoom:Math.max(map.getZoom(),16),duration:900});
  }
  popup=new ml.Popup({maxWidth:'345px',closeOnClick:false}).setLngLat(xy).setDOMContent(popupContent(record)).addTo(map);$('results').replaceChildren();if(innerWidth<760)$('sidebar').classList.remove('open');
 }
 function hit(event,pointsOnly=false){
  if(!enabled)return false;const layers=pointsOnly?pointsToggle.checked?['historic-stations','historic-sites','historic-point-names']:[]:['historic-lines','historic-line-names'];if(!layers.length)return false;
  const hits=map.queryRenderedFeatures([[event.point.x-6,event.point.y-6],[event.point.x+6,event.point.y+6]],{layers});if(!hits.length)return false;select(Number(hits[0].properties.i),false,[event.lngLat.lng,event.lngLat.lat]);return true;
 }
 async function setEnabled(next){
  desired=Boolean(next);toggle.checked=desired;child.hidden=!desired;pointsToggle.disabled=!desired;urlState();const current=++revision;
  if(!desired){enabled=false;visible();clearSelection();setAttribution('');status.hidden=true;onSearchChange();return;}
  status.hidden=false;status.textContent='Loading historical railways…';
  try{
   if(!pending)pending=Promise.resolve().then(loadData).then(value=>{data=value;for(const r of data.records){recordById.set(Number(r.i),r);}for(const f of data.lines.features)lineById.set(Number(f.properties.i),f);entries=data.records.map(r=>({type:'history',kind:r.kind,i:r.i,n:r.name||r.en||'Unnamed railway site',en:r.en||'',o:r.operator||'',key:norm([r.name,r.en,r.operator,...(r.aliases||[])].filter(Boolean).join(' '))}));return data;}).catch(error=>{pending=null;throw error;});
   await pending;if(current!==revision||!desired)return;install();enabled=true;visible();setAttribution(data.attribution_html||'');status.hidden=true;onSearchChange();
  }catch(error){console.warn('Historical railways:',error);if(current!==revision)return;desired=false;enabled=false;toggle.checked=false;child.hidden=true;pointsToggle.disabled=true;visible();setAttribution('');urlState();status.hidden=false;status.textContent='Historical railways could not load. Select the layer to try again.';onSearchChange();}
 }
 function init(){toggle.disabled=false;const params=new URLSearchParams(location.search);pointsToggle.checked=params.get('history-points')!=='0';toggle.onchange=()=>setEnabled(toggle.checked);pointsToggle.onchange=()=>{visible();urlState();};if(params.get('history')==='1')setEnabled(true);}
 return {init,setEnabled,updateNames,clearSelection,select,hit,labels,get enabled(){return enabled;},get data(){return data;},get searchEntries(){return enabled?entries:[];},get backgroundBefore(){return installed?'historic-lines':'line-ferry_suspended';},get attributionText(){return enabled?(data.attribution_text||''):'';},pointer(event){if(!enabled)return false;return map.queryRenderedFeatures(event.point,{layers:['historic-lines',...(pointsToggle.checked?['historic-stations','historic-sites','historic-point-names']:[])]}).length>0;}};
}
