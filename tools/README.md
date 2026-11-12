# Site builder

`python3 tools/build_site.py` (run from the repo root) puts the shared header, mega-menu,
mobile menu and footer on every page, and regenerates the content pages
(about, contact, careers, refer, partners, founder's guide, compliance calendar,
business search, learning center, legal pages, /services/ directory).

- Menus and footer links: edit `MENUS` / `FOOTER_COLS` in `build_site.py`
- Contact details, legal name, referral reward: edit `SITE` in `build_site.py`
- Page copy and guides: edit `content.py`
- Compliance due-date rules: edit `RULES` in `iwf-website/assets/calendar.js`

Safe to re-run any time. Service pages keep their own content; only the header
and footer between the `<!--IWF:HEADER-->` / `<!--IWF:FOOTER-->` markers are replaced.

## Service page content

`python3 tools/rebuild_services.py` adds the full sections (overview, what's included,
documents, process, FAQs, related services) to service pages. Content lives in
`tools/service_content/<category>.py`, one entry per page. Edit the text there and re-run.
Pages keep their own hero, lead form and payment code. Safe to re-run.
