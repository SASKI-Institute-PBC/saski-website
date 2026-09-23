from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import json, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]/'dist'
class Page(HTMLParser):
    def __init__(self): super().__init__(); self.tags=[]; self.ld=[]; self.in_ld=False; self.data=''
    def handle_starttag(self,tag,attrs):
        a=dict(attrs); self.tags.append((tag,a))
        if tag=='script' and a.get('type')=='application/ld+json': self.in_ld=True; self.data=''
    def handle_data(self,data):
        if self.in_ld: self.data+=data
    def handle_endtag(self,tag):
        if tag=='script' and self.in_ld: self.ld.append(json.loads(self.data)); self.in_ld=False
pages=list(ROOT.rglob('*.html')); canonical_seen=set(); descriptions=set()
for file in pages:
    p=Page(); p.feed(file.read_text()); tags=p.tags
    assert sum(t=='h1' for t,a in tags)==1,file
    assert sum(t=='main' for t,a in tags)==1,file
    assert any(t=='html' and a.get('lang')=='en' for t,a in tags),file
    canonical=[a['href'] for t,a in tags if t=='link' and a.get('rel')=='canonical']
    assert len(canonical)==1 and canonical[0] not in canonical_seen,file
    canonical_seen.add(canonical[0]); parsed=urlparse(canonical[0])
    route=file.parent.relative_to(ROOT).as_posix()
    if file.name=='404.html': suffix='/404/'
    elif route=='.': suffix='/'
    else: suffix='/'+route+'/'
    prefix=parsed.path[:-len(suffix)]
    meta={a.get('name',a.get('property')):a.get('content') for t,a in tags if t=='meta'}
    assert meta['description'] not in descriptions,file
    descriptions.add(meta['description'])
    for key in ['description','robots','og:title','og:description','og:type','og:url','twitter:card','twitter:title','twitter:description']: assert meta.get(key), (file,key)
    assert meta['og:url']==canonical[0],file
    assert p.ld and p.ld[0]['@context']=='https://schema.org',file
    ids={a['id'] for t,a in tags if 'id' in a}
    for t,a in tags:
        target=a.get('href') if t=='a' else a.get('src') if t in ['script','img'] else a.get('href') if t=='link' and a.get('rel') in ['stylesheet','icon'] else None
        if not target: continue
        u=urlparse(target)
        if u.scheme or u.netloc: continue
        if not u.path:
            if u.fragment: assert u.fragment in ids,(file,target)
            continue
        assert u.path.startswith(prefix+'/'),(file,target,prefix)
        dest=ROOT/u.path[len(prefix):].lstrip('/')
        if u.path.endswith('/'): dest=dest/'index.html'
        assert dest.is_file(),(file,target)
    for t,a in tags:
        if t=='img': assert 'alt' in a and a.get('width') and a.get('height'),(file,a)
        if t=='input': assert any(lt=='label' and la.get('for')==a.get('id') for lt,la in tags),(file,a)
urls=ET.parse(ROOT/'sitemap.xml').getroot()
listed={e.text for e in urls.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
assert len(listed)==11
assert listed.issubset(canonical_seen)
assert (ROOT/'robots.txt').read_text().startswith('User-agent: *')
assert not (ROOT/'CNAME').exists()
print(f'PASS: {len(pages)} HTML pages; internal links, assets, metadata, JSON-LD, labels, sitemap, and no domain change.')
