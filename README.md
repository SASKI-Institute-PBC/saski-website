# SASKI Institute website

Static website for SASKI-Institute-PBC, built around SASKI Agentic, Estate, SDK, and Replay. Python 3 generates complete semantic HTML; the deployed site uses only HTML, CSS, and a small JavaScript file. There are no runtime dependencies, cookies, analytics, or form backend.

## Preview locally

```sh
SITE_URL=http://localhost:4173 python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

Open http://localhost:4173. Edit content and metadata in `scripts/build.py`, styling in `assets/site.css`, and the menu/calculator in `assets/site.js`. Rebuild and refresh to see changes.

## GitHub Pages staging

The default build targets `https://saski-institute-pbc.github.io/saski-website/`. It handles the repository subpath in links, assets, canonicals, structured data, and sitemap. Staging pages use `noindex,follow`; robots.txt allows crawling so crawlers can observe that directive. This does not make the staging site private.

The Pages workflow is manually triggered, so pushing or merging does not deploy. After the implementation is merged, select GitHub Actions as the repository's Pages source and run **Deploy Pages preview**. The separate validation workflow builds and checks pull requests and pushes. No CNAME file is included. Durable remains live and DNS is unchanged.

## Production, later

Only after the migration is approved, set the repository variables `SITE_URL=https://www.saski.io` and `SITE_INDEXABLE=true`, build and validate, and deploy using the configured custom domain. Confirm www versus apex canonical policy before cutover. Domain configuration and DNS are a separate explicit launch step, not part of this build.

## Architecture

| Route | Purpose |
| --- | --- |
| `/` | Agentic-led positioning and four-product overview |
| `/agentic/` | Governance of agent actions |
| `/estate/` | Governed smart-home control and troubleshooting for integrators |
| `/sdk/` | Human-facing interaction governance |
| `/replay/` | Historical policy evaluation and evidence |
| `/how-it-works/` | Independent enforcement architecture |
| `/findings/` | Condensed six-failure-class research article |
| `/resources/` | Findings, architecture, and Tokenator discovery |
| `/tokenator/` | Input-token overhead calculator |
| `/about/` | Institute and public-benefit purpose |
| `/contact-us/` | Demo scheduling using the existing booking URL |

Every page has a unique title/description, canonical, Open Graph and Twitter metadata, Organization JSON-LD, and appropriate page schema. Product pages add Product schema; Findings adds Article schema. No invented prices, ratings, review counts, or publication dates are included. Social image tags are deliberately omitted until an approved brand image is supplied.

## Migration scope

Do not migrate pricing, founder story, old privacy/terms, beta-program content, or the full legacy blog. The existing `/findings`, `/tokenator`, and `/contact-us` names are preserved (Pages serves directory URLs with trailing slashes). Retired content is not silently redirected to unrelated pages. Before production, decide which historical URLs merit a specific replacement or an intentional removal. GitHub Pages cannot configure arbitrary HTTP 301 rules; any required server-side redirect strategy must be resolved separately.

The demo CTA uses the booking URL linked from the existing contact page. The new website does not reproduce Durable's contact form. Findings is a condensed article, not a migration of all linked evaluation reports. Tokenator is a transparent repeated-prompt estimator, not a port of every legacy mode/tier assumption.

## Sources and editorial decisions

- User's September 23, 2026 build request and referenced conversation: **AI Visibility for SASKI**.
- User-supplied SASKI Public Website Content Inventory and SASKI Website Change Recommendations (July 20, 2026).
- Existing public Findings and Contact pages checked September 23, 2026.
- [GitHub Pages custom workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

Current Agentic-first direction takes precedence over earlier SDK-led homepage recommendations. Unsupported latency, savings percentages, compliance guarantees, FDA claims, customer/partner claims, and old pricing are omitted. The homepage action panel is explicitly labeled illustrative. No proprietary SDK/Agentic code or internal documents are included.

Estate content is adapted from the user-supplied **SASKI_Estates_Product_Sheet_v2.pdf**. The website uses the singular product name from its title, preserves the supported-system list and labeled lab example, and does not repeat legal-outcome guarantees. The original PDF is not republished.

The Institute, Agentic, and Estate logos are the supplied original PNG artwork. The Institute logo appears in the header/footer and Organization schema; product logos appear on the matching product pages and in Product schema. Team profiles will live on About once names, roles, biographies, and portraits are supplied. No placeholder people are published.
