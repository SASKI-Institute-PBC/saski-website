import html
import json


TITLE = "AI help for Truckee businesses | SASKI Institute"
DESCRIPTION = (
    "Free 30 minute walkthrough for Truckee small businesses. AI assistants that "
    "handle busywork, designed so nothing happens without your approval."
)


def render(prefix, base, public, ga_id):
    canonical = base + "/truckee-locals/"
    social_image = base + "/assets/social-share.png"
    schema = json.dumps(
        {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Organization",
                    "@id": base + "/#organization",
                    "name": "SASKI Institute PBC",
                    "url": base + "/",
                    "logo": base + "/assets/institute-logo.png",
                },
                {
                    "@type": "WebPage",
                    "@id": canonical + "#webpage",
                    "name": TITLE,
                    "description": DESCRIPTION,
                    "url": canonical,
                    "about": {"@id": base + "/#organization"},
                },
            ],
        },
        ensure_ascii=False,
    )
    analytics = ""
    analytics_manage = ""
    if public and ga_id:
        analytics = (
            f'<script>window.SASKI_GA_ID={json.dumps(ga_id)};</script>'
            '<aside class="consent-banner" data-analytics-consent role="dialog" '
            'aria-labelledby="analytics-title" hidden><div><h2 id="analytics-title">'
            'Optional analytics</h2><p>We use Google Analytics to understand how people '
            'use this site. Analytics loads only if you accept.</p></div><div class="consent-actions">'
            '<button type="button" class="text-button" data-consent="declined">Decline</button>'
            '<button type="button" class="button" data-consent="granted">Accept analytics</button>'
            '</div></aside>'
        )
        analytics_manage = '<button type="button" class="footer-choice" data-manage-consent>Analytics choices</button>'
    robots = "index,follow" if public else "noindex,follow"
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{TITLE}</title><meta name="description" content="{html.escape(DESCRIPTION, quote=True)}"><link rel="canonical" href="{canonical}"><meta name="robots" content="{robots}"><meta property="og:type" content="website"><meta property="og:title" content="{TITLE}"><meta property="og:description" content="{html.escape(DESCRIPTION, quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:site_name" content="SASKI Institute"><meta property="og:locale" content="en_US"><meta property="og:image" content="{social_image}"><meta property="og:image:secure_url" content="{social_image}"><meta property="og:image:type" content="image/png"><meta property="og:image:width" content="1734"><meta property="og:image:height" content="907"><meta property="og:image:alt" content="SASKI Institute — AI understands. SASKI governs."><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{TITLE}"><meta name="twitter:description" content="{html.escape(DESCRIPTION, quote=True)}"><meta name="twitter:image" content="{social_image}"><meta name="twitter:image:alt" content="SASKI Institute — AI understands. SASKI governs."><meta name="theme-color" content="#1e3b32"><link rel="icon" type="image/png" href="{prefix}/assets/institute-logo.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&display=swap" rel="stylesheet"><link rel="stylesheet" href="{prefix}/assets/site.css"><link rel="stylesheet" href="{prefix}/assets/truckee.css"><script src="{prefix}/assets/site.js" defer></script><script src="{prefix}/assets/truckee.js" defer></script><script type="application/ld+json">{schema}</script></head><body class="truckee-page"><a class="skip" href="#main">Skip to content</a>
<header class="truckee-hero">
  <div class="truckee-wrap truckee-topbar"><a href="{prefix}/" aria-label="SASKI Institute home"><img src="{prefix}/assets/institute-logo-small.webp" alt="SASKI Institute" width="220" height="220"></a><span>FOR TRUCKEE LOCAL BUSINESSES</span></div>
  <div class="truckee-wrap truckee-hero-copy"><p class="truckee-kicker">Practical AI help, built around your business</p><h1>Spend less time<br>on busywork.</h1><p class="truckee-subhead">Let AI handle it, safely.</p><p class="truckee-intro">I help Truckee business owners set up useful AI assistants that save time while keeping you in control.</p><a class="truckee-button" href="#contact">Book a free 30 minute walkthrough</a></div>
  <svg class="truckee-ridge" viewBox="0 0 1440 150" preserveAspectRatio="none" aria-hidden="true"><path d="M0 112L118 79l82 25 132-69 107 55 113-35 105 47 128-76 119 69 108-46 118 55 110-39 100 55v80H0z" fill="#eaf1ed"/></svg>
</header>
<main id="main">
  <section class="truckee-section truckee-services"><div class="truckee-wrap"><p class="truckee-eyebrow">A GOOD PLACE TO START</p><h2>What I can set up for you</h2><p class="truckee-lead">Start with the repetitive work that steals time from customers, employees, and the work only you can do.</p><div class="truckee-cards">
    <article><span>01</span><h3>After-hours response</h3><p>Answer customer calls, texts, and emails after hours.</p></article>
    <article><span>02</span><h3>Appointments</h3><p>Book appointments and send reminders.</p></article>
    <article><span>03</span><h3>Follow-up</h3><p>Follow up on quotes and unpaid invoices.</p></article>
    <article><span>04</span><h3>Bookkeeping help</h3><p>Turn receipts into bookkeeping entries.</p></article>
    <article><span>05</span><h3>Stay current</h3><p>Keep your reviews and social posts current.</p></article>
    <article><span>06</span><h3>Your workflow</h3><p>Build around the way you already work.</p></article>
  </div></div></section>
  <section class="truckee-section truckee-safety"><div class="truckee-wrap truckee-safety-grid"><div><p class="truckee-eyebrow">YOU SET THE BOUNDARIES</p><h2>Built safe from day one</h2></div><p>Your assistant is designed so it can’t spend money, delete records, or contact customers in ways you haven’t approved. Every action is logged, so you can always see exactly what it did.</p></div></section>
  <section class="truckee-section truckee-process"><div class="truckee-wrap"><p class="truckee-eyebrow">SIMPLE AND PRACTICAL</p><h2>How it works</h2><ol>
    <li><span>1</span><div><h3>Free walkthrough</h3><p>We talk for 30 minutes about where your time goes.</p></div></li>
    <li><span>2</span><div><h3>I set it up</h3><p>I build the assistant around the tools you already use.</p></div></li>
    <li><span>3</span><div><h3>You stay in control</h3><p>You approve what it can do and can see everything it did.</p></div></li>
  </ol></div></section>
  <section class="truckee-section truckee-about"><div class="truckee-wrap truckee-about-grid"><div><p class="truckee-eyebrow">A TRUCKEE LOCAL</p><h2>Meet Stephen</h2></div><div><p class="truckee-lead">Stephen Calhoun is the founder of SASKI Institute PBC and a Truckee local with more than 40 years in technology.</p><p>He also founded the Truckee Neural Network, a LinkedIn group for local people working with and learning about AI.</p><a class="truckee-text-link" href="https://www.linkedin.com/in/steve-calhoun/" target="_blank" rel="noopener">Connect with Stephen on LinkedIn →</a></div></div></section>
  <section class="truckee-section truckee-contact" id="contact"><div class="truckee-wrap truckee-contact-grid"><div><p class="truckee-eyebrow">LET’S FIND THE TIME SAVERS</p><h2>Book your free 30 minute walkthrough</h2><p class="truckee-lead">No obligation. I’ll show you where AI can save you time.</p><div class="truckee-contact-links"><a href="tel:+17072874544">Call 707.287.4544</a><a href="mailto:info@saski.io">Email info@saski.io</a><a href="https://calendar.app.google/xDDyqy35d2zpwDTX7" target="_blank" rel="noopener">Pick a time on the calendar →</a></div></div>
  <form class="truckee-form" data-truckee-form><label for="truckee-name">Name</label><input id="truckee-name" name="name" autocomplete="name" required><label for="truckee-business">Business name</label><input id="truckee-business" name="business" autocomplete="organization" required><label for="truckee-phone">Phone</label><input id="truckee-phone" name="phone" type="tel" autocomplete="tel" required><label for="truckee-email">Email</label><input id="truckee-email" name="email" type="email" autocomplete="email" required><label for="truckee-challenge">What takes up too much of your time? <span>(optional)</span></label><textarea id="truckee-challenge" name="challenge" rows="4"></textarea><button class="truckee-button" type="submit">Request my walkthrough</button><p class="truckee-form-note">Submitting opens your email app with the details filled in.</p><p class="truckee-form-status" data-truckee-status aria-live="polite"></p></form></div></section>
</main>
<footer class="truckee-footer"><div class="truckee-wrap"><p><strong>SASKI Institute PBC</strong> · Truckee, California</p><p><a href="mailto:info@saski.io">info@saski.io</a> · <a href="tel:+17072874544">707.287.4544</a></p><p><a href="{prefix}/">Visit the main SASKI website →</a></p>{analytics_manage}</div></footer>{analytics}</body></html>'''
