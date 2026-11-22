from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1] / 'dist'
REDIRECTS = {'agentic': '/saski/', 'sdk': '/saski/', 'enterprise-ai-governance': '/replay/', 'estate': '/solutions/', 'ai-attestation': '/attestation/'}
ARCHIVES = {'blog/the-quiet-consensus--why-ai-safety-is-moving-out-of-the-model-and-into-middleware', 'blog/enterprise-ai-pricing-trap'}

class Page(HTMLParser):
    def __init__(self): super().__init__(); self.tags = []; self.text = []
    def handle_starttag(self, tag, attrs): self.tags.append((tag, dict(attrs)))
    def handle_data(self, data): self.text.append(data)

def parse(path):
    page = Page(); page.feed(path.read_text()); return page

def route_file(path):
    route = path.strip('/')
    return ROOT / route / 'index.html' if route else ROOT / 'index.html'

html_pages = list(ROOT.rglob('*.html'))
live_pages = [p for p in html_pages if p.parent.relative_to(ROOT).as_posix() not in REDIRECTS]
for file in live_pages:
    page = parse(file)
    for tag, attrs in page.tags:
        target = attrs.get('href') if tag == 'a' else attrs.get('src') if tag in {'script', 'img', 'iframe'} else None
        if not target: continue
        parsed = urlparse(target)
        if parsed.scheme or parsed.netloc or not parsed.path or parsed.path.startswith('/assets/'): continue
        dest = route_file(parsed.path)
        assert dest.is_file(), (file, target)
        if parsed.fragment: assert f'id="{parsed.fragment}"' in dest.read_text(), (file, target)

home = (ROOT / 'index.html').read_text()
assert '<a class="button" href="/contact-us/">Request a Shadow Replay' in home
assert 'MyTrusted' not in home and 'href="/saski/">Explore SASKI' not in home
qa_path = 'qa-chat-embed-test-7k3'
qa = (ROOT / qa_path / 'index.html').read_text()
assert '<h1>Internal QA test page</h1>' in qa
assert 'content="noindex, nofollow"' in qa
assert 'https://sitegpt.ai/widget/5e8810a7-ad4b-494f-9f0d-5dea50c32e5d.js' in qa
for unwanted in ['site.css', 'site.js', 'googletagmanager.com', 'SASKI_GA_ID', '<nav', '<footer', 'consent-banner', 'livechatai.com', 'chatbase.co', 'botpress.cloud', 'bpcontent.cloud']:
    assert unwanted not in qa, unwanted
saski = (ROOT / 'saski' / 'index.html').read_text()
for anchor in ['overview','checks','action-gate','chat-gate','deployments','attestation','ship','openshell','enterprise','tokens','contact']:
    assert f'id="{anchor}"' in saski, anchor
assert 'youtube-nocookie.com/embed/Wr70W4wsSAg' in (ROOT / 'solutions' / 'estate' / 'index.html').read_text()

for old, target in REDIRECTS.items():
    source = (ROOT / old / 'index.html').read_text()
    assert 'http-equiv="refresh" content="0;' in source and 'window.location.replace' in source, old
    assert 'rel="canonical"' in source and 'noindex' in source and 'This page has moved' in source and target in source, old
    parsed = urlparse(target); destination = route_file(parsed.path)
    assert destination.is_file(), (old, target)
    if parsed.fragment: assert f'id="{parsed.fragment}"' in destination.read_text(), (old, target)

nav = home.split('<nav id="navigation"', 1)[1].split('</nav>', 1)[0]
nav_order = ['SASKI', 'SASKI Replay', 'Solutions', 'How it works', 'Attestation', 'Resources', 'About', 'Request a Shadow Replay']
for first, second in zip(nav_order, nav_order[1:]): assert nav.index(first) < nav.index(second), (first, second)
for text in ['Findings', 'AI News', 'Illustrations', 'Tokenator', 'Press', 'Founder’s Story']: assert text in nav, text
for file in live_pages:
    source = file.read_text()
    if '<nav id="navigation"' in source:
        current = source.split('<nav id="navigation"', 1)[1].split('</nav>', 1)[0]
        assert re.sub(r' aria-current="page"', '', current) == nav, file
footer = home.split('<footer>', 1)[1].split('</footer>', 1)[0]
for href, label in [('/saski/', 'SASKI'), ('/replay/', 'SASKI Replay'), ('/solutions/', 'Solutions'), ('/attestation/', 'Attestation')]: assert f'href="{href}">{label}</a>' in footer, (href, label)

for file in live_pages:
    source = file.read_text()
    for match in re.finditer(r'<a class="[^"]*\bbutton\b[^"]*"[^>]*href="/contact-us/"[^>]*>(.*?)</a>', source, re.S):
        label = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        assert label == 'Request a Shadow Replay', (file, label)

for file in [*html_pages, ROOT / 'sitemap.xml', ROOT / 'llms.txt']:
    route = file.parent.relative_to(ROOT).as_posix() if file.suffix == '.html' else ''
    source = file.read_text().lower()
    if route not in REDIRECTS:
        for term in ['four products', 'enterprise ai governance', 'saski agentic', 'saski sdk', 'saski estate']: assert term not in source, (file, term)
    for term in ['de-risk', 'makes ai safe', 'safety middleware', 'insurers', 'regulators and insurers', 'compliance', 'exposure', 'coming soon', 'in development', 'beta', 'not yet', 'planned', 'roadmap']: assert term not in source, (file, term)
    if file.suffix == '.html': assert not any(mark in ''.join(parse(file).text) for mark in ['—', '–', '--']), file

listed = {node.text for node in ET.parse(ROOT / 'sitemap.xml').getroot().iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
listing = (ROOT / 'sitemap.xml').read_text() + (ROOT / 'llms.txt').read_text()
for route in [*REDIRECTS, *ARCHIVES]:
    assert not any(urlparse(url).path.rstrip('/') == '/'+route for url in listed), route
    assert not any(urlparse(url).path.rstrip('/') == '/'+route for url in re.findall(r'\]\((https?://[^)]+)\)', listing)), route
assert f'/{qa_path}/' not in listing
assert any(loc.endswith('/attestation/') for loc in listed) and any(loc.endswith('/solutions/') for loc in listed)
print(f'PASS: {len(html_pages)} HTML files; navigation, CTAs, anchors, redirects, links, copy scan, and discovery files.')
