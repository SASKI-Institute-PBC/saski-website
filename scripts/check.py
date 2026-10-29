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
legacy_redirects={
    'ai-watch':'resources',
    'enterprise-ai':'enterprise-ai-governance',
    'contact':'contact-us',
}
for file in pages:
    source=file.read_text()
    route=file.parent.relative_to(ROOT).as_posix()
    if route=='believe-even-when-they-dont':
        assert 'content="noindex,follow"' in source
        assert '/founders-story/' in source
        continue
    if route in legacy_redirects:
        target=legacy_redirects[route]
        assert 'content="noindex,follow"' in source
        assert f'<link rel="canonical" href="https://www.saski.io/{target}/">' in source if SITE_PUBLIC else f'/{target}/' in source
        assert 'window.location.replace' in source
        assert f'/{target}/' in source
        assert 'body{visibility:hidden}' in source
        continue
    if route=='educators/storybook':
        assert 'content="noindex,follow"' in source
        assert 'window.location.replace' in source
        assert 'docs.google.com/presentation/' in source
        assert (GA_ID in source)==SITE_PUBLIC
        assert "gtag('event','page_view'" in source if SITE_PUBLIC else True
        assert 'event_callback:openStorybook' in source if SITE_PUBLIC else True
        assert 'setTimeout(openStorybook,800)' in source if SITE_PUBLIC else True
        assert 'body{visibility:hidden}' in source
        assert '<noscript><style>body{visibility:visible}' in source
        continue
    if route=='tiktok':
        assert 'content="noindex,follow"' in source
        assert '<title>Questions About AI Safety? | SASKI Institute</title>' in source
        assert '/assets/ai-safety-live-tv-16x9.jpg' in source
        assert 'object-fit:contain' in source
        assert 'requestFullscreen' in source
        assert (ROOT/'assets'/'ai-safety-live-tv-16x9.jpg').is_file()
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
assert len(listed)==22
assert not any(loc.endswith('/tiktok/') for loc in listed)
assert listed.issubset(canonical_seen | {loc for loc in listed if loc.endswith('/receipt-anatomy/')})
attestation=(ROOT/'ai-attestation'/'index.html').read_text()
assert 'AI Attestation and Signed Decision Receipts' in attestation
assert '"@type": "TechArticle"' in attestation
assert '"@type": "FAQPage"' in attestation
assert 'A plain-English example.' in attestation
assert 'checks the Ed25519 signature without contacting SASKI' in attestation
assert 'How SASKI evidence relates to ISO/IEC 42001.' in attestation
assert 'does not establish organizational conformity with ISO/IEC 42001' in attestation
assert 'https://www.iso.org/standard/42001' in attestation
assert (ROOT/'robots.txt').read_text().startswith('User-agent: *')
assert (ROOT/'assets/social-share.png').is_file()
anatomy=(ROOT/'receipt-anatomy'/'index.html').read_text()
assert 'Anatomy of a SASKI receipt' in anatomy
assert hashlib.sha256((ROOT/'receipt-anatomy'/'index.html').read_bytes()).hexdigest()=='90248fa1ad45afc643b11ed3d53f4afe47b21cf42de91ed334fea931ef391f00'
for retired_file in ['receipt-sample.json','verify-receipt.py','receipt-test-public-key.txt']:
    assert not (ROOT/retired_file).exists(), retired_file
story=(ROOT/'founders-story'/'index.html').read_text()
assert "Just Because You Can't See It Doesn't Mean It Isn't Real" in story
assert 'class="wrap story-article"' in story
assert '"@type": "Article"' in story
assert '/founders-story/' not in story.split('<nav id="navigation"',1)[1].split('</nav>',1)[0]
assert "Founder's Story" in story.split('<footer>',1)[1]
assert story.count('assets/founders-story/')==7
assert 'STORY_MEDIA_' not in story
legacy_story=(ROOT/'believe-even-when-they-dont'/'index.html').read_text()
assert 'window.location.replace' in legacy_story and '/founders-story/' in legacy_story
home=(ROOT/'index.html').read_text()
assert 'One governance foundation for your company’s AI.' in home
assert '/enterprise-ai-governance/' in home
assert 'Experience SASKI governance in a working application.' in home
assert 'https://www.mytrusted.ai/' in home
assert 'Future enterprise chatbot packaging remains in development' in home
enterprise=(ROOT/'enterprise-ai-governance'/'index.html').read_text()
assert 'Govern existing AI or design the controls before launch.' in enterprise
assert 'https://www.mytrusted.ai/' in enterprise
assert 'Future company-chatbot packaging remains in development' in enterprise
about=(ROOT/'about'/'index.html').read_text()
assert '40+ years of multidisciplinary experience' in about
agentic=(ROOT/'agentic'/'index.html').read_text()
resources=(ROOT/'resources'/'index.html').read_text()
assert 'SASKI-conducted lab test' in agentic and 'SASKI-conducted lab test' in resources
assert 'independent lab test' not in agentic.lower() and 'independent lab test' not in resources.lower()
assert all(text in agentic for text in ['Authenticated customer lookup','$50 Stripe test charge','Unauthenticated attempts'])
assert agentic.count('Read the complete lab report (PDF)')==1
estate=(ROOT/'estate'/'index.html').read_text()
assert 'Control-system integration targets' in estate
assert 'Compatibility must be validated for each product, version, interface, and deployment.' in estate
replay=(ROOT/'replay'/'index.html').read_text()
assert 'SASKI Replay is available as a self-hosted deployment' in replay
assert 'Federal and state references' in replay
assert 'They are not legal advice' in replay
how=(ROOT/'how-it-works'/'index.html').read_text()
assert 'The governance feedback loop' in how
assert '/assets/continuous-governance-loop.webp' in how
assert all(label in how for label in ['Enforce','Signed receipt','Independent review','Improve rules'])
assert 'People remain responsible for approving rulebook changes.' in how
assert (ROOT/'assets'/'continuous-governance-loop.webp').is_file()
articles={
    'blog/the-quiet-consensus--why-ai-safety-is-moving-out-of-the-model-and-into-middleware':'The Quiet Consensus',
    'blog/8-point-safety-checklist':'Beyond the App Store',
    'blog/enterprise-ai-pricing-trap':'The Enterprise AI Pricing Trap',
}
for route,heading in articles.items():
    article=(ROOT/route/'index.html').read_text()
    assert heading in article and 'Archive note' in article
    assert 'content="index,follow"' in article if SITE_PUBLIC else 'content="noindex,follow"' in article
    assert 'data:image' not in article and '[image1]' not in article and 'SASI' not in article
    assert any(loc.endswith('/'+route+'/') for loc in listed)
quiet=(ROOT/'blog'/'the-quiet-consensus--why-ai-safety-is-moving-out-of-the-model-and-into-middleware'/'index.html').read_text()
assert 'Explore <a href="https://www.saski.io/how-it-works/"' in quiet
assert 'public <a href="https://www.mytrusted.ai/"' in quiet
assert 'techviz.us/sasi-integration' not in quiet and 'http://www.mytrusted.ai/' not in quiet
assert '<p>.</p>' not in quiet
pricing=(ROOT/'blog'/'enterprise-ai-pricing-trap'/'index.html').read_text()
assert 'historical and are not current offers' in pricing
press=(ROOT/'press'/'index.html').read_text()
assert 'Experience the safeguards.' in press
assert 'Verify the evidence yourself.' in press
assert 'info@saski.io' in press
assert 'These are company-issued materials from SASKI Institute, not independent news coverage.' in press
assert '/assets/institute-logo.png' in press and '/assets/stephen-calhoun.png' in press
news=(ROOT/'ai-news'/'index.html').read_text()
assert 'AI developments<br> worth governing.' in news
assert news.count('class="news-story"')==7
assert all(text in news for text in ['Anthropic model submitted a fabricated homicide tip','OpenAI agent gained unauthorized access','Senators demand answers from Google','New York City schools restrict student-facing generative AI','Major U.S. banks restrict unvetted AI agents','Community Bank disclosed customer data','Suspected AI-assisted attacks affected 16 South Korean financial firms'])
assert all(source in news for source in ['apnews.com','abc.net.au','blumenthal.senate.gov','hawley.senate.gov','wsj.com','schools.nyc.gov','nyc.gov','cnbc.com','axios.com','americanbanker.com','sec.gov','yna.co.kr','koreatimes.co.kr'])
assert 'SASKI did not independently investigate these events.' in news
assert 'Google has aggressively pushed Gemini into classrooms' in news
assert news.index('Recent headlines') < news.index('About this page')
assert '/ai-news/' in (ROOT/'index.html').read_text().split('<nav id="navigation"',1)[1].split('</nav>',1)[0]
assert any(loc.endswith('/ai-news/') for loc in listed)
illustrations=(ROOT/'illustrations'/'index.html').read_text()
assert 'AI governance,<br> illustrated.' in illustrations
assert illustrations.count('class="illustration-card"')==9
assert illustrations.count('data-illustration-open')==9
assert all(text in illustrations for text in ['The Memory Defense','Where’s the Evidence?','Empty Binder, Empty Promises','The Incident Report Shredder','The Proof Problem','The Safety Feedback Loop','The Missing Version','Who Authorizes the Authorizers?','Investigating With What?','Governance must leave evidence.'])
assert 'SASKI Educator Storybook' in illustrations and '/educators/storybook/' in illustrations
assert all((ROOT/'assets'/'illustrations'/asset).is_file() for asset in ['courtroom-memory-defense.jpg','courtroom-blame-game.jpg','empty-binder-empty-promises.jpg','ai-incident-report-shredder.jpg','ai-safety-proof-problem.jpg','ai-safety-workflow-workshop.jpg','missing-ai-instructions-version.jpg','ai-safety-log-authority.jpg','ai-liability-incident-evidence.jpg'])
assert 'data-illustration-viewer' in illustrations and 'data-illustration-zoom-in' in illustrations
assert '/illustrations/' in (ROOT/'index.html').read_text().split('<nav id="navigation"',1)[1].split('</nav>',1)[0]
assert any(loc.endswith('/illustrations/') for loc in listed)
contact=(ROOT/'contact-us'/'index.html').read_text()
assert all(text in contact for text in ['AI governance assessment','Enterprise AI deployment','Technical demonstration'])
assert contact.count('https://calendar.app.google/WZfXQN1dpcvTcMGLA')==3
storybook=(ROOT/'educators'/'storybook'/'index.html').read_text()
assert 'window.location.replace' in storybook and 'docs.google.com/presentation/' in storybook
assert ("gtag('event','page_view'" in storybook)==SITE_PUBLIC
workflow=(ROOT/'assets/agentic-enterprise-workflow.html').read_text()
assert '<meta charset="utf-8">' in workflow
assert 'prefers-reduced-motion' in workflow
assert not any(claim in workflow for claim in ['UNDER 50MS','BIP-340','SCHNORR','RFC 8785','Zero Socket','NO UNMONITORED','Ed25519','policy_ver'])
assert (ROOT/'llms.txt').read_text().startswith('# SASKI Institute PBC')
assert not (ROOT/'CNAME').exists()
print(f'PASS: {len(pages)} HTML pages; internal links, assets, metadata, JSON-LD, labels, sitemap, and no domain change.')
