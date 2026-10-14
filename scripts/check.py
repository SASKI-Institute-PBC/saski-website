from pathlib import Path
import hashlib
from html.parser import HTMLParser
from urllib.parse import urlparse
import json, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]/'dist'
GA_ID='G-KN2FB37JB4'
SITE_PUBLIC='content="index,follow"' in (ROOT/'index.html').read_text()
class Page(HTMLParser):
    def __init__(self): super().__init__(); self.tags=[]; self.ld=[]; self.in_ld=False; self.data=''
    def handle_starttag(self,tag,attrs):
        a=dict(attrs); self.tags.append((tag,a))
        if tag=='script' and a.get('type')=='application/ld+json': self.in_ld=True; self.data=''
    def handle_data(self,data):
        if self.in_ld: self.data+=data
    def handle_endtag(self,tag):
        if tag=='script' and self.in_ld: self.ld.append(json.loads(self.data)); self.in_ld=False
pages=[p for p in ROOT.rglob('*.html') if 'assets' not in p.relative_to(ROOT).parts]; canonical_seen=set(); descriptions=set()
for file in pages:
    source=file.read_text()
    route=file.parent.relative_to(ROOT).as_posix()
    if route=='believe-even-when-they-dont':
        assert 'content="noindex,follow"' in source
        assert '/founders-story/' in source
        continue
    if route=='receipt-anatomy':
        assert hashlib.sha256(file.read_bytes()).hexdigest()=='90248fa1ad45afc643b11ed3d53f4afe47b21cf42de91ed334fea931ef391f00'
        continue
    p=Page(); p.feed(source); tags=p.tags
    assert sum(t=='h1' for t,a in tags)==1,file
    assert sum(t=='main' for t,a in tags)==1,file
    assert any(t=='html' and a.get('lang')=='en' for t,a in tags),file
    canonical=[a['href'] for t,a in tags if t=='link' and a.get('rel')=='canonical']
    assert len(canonical)==1 and canonical[0] not in canonical_seen,file
    canonical_seen.add(canonical[0]); parsed=urlparse(canonical[0])
    if file.name=='404.html': suffix='/404/'
    elif route=='.': suffix='/'
    else: suffix='/'+route+'/'
    prefix=parsed.path[:-len(suffix)]
    meta={a.get('name',a.get('property')):a.get('content') for t,a in tags if t=='meta'}
    assert meta['description'] not in descriptions,file
    descriptions.add(meta['description'])
    for key in ['description','robots','og:title','og:description','og:type','og:url','og:image','og:image:secure_url','og:image:type','og:image:width','og:image:height','og:image:alt','twitter:card','twitter:title','twitter:description','twitter:image','twitter:image:alt']: assert meta.get(key), (file,key)
    assert meta['og:url']==canonical[0],file
    assert meta['og:image']==meta['og:image:secure_url']==meta['twitter:image'],file
    assert meta['og:image'].endswith('/assets/social-share.png'),file
    assert meta['twitter:card']=='summary_large_image',file
    assert p.ld and p.ld[0]['@context']=='https://schema.org',file
    analytics_expected=SITE_PUBLIC and meta['robots']!='noindex,nofollow'
    assert (GA_ID in source)==analytics_expected,file
    assert ('data-analytics-consent' in source)==analytics_expected,file
    ids={a['id'] for t,a in tags if 'id' in a}
    for t,a in tags:
        target=a.get('href') if t=='a' else a.get('src') if t in ['script','img','iframe'] else a.get('href') if t=='link' and a.get('rel') in ['stylesheet','icon'] else None
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
assert len(listed)==15
assert listed.issubset(canonical_seen | {loc for loc in listed if loc.endswith('/receipt-anatomy/')})
attestation=(ROOT/'ai-attestation'/'index.html').read_text()
assert 'AI Attestation and Signed Decision Receipts' in attestation
assert '"@type": "TechArticle"' in attestation
assert '"@type": "FAQPage"' in attestation
assert (ROOT/'robots.txt').read_text().startswith('User-agent: *')
assert (ROOT/'assets/social-share.png').is_file()
assert (ROOT/'receipt-test-public-key.txt').read_text().strip()=='uAKiced9sck1tT/LJ82Vw9ouImOqVNYHYn1+STp6MzM='
anatomy=(ROOT/'receipt-anatomy'/'index.html').read_text()
assert 'Anatomy of a SASKI receipt' in anatomy
story=(ROOT/'founders-story'/'index.html').read_text()
assert "Just Because You Can't See It Doesn't Mean It Isn't Real" in story
assert 'class="wrap story-article"' in story
assert '"@type": "Article"' in story
assert '/founders-story/' not in story.split('<nav id="navigation"',1)[1].split('</nav>',1)[0]
assert "Founder's Story" in story.split('<footer>',1)[1]
legacy_story=(ROOT/'believe-even-when-they-dont'/'index.html').read_text()
assert 'window.location.replace' in legacy_story and '/founders-story/' in legacy_story
workflow=(ROOT/'assets/agentic-enterprise-workflow.html').read_text()
assert '<meta charset="utf-8">' in workflow
assert 'prefers-reduced-motion' in workflow
assert not any(claim in workflow for claim in ['UNDER 50MS','BIP-340','SCHNORR','RFC 8785','Zero Socket','NO UNMONITORED','Ed25519','policy_ver'])
assert (ROOT/'llms.txt').read_text().startswith('# SASKI Institute PBC')
assert not (ROOT/'CNAME').exists()
print(f'PASS: {len(pages)} HTML pages; internal links, assets, metadata, JSON-LD, labels, sitemap, and no domain change.')
