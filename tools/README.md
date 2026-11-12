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
