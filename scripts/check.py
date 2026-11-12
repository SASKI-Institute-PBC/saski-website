from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]/'dist'
class Page(HTMLParser):
    def __init__(self): super().__init__(); self.tags=[]
    def handle_starttag(self,tag,attrs): self.tags.append((tag,dict(attrs)))

pages=[p for p in ROOT.rglob('*.html') if 'assets' not in p.relative_to(ROOT).parts]
canonicals=set()
redirect_routes={'agentic','sdk','enterprise-ai-governance','estate','ai-watch','enterprise-ai','contact','believe-even-when-they-dont','educators/storybook','receipt-anatomy','tiktok'}
for file in pages:
    source=file.read_text(); route=file.parent.relative_to(ROOT).as_posix()
    if route in {'receipt-anatomy','tiktok'}:
        continue
    if route in redirect_routes:
        assert 'window.location.replace' in source and 'rel="canonical"' in source
        continue
    p=Page(); p.feed(source); tags=p.tags
    assert sum(t=='h1' for t,a in tags)==1,file
    assert sum(t=='main' for t,a in tags)==1,file
    canonical=[a['href'] for t,a in tags if t=='link' and a.get('rel')=='canonical']
    assert len(canonical)==1 and canonical[0] not in canonicals,file
    canonicals.add(canonical[0])
    for t,a in tags:
        target=a.get('href') if t=='a' else a.get('src') if t in {'script','img','iframe'} else None
        if not target: continue
        u=urlparse(target)
        if u.scheme or u.netloc or not u.path: continue
        dest=ROOT/u.path.lstrip('/')
        if u.path.endswith('/'): dest=dest/'index.html'
        assert dest.is_file(),(file,target)

home=(ROOT/'index.html').read_text()
assert '<a class="button" href="/saski/">Explore SASKI' in home
assert 'One product, three checks.' in home and 'MyTrusted.ai' in home
saski=(ROOT/'saski'/'index.html').read_text()
required_anchors=['overview','checks','action-gate','chat-gate','deployments','attestation','ship','openshell','enterprise','tokens','contact']
for anchor in required_anchors:
    assert f'id="{anchor}"' in saski
for text in ['Input','Action','Output','SASKI Cloud','SASKI Gateway','SASKI Replay','OpenShell lab']:
    assert text in saski
replay=(ROOT/'replay'/'index.html').read_text()
for text in ['included in the subscription','Nothing is uploaded','tool-call logs','unsigned']:
    assert text in replay
for slug in ['financial-services','estate','education','healthcare','hiring','it-operations']:
    assert (ROOT/'solutions'/slug/'index.html').is_file(),slug
redirects={'agentic':'/saski/#action-gate','sdk':'/saski/#chat-gate','enterprise-ai-governance':'/saski/#enterprise','estate':'/solutions/estate/'}
for old,target in redirects.items():
    redirect=(ROOT/old/'index.html').read_text()
    assert 'content="noindex,follow"' in redirect and 'window.location.replace' in redirect,(old,redirect)
    assert target in redirect,(old,target)
    parsed=urlparse(target)
    destination=ROOT/parsed.path.strip('/')/'index.html'
    assert destination.is_file(),(old,target)
    if parsed.fragment:
        assert f'id="{parsed.fragment}"' in destination.read_text(),(old,target)
nav=home.split('<nav id="navigation"',1)[1].split('</nav>',1)[0]
for text in ['SASKI','SASKI Replay','Solutions','How it works','Attestation','Resources','About','Request a demo']:
    assert text in nav,text
for first,second in zip(['SASKI','SASKI Replay','Solutions','How it works','Attestation','Resources','About','Request a demo'],['SASKI Replay','Solutions','How it works','Attestation','Resources','About','Request a demo','Request a demo']):
    if first!=second:
        assert nav.index(first)<nav.index(second),(first,second)
listed={e.text for e in ET.parse(ROOT/'sitemap.xml').getroot().iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
assert any(loc.endswith('/saski/') for loc in listed)
assert any(loc.endswith('/solutions/financial-services/') for loc in listed)
assert not any(urlparse(loc).path.rstrip('/') == '/'+route for route in redirects for loc in listed),listed
footer=home.split('<footer>',1)[1].split('</footer>',1)[0]
for href,label in [('/saski/','SASKI'),('/replay/','SASKI Replay'),('/solutions/','Solutions'),('/ai-attestation/','Attestation')]:
    assert f'href="{href}">{label}</a>' in footer,(href,label)
estate=(ROOT/'solutions'/'estate'/'index.html').read_text()
assert 'https://www.youtube-nocookie.com/embed/Wr70W4wsSAg' in estate
forbidden=['SASKI SDK','SASKI Agentic','Enterprise AI Governance','SASKI Estate','Shadow Mode','coming soon','in development']
for file in [*ROOT.rglob('*.html'),ROOT/'sitemap.xml',ROOT/'llms.txt']:
    source=file.read_text().lower()
    for term in forbidden:
        assert term.lower() not in source,(file,term)
for brand in ['Q-SYS','Crestron','Control4','RTI','WattBox']:
    for file in ROOT.rglob('*.html'):
        if brand in file.read_text():
            assert file == ROOT/'solutions'/'estate'/'index.html',(file,brand)
print(f'PASS: {len(pages)} HTML pages; navigation, anchors, redirects, solution content, retired-copy scan, links, and sitemap.')
