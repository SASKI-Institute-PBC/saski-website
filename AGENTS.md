# Local preview procedure

After changes to the static site, always run the production-equivalent build
and checks before previewing:

```bash
SITE_URL=https://www.saski.io SITE_INDEXABLE=true python3 scripts/build.py
python3 scripts/check.py
node --check assets/site.js
```

For visual QA in the ChatGPT desktop app, start the built files with this
exact command and keep its process running for the duration of the review:

```bash
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

Then open `http://localhost:4173/` in the app's built-in browser and inspect
the page being changed. Do not substitute a public deployment for local
preview. If the sandbox denies binding, request the local binding permission;
do not claim visual QA passed until the browser loads the page.
