#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 MH
"""Normalize licensed historical inputs into the embedded layer (standard library only)."""
from __future__ import annotations
import collections
import csv
import gzip
import hashlib
import json
import math
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
INPUT=ROOT/'data/history'
OUTPUT=ROOT/'data/history.json.gz'


def read(name):
    p=INPUT/name
    return json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes())


def clean(value):
    return str(value or '').strip()


def unique(items):
    return list(dict.fromkeys(item for item in items if item))


def name_key(name):
    name=re.sub(r'^(?:旧|国鉄|JR)+','',name)
    name=re.sub(r'(?:駅跡|駅|廃線跡|線跡|跡)$','',name)
    return re.sub(r'[\s・　()（）\[\]]','',name)


def near_metres(a,b):
    dx=(a[0]-b[0])*111320*math.cos(math.radians((a[1]+b[1])/2))
    dy=(a[1]-b[1])*111320
    return math.hypot(dx,dy)


def in_hokkaido(xy):
    # Exclude Shimokita across the Tsugaru Strait: northern Honshu also
    # reaches above 41.3 N and would otherwise enter a rectangular count.
    lon,lat=xy
    return 139<=lon<=146 and 41.3<=lat<=46 and (lon<=140.6 or lat>=41.65)


def rounded(coords):
    if isinstance(coords[0],(int,float)):
        return [round(float(v),6) for v in coords[:2]]
    return [rounded(v) for v in coords]


def infer_kind(p):
    explicit=clean(p.get('historical_use') or p.get('former_kind') or p.get('railway') or p.get('mode'))
    text=' '.join(clean(p.get(k)) for k in ['name','operator','source_folder','usage'])
    if explicit=='industrial' or re.search(r'製糖|森林|林用|炭鉱|炭砿|鉱山|専用鉄道|燐鉱',text):return 'Industrial / forest railway'
    if explicit=='rural_tramway' or '簡易軌道' in text or '殖民' in text:return 'Rural light railway'
    return {'tram':'Tramway','light_rail':'Light railway','funicular':'Funicular','monorail':'Monorail','rail':'Railway','station':'Railway','stop':'Railway','halt':'Railway'}.get(explicit,'Railway')


def feature_id(f,p,component):
    if p.get('history_id'):return p['history_id']
    if p.get('id'):return p['id']
    return clean(f.get('id')) or component+'-'+hashlib.sha256(json.dumps(f,sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:20]


def normalize(f,component):
    p=f['properties'];geom={'type':f['geometry']['type'],'coordinates':rounded(f['geometry']['coordinates'])}
    ispoint=geom['type']=='Point'
    kind='site' if p.get('kind')=='site' else 'station' if ispoint else 'line'
    name=clean(p.get('name') or p.get('name_ja'))
    en=clean(p.get('name_en') or p.get('name_rm'))
    urls=[];dates=[];notes=[]
    def date(label,value,scope=''):
        if value:dates.append({'label':label,'value':str(value),'scope':scope})
    q='mapped'
    if component=='osm':
        license_='ODbL-1.0';credit='© OpenStreetMap contributors';urls=[p.get('source_url')]
        date('Recorded start',p.get('start_date'),'Source tag for this mapped object; not necessarily the opening of the entire railway.')
        date('Recorded end',p.get('end_date'),p.get('end_date_type') or 'Source tag for this mapped object; not necessarily the closure of the entire railway.')
        notes.append('Mapped former infrastructure or remnant. Missing connections have not been reconstructed.')
        tags=p.get('tags',{})
        for key in ['description','description:en','note']:
            if tags.get(key) and not tags[key].startswith('National-Land Numerical'):notes.append(tags[key][:900])
        if p.get('notes'):notes.append(p['notes'])
        urls+=p.get('sources',[])
    elif component.startswith('naebo'):
        license_='CC-BY-4.0';credit='© 2007–2026 苗穂工房 / naeboworks; GSI aerial-photo reference. Adapted.'
        urls=[p.get('source_url'),p.get('source_data_url'),'https://naeboworks.com/haisen/about.htm']
        q='source_reconstruction'
        for label,key in [('Passenger closure','passenger_closed_date'),('Passenger closure','passenger_closed_year'),('Recorded closure','closed_date'),('Recorded closure','closed_year'),('Signal-box closure','signal_closed_date')]:
            value=p.get(key)
            if value and not any(d['label']==label or (label=='Recorded closure' and d['label']=='Passenger closure') for d in dates):date(label,value,'Source-recorded event for this station/site.')
        notes.append('Historical alignment/site reconstructed by 苗穂工房 from aerial photographs. Coordinates are source locations, not survey measurements.')
        if p.get('source_notes_ja'):notes.append(p['source_notes_ja'])
        if 'estimated' in clean(p.get('confidence')):notes.append('The source explicitly marks this location as approximate.')
        # Regional KML top folders can be the project title, rather than a railway.
        folders=p.get('source_folder','').split(' / ')
        line=next((x for x in reversed(folders) if not x.endswith('(駅)') and not x.startswith('北海道廃線路線図')),p.get('line_ja',''))
        p=dict(p);p['line_alias']=line
    elif component=='ohm':
        license_='CC0-1.0';credit='OpenHistoricalMap contributors';urls=[p.get('source_url')]
        periods=p.get('periods') or [{'start_date':p.get('start_date'),'end_date':p.get('end_date')}]
        for period in periods:
            a=period.get('start_date') or '?';b=period.get('end_date') or '?'
            date('Mapped feature period',f'{a} – {b}','This period can describe a former alignment or identity; it is not necessarily the lifetime of the whole railway.')
        notes.append('Historical community-mapped geometry. Current-overlap identities were conservatively screened; coverage remains partial.')
    else:
        license_=p.get('license','CC0-1.0');credit=p.get('attribution','Original factual annotation; source credited below.')
        urls=p.get('sources',[]);q=p.get('geometry_quality','site_only')
        if component=='kitadaito':license_='CC0-1.0'
        if p.get('network_closure_year'):date('Network closure',p['network_closure_year'],'Network-level event; individual branches are not independently dated.')
        if p.get('documented_site_period'):date('Documented site period',p['documented_site_period'],'Industrial-site period, not a surveyed track operating interval.')
        if p.get('end_date'):date('Railway network closure',p['end_date'],'The factory itself may still operate; this date concerns its former railway.')
        if p.get('documented_date'):date('Documented in',p['documented_date'])
        if p.get('notes'):notes.append(p['notes'])
        if p.get('geometry_epoch'):notes.append(p['geometry_epoch'])
    name= name or en
    record={'id':feature_id(f,p,component),'kind':kind,'name':name or ('Unnamed former station' if ispoint else 'Unnamed former railway'),
            'en':en,'operator':clean(p.get('operator')),'lifecycle':clean(p.get('lifecycle') or p.get('status') or 'former'),
            'railway_kind':infer_kind(p),'geometry_quality':q,'source_urls':unique(urls),'license':license_,'credit':credit,
            'dates':dates,'notes':unique(notes),'aliases':unique([p.get('line_alias'),p.get('line_ja'),p.get('source_label'),*(p.get('alternate_names') or [])]),
            'source_component':component,'source_ids':[feature_id(f,p,component)],'gauge':clean(p.get('gauge'))}
    if p.get('positional_uncertainty_m'):record['positional_uncertainty_m']=p['positional_uncertainty_m']
    if p.get('license_urls'):record['license_urls']=p['license_urls']
    if component=='okinawa' and '大東' in name:
        record['aliases']+=['南大東島','南大東製糖鉄道','Minami-Daito sugar railway','Minamidaito']
    if ispoint:record['xy']=geom['coordinates']
    record['_label']=name
    return record,geom


def group_connected_osm(items):
    """Group only identically named/dated OSM ways sharing an actual source vertex."""
    buckets=collections.defaultdict(list);passthrough=[]
    generic={'廃線跡','廃線','専用線','軌道','森林鉄道','旧線','abandoned railway'}
    for r,g in items:
        if r['source_component']!='osm' or r['kind']!='line' or not r['_label'] or r['_label'] in generic:
            passthrough.append((r,g));continue
        key=(r['name'],r['operator'],r['lifecycle'],r['railway_kind'],r['gauge'],json.dumps(r['dates'],sort_keys=True))
        buckets[key].append((r,g))
    for entries in buckets.values():
        parent=list(range(len(entries)))
        def root(i):
            while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
            return i
        vertices={}
        for j,(r,g) in enumerate(entries):
            for v in g['coordinates']:
                v=tuple(v)
                if v in vertices:parent[root(j)]=root(vertices[v])
                else:vertices[v]=j
        components=collections.defaultdict(list)
        for j,item in enumerate(entries):components[root(j)].append(item)
        for group in components.values():
            r=dict(group[0][0]);geoms=[g['coordinates'] for _,g in group]
            if len(group)>1:
                ids=sorted(rid for record,_ in group for rid in record['source_ids'])
                r['id']='osm-connected-'+hashlib.sha256('\n'.join(ids).encode()).hexdigest()[:20];r['source_ids']=ids
                r['source_urls']=unique(url for record,_ in group for url in record['source_urls'])[:8]
                r['notes']=unique(note for record,_ in group for note in record['notes'])[:6]
            passthrough.append((r,{'type':'LineString','coordinates':geoms[0]} if len(geoms)==1 else {'type':'MultiLineString','coordinates':geoms}))
    return passthrough


def build():
    conflicts=read('current-history-conflicts.json')
    excluded=set(conflicts['exclude_history_osm_ids'])
    updates={r['history_id']:r['set'] for r in conflicts.get('historical_updates',[])}
    closure_review=read('current_station_closure_review.json')
    date_updates={r['historical_id']:r for r in closure_review['proposals'] if r.get('action')=='enrich_historical_closure_date' and r.get('safe_to_apply')}
    coal={r.get('id'):r for r in read('industrial-coal-review.json')['osm_reviews'] if r.get('id')}
    inputs=[('naebo_hokkaido','naeboworks-hokkaido.geojson.gz'),('naebo_regions','naeboworks-regions.geojson.gz'),('osm','osm.geojson.gz'),('ohm','ohm.geojson.gz'),('okinawa','okinawa-sugar.geojson.gz'),('kitadaito','kitadaito-site.geojson')]
    items=[];audit=[]
    for component,filename in inputs:
        for f in read(filename)['features']:
            p=f['properties']
            if component=='osm':
                raw=('n' if p['osm_type']=='node' else 'w')+str(p['osm_id'])
                if raw in excluded:audit.append({'id':p['id'],'decision':'omit','reason':'Active, suspended or flood-damaged infrastructure; historical closure not established.'});continue
                if p['id'] in updates:p=dict(p);p.update(updates[p['id']]);f=dict(f);f['properties']=p
            r,g=normalize(f,component)
            if r['id'] in date_updates:
                change=date_updates[r['id']]
                r['dates']=[{'label':'Passenger closure','value':change['closed_date'],'scope':'Station closure confirmed by the operator timetable-change notice.'}]
                r['source_urls']=unique(r['source_urls']+[change['source_url']])
            if r['id'] in coal:
                c=coal[r['id']];r['railway_kind']='Industrial / forest railway';r['source_urls']=unique(r['source_urls']+c['source_urls'])
                r['dates']=[{'label':'Documented coal-railway operation','value':f"{c['start_year']} – {c['end_year']}",'scope':'The operated Akebono–Sankebetsu coal corridor, not the full unfinished Meiu project.'}]
                r['notes'].append('An industrial coal-working section operated here; the long never-completed continuation is excluded.')
            items.append((r,g))
    # Prefer source-documented Naeboworks points over a close identical-name copy.
    # Do not combine attributes or bridge geometry across differently licensed inputs.
    points_by_name=collections.defaultdict(list);kept=[]
    for r,g in items:
        if r['kind']=='station' and r['_label']:
            match=next((old for old in points_by_name[name_key(r['_label'])] if near_metres(old['xy'],r['xy'])<80 and old['source_component']!=r['source_component']),None)
            if match:
                audit.append({'id':r['id'],'decision':'omit_duplicate_point','displayed_id':match['id'],'distance_m':round(near_metres(match['xy'],r['xy']),1),'reason':'Same named former stop within80m from another source; original source inputs remain available.'});continue
            points_by_name[name_key(r['_label'])].append(r)
        kept.append((r,g))
    kept=group_connected_osm(kept)
    kept.sort(key=lambda pair:(pair[0]['kind'],pair[0]['source_component'],pair[0]['id']))
    records=[];lines=[];points=[]
    for i,(r,g) in enumerate(kept):
        label=r.pop('_label');r['i']=i;records.append(r)
        props={'i':i,'n':label,'en':r['en'],'label':label,'c':'#936444','kind':r['kind'],'q':r['geometry_quality']}
        feature={'type':'Feature','id':i,'properties':props,'geometry':g}
        (lines if r['kind']=='line' else points).append(feature)
    count={'line_features':len(lines),'station_objects':sum(r['kind']=='station' for r in records),'site_objects':sum(r['kind']=='site' for r in records),
           'hokkaido_station_objects':sum(r['kind']=='station' and in_hokkaido(r['xy']) for r in records),
           'approximate_line_features':sum(r['kind']=='line' and r['geometry_quality']=='approximate' for r in records)}
    credits='History: ©苗穂工房 / naeboworks (CC BY4.0, adapted; GSI aerial-photo / site-coordinate references) · OpenHistoricalMap (CC0) · Tamurono157 (CC BY3.0, adapted) · OSM (ODbL).'
    html='History: <a href="https://naeboworks.com/haisen/" target="_blank" rel="noopener">©苗穂工房</a> (<a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">CC BY4.0</a>, adapted; GSI aerial-photo / site-coordinate references) · <a href="https://www.openhistoricalmap.org/copyright" target="_blank" rel="noopener">OpenHistoricalMap (CC0)</a> · <a href="https://commons.wikimedia.org/wiki/File:Minami-Daito-Sugartrain-line.gif" target="_blank" rel="noopener">Tamurono157</a> (<a href="https://creativecommons.org/licenses/by/3.0/" target="_blank" rel="noopener">CC BY3.0</a>, adapted)'
    sources={'osm':{'name':'OpenStreetMap','license':'ODbL-1.0','url':'https://www.openstreetmap.org/copyright'},'naeboworks':{'name':'苗穂工房','license':'CC-BY-4.0','url':'https://naeboworks.com/haisen/'},'ohm':{'name':'OpenHistoricalMap','license':'CC0-1.0','url':'https://www.openhistoricalmap.org/copyright'},'sugar_diagram':{'name':'Tamurono157','license':'CC-BY-3.0','url':'https://commons.wikimedia.org/wiki/File:Minami-Daito-Sugartrain-line.gif'}}
    payload={'schema_version':1,'lines':{'type':'FeatureCollection','features':lines},'points':{'type':'FeatureCollection','features':points},'records':records,'count':count,'sources':sources,'attribution_html':html,'attribution_text':credits,'period_policy':'All recorded eras combined; no simultaneous-network claim. Source dates retain their individual scopes.'}
    OUTPUT.write_bytes(gzip.compress(json.dumps(payload,ensure_ascii=False,separators=(',',':')).encode(),compresslevel=9,mtime=0))
    (INPUT/'integration-audit.json').write_text(json.dumps({'counts':count,'decisions':audit,'grouping':'Only identically named/dated OSM sections sharing a source vertex are grouped. No missing geometry or source dates are inferred.'},ensure_ascii=False,indent=2)+'\n')
    with (INPUT/'stations-and-sites.csv').open('w',newline='') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['id','kind','name','name_en','longitude','latitude','source_component','geometry_quality','license','sources'])
        for r in records:
            if r['kind']!='line':w.writerow([r['id'],r['kind'],r['name'],r['en'],*r['xy'],r['source_component'],r['geometry_quality'],r['license'],' | '.join(r['source_urls'])])
    print(json.dumps(count,indent=2));print(f'Historical payload: {OUTPUT.stat().st_size:,} bytes')
    return payload

if __name__=='__main__':build()
