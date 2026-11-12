#!/usr/bin/env python3
"""
Adds full IndiaFilings-style sections to service pages:
  overview + key benefits, what's included, documents required,
  4-step process, FAQs and related services.

Content lives in tools/service_content/*.py (one file per category). Each page
keeps its own hero, lead form, payment code, header and footer. The generated
block sits between <!--IWF:SVC--> markers, so this script is safe to re-run.

Usage (from the repo root):
    python3 tools/rebuild_services.py
"""
import html
import importlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(os.path.dirname(HERE), 'iwf-website')
SVC_DIR = os.path.join(ROOT, 'services')
sys.path.insert(0, HERE)

CATEGORY_FILES = ['startup', 'registrations', 'trademark', 'gst', 'income_tax', 'mca', 'compliance', 'consultation', 'global_']

e = html.escape

ICONS = [
    '<path d="M9 11l3 3 8-8M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
    '<path d="M12 2l8 4v6c0 5-3.5 9-8 10-4.5-1-8-5-8-10V6l8-4z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>',
    '<path d="M3 17l6-6 4 4 8-8M14 7h7v7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
    '<circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.6"/><path d="M12 6v6l4 2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
]

CSS = r'''<style><!--IWF:SVC-CSS-->
  section{position:relative;z-index:1}
  .section-head{max-width:780px;margin:0 auto 3rem;text-align:center}
  .sec-eyebrow{font-family:'Geist Mono',monospace;font-size:.78rem;color:var(--saffron-deep);text-transform:uppercase;letter-spacing:.15em;margin-bottom:1rem}
  .section-head h2{font-family:'Fraunces',serif;font-size:clamp(1.9rem,3.5vw,2.8rem);font-weight:400;letter-spacing:-.025em;line-height:1.1}
  .section-head h2 em{color:var(--saffron-deep);font-weight:500}
  .section-head p{margin-top:.9rem;color:var(--muted)}
  .what-is{padding:5rem 2rem;max-width:1180px;margin:0 auto}
  .what-grid{display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:start}
  .what-grid h2{font-family:'Fraunces',serif;font-size:clamp(1.7rem,3vw,2.4rem);font-weight:400;letter-spacing:-.02em;line-height:1.15;margin-bottom:1.2rem}
  .what-grid h2 em{color:var(--saffron-deep);font-weight:500}
  .what-grid p{color:var(--muted);margin-bottom:1rem;line-height:1.7}
  .what-grid p strong{color:var(--ink);font-weight:500}
  .highlights{list-style:none;display:grid;gap:1rem;margin:0;padding:0}
  .highlights li{display:flex;gap:1rem;padding:1.2rem;background:var(--card);border:1px solid var(--line);border-radius:14px}
  .hi-icon{width:40px;height:40px;border-radius:10px;background:var(--paper-warm);color:var(--saffron-deep);display:flex;align-items:center;justify-content:center;flex-shrink:0}
  .hi-text strong{display:block;font-weight:500;margin-bottom:.2rem}
  .hi-text span{color:var(--muted);font-size:.9rem;line-height:1.5}
  .incl{padding:5rem 2rem;background:linear-gradient(180deg,var(--paper-warm),var(--paper))}
  .incl-inner{max-width:1180px;margin:0 auto;display:grid;grid-template-columns:1.2fr 1fr;gap:2rem;align-items:start}
  .incl-card{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:2rem}
  .incl-card h3{font-family:'Fraunces',serif;font-weight:500;font-size:1.4rem;margin-bottom:1.2rem}
  .incl-list{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:.75rem 1.5rem;margin:0;padding:0}
  .incl-list li{display:flex;gap:.6rem;align-items:flex-start;font-size:.93rem;line-height:1.45}
  .incl-list li::before{content:'';width:18px;height:18px;border-radius:50%;flex-shrink:0;margin-top:1px;background:var(--saffron) url("data:image/svg+xml;utf8,<svg viewBox='0 0 16 16' xmlns='http://www.w3.org/2000/svg'><path d='M4 8L7 11L12 5' stroke='white' stroke-width='2' fill='none' stroke-linecap='round'/></svg>") center/14px no-repeat}
  .quote-card{background:linear-gradient(135deg,var(--indigo-deep),var(--indigo));color:var(--paper);border-radius:18px;padding:2rem;position:relative;overflow:hidden}
  .quote-card .tag{font-family:'Geist Mono',monospace;font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;color:var(--saffron);margin-bottom:.8rem}
  .quote-card h3{font-family:'Fraunces',serif;font-weight:500;font-size:1.6rem;line-height:1.2;margin-bottom:.8rem}
  .quote-card p{color:rgba(250,246,239,.75);font-size:.92rem;line-height:1.6;margin-bottom:1.2rem}
  .quote-card .gov{border-top:1px dashed rgba(250,246,239,.25);padding-top:1rem;margin-top:1rem;font-size:.85rem;color:rgba(250,246,239,.7)}
  .quote-card .gov strong{color:var(--paper);font-weight:500}
  .quote-card a.qbtn{display:inline-flex;padding:.8rem 1.4rem;border-radius:100px;background:var(--saffron);color:#fff;text-decoration:none;font-weight:500;font-size:.92rem}
  .quote-card a.qbtn:hover{background:var(--saffron-deep)}
  .docs{padding:5rem 2rem;max-width:1180px;margin:0 auto}
  .docs-grid{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem}
  .docs-grid.one{grid-template-columns:1fr;max-width:760px;margin:0 auto}
  .doc-block{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:1.8rem}
  .doc-block h3{font-family:'Fraunces',serif;font-weight:500;font-size:1.25rem;margin-bottom:.2rem}
  .doc-sub{font-family:'Geist Mono',monospace;font-size:.72rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-bottom:1.2rem}
  .doc-list{list-style:none;display:grid;gap:.9rem;margin:0;padding:0}
  .doc-list li{display:flex;gap:.8rem;padding-bottom:.9rem;border-bottom:1px dashed var(--line)}
  .doc-list li:last-child{border-bottom:0;padding-bottom:0}
  .doc-list li::before{content:'';width:8px;height:8px;border-radius:50%;background:var(--saffron);margin-top:.5rem;flex-shrink:0}
  .doc-list strong{display:block;font-weight:500;font-size:.95rem}
  .doc-list span{color:var(--muted);font-size:.86rem}
  .process{padding:5rem 2rem;background:var(--indigo-deep);color:var(--paper)}
  .process-inner{max-width:1180px;margin:0 auto}
  .process .section-head h2{color:var(--paper)}
  .process .section-head p{color:rgba(250,246,239,.65)}
  .timeline{display:grid;grid-template-columns:repeat(4,1fr);gap:0}
  .step{padding:0 1.5rem;border-left:1px solid rgba(250,246,239,.15)}
  .step:first-child{border-left:0;padding-left:0}
  .step .num{font-family:'Fraunces',serif;font-size:2.4rem;color:var(--saffron);line-height:1;margin-bottom:1rem}
  .step h4{font-family:'Fraunces',serif;font-weight:500;font-size:1.15rem;margin-bottom:.5rem}
  .step p{color:rgba(250,246,239,.7);font-size:.9rem;line-height:1.55}
  .faq{padding:5rem 2rem;max-width:880px;margin:0 auto}
  .faq-item{border-bottom:1px solid var(--line)}
  .faq-q{padding:1.3rem 0;display:flex;justify-content:space-between;align-items:center;cursor:pointer;font-family:'Fraunces',serif;font-size:1.15rem;font-weight:500;letter-spacing:-.01em}
  .faq-q::after{content:'+';font-family:'Fraunces',serif;font-size:1.6rem;color:var(--saffron-deep);transition:transform .25s;flex-shrink:0;margin-left:1rem}
  .faq-item.open .faq-q::after{transform:rotate(45deg)}
  .faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease}
  .faq-item.open .faq-a{max-height:600px}
  .faq-a p{padding-bottom:1.3rem;color:var(--muted);line-height:1.7}
  .related{padding:0 2rem 5rem;max-width:1180px;margin:0 auto}
  .rel-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}
  .rel-card{display:block;padding:1.4rem;background:var(--card);border:1px solid var(--line);border-radius:14px;color:var(--ink);text-decoration:none;transition:border-color .2s,transform .2s}
  .rel-card:hover{border-color:var(--saffron);transform:translateY(-2px)}
  .rel-card small{font-family:'Geist Mono',monospace;font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;color:var(--saffron-deep)}
  .rel-card strong{display:block;font-family:'Fraunces',serif;font-weight:500;font-size:1.1rem;margin:.35rem 0 .3rem}
  .rel-card span{color:var(--muted);font-size:.86rem}
  @media(max-width:900px){.what-grid,.docs-grid,.incl-inner{grid-template-columns:1fr;gap:2rem}.timeline{grid-template-columns:1fr 1fr;gap:2rem}.step{border-left:none;padding:0}.rel-grid{grid-template-columns:1fr 1fr}}
  @media(max-width:560px){.timeline,.rel-grid,.incl-list{grid-template-columns:1fr}.what-is,.docs,.faq,.incl,.process{padding:3.5rem 1.2rem}.related{padding:0 1.2rem 3.5rem}}
</style>'''

FAQ_JS = '''<script><!--IWF:SVC-JS-->
document.querySelectorAll('.faq-item').forEach(function(i){var q=i.querySelector('.faq-q');if(q&&!q.dataset.bound){q.dataset.bound='1';q.addEventListener('click',function(){i.classList.toggle('open')})}});
</script>'''


def em(text):
    """*word* becomes <em>word</em>; everything else is escaped."""
    return re.sub(r'\*(.+?)\*', r'<em>\1</em>', e(text))


def rich(text):
    """Escape, then allow **bold**."""
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', e(text))


def load_content():
    data = {}
    for name in CATEGORY_FILES:
        mod = importlib.import_module(f'service_content.{name}')
        for slug, d in mod.SERVICES.items():
            if slug in data:
                raise ValueError(f'duplicate content for {slug}')
            data[slug] = d
    return data


def title_of(slug):
    path = os.path.join(SVC_DIR, slug + '.html')
    if not os.path.exists(path):
        return slug.replace('-', ' ').title()
    t = open(path, encoding='utf-8').read()
    m = re.search(r'<h1>(.*?)<em>', t, re.S)
    return html.unescape(re.sub('<[^>]+>', '', m.group(1))).strip() if m else slug


def build_block(slug, name, d, titles):
    hl = ''.join(
        f'<li><div class="hi-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none">{ICONS[i % 4]}</svg></div>'
        f'<div class="hi-text"><strong>{e(t)}</strong><span>{e(x)}</span></div></li>'
        for i, (t, x) in enumerate(d['b']))
    paras = ''.join(f'<p>{rich(p)}</p>' for p in d['p'])
    what = f'''<section class="what-is">
  <div class="what-grid">
    <div>
      <div class="sec-eyebrow">— About {e(name)} —</div>
      <h2>{em(d["h"])}</h2>
      {paras}
    </div>
    <ul class="highlights">{hl}</ul>
  </div>
</section>'''

    inc = ''.join(f'<li>{e(x)}</li>' for x in d['inc'])
    gov = f'<div class="gov"><strong>Government fees:</strong> {e(d["g"])}</div>' if d.get('g') else ''
    incl = f'''<section class="incl" id="pricing">
  <div class="section-head">
    <div class="sec-eyebrow">— What's included —</div>
    <h2>Everything we handle for <em>{e(name)}</em>.</h2>
    <p>One professional handles your work from start to finish, with updates on WhatsApp.</p>
  </div>
  <div class="incl-inner">
    <div class="incl-card"><h3>Our service covers</h3><ul class="incl-list">{inc}</ul></div>
    <div class="quote-card">
      <div class="tag">Pricing</div>
      <h3>Get an exact quote in your inbox.</h3>
      <p>Fees depend on your entity type, state and how complex the work is. Share a few details and we will send a fixed price, the document checklist and a timeline before you pay anything.</p>
      <a href="#start" class="qbtn">Get my quote →</a>
      {gov}
    </div>
  </div>
</section>'''

    blocks = d['d'] if isinstance(d['d'][0], dict) else [{'t': f'Documents for {name}', 'sub': 'Typical checklist', 'items': d['d']}]
    docs_html = ''.join(
        f'<div class="doc-block"><h3>{e(b["t"])}</h3><div class="doc-sub">{e(b.get("sub", ""))}</div><ul class="doc-list">' +
        ''.join(f'<li><div><strong>{e(a)}</strong><span>{e(c)}</span></div></li>' for a, c in b['items']) + '</ul></div>'
        for b in blocks)
    docs = f'''<section class="docs">
  <div class="section-head">
    <div class="sec-eyebrow">— What you'll need —</div>
    <h2>Documents <em>required</em>.</h2>
    <p>{e(d.get("dn", "The exact list depends on your situation. We send a personalised checklist after the first call."))}</p>
  </div>
  <div class="docs-grid{"" if len(blocks) > 1 else " one"}">{docs_html}</div>
</section>'''

    steps = ''.join(f'<div class="step"><div class="num">{i + 1:02d}</div><h4>{e(t)}</h4><p>{e(x)}</p></div>' for i, (t, x) in enumerate(d['s']))
    process = f'''<section class="process">
  <div class="process-inner">
    <div class="section-head">
      <div class="sec-eyebrow">— The process —</div>
      <h2>How it works, in <em>{len(d["s"])} steps</em>.</h2>
      <p>{e(d.get("tl", "Timelines depend on the authority and on how quickly documents are shared. We confirm yours upfront."))}</p>
    </div>
    <div class="timeline">{steps}</div>
  </div>
</section>'''

    faqs = ''.join(f'<div class="faq-item"><div class="faq-q">{e(q)}</div><div class="faq-a"><p>{rich(a)}</p></div></div>' for q, a in d['f'])
    faq = f'''<section class="faq">
  <div class="section-head">
    <div class="sec-eyebrow">— FAQ —</div>
    <h2>Questions people <em>ask us</em>.</h2>
  </div>
  {faqs}
</section>'''

    rel = ''
    if d.get('r'):
        cards = ''.join(
            f'<a class="rel-card" href="/services/{r}.html"><small>Related</small><strong>{e(titles.get(r, r))}</strong><span>Learn more →</span></a>'
            for r in d['r'])
        rel = f'''<section class="related">
  <div class="section-head" style="margin-bottom:2rem">
    <div class="sec-eyebrow">— You may also need —</div>
    <h2>Related <em>services</em>.</h2>
  </div>
  <div class="rel-grid">{cards}</div>
</section>'''
    return what, incl, docs + process + faq + rel


def apply(slug, d, titles):
    path = os.path.join(SVC_DIR, slug + '.html')
    t = open(path, encoding='utf-8').read()
    name = title_of(slug)
    what, incl, rest = build_block(slug, name, d, titles)

    # remove a previous run
    t = re.sub(r'<!--IWF:SVC-A-->.*?<!--/IWF:SVC-A-->\n?', '', t, flags=re.S)
    t = re.sub(r'<!--IWF:SVC-B-->.*?<!--/IWF:SVC-B-->\n?', '', t, flags=re.S)

    # A: after the hero, before the "why" section
    hero_end = t.index('</section>', t.index('<section class="hero"')) + len('</section>')
    t = t[:hero_end] + '\n<!--IWF:SVC-A-->\n' + what + '\n' + incl + '\n<!--/IWF:SVC-A-->' + t[hero_end:]
    # B: after the "why" section, before the CTA strip
    cta = t.index('<section class="cta-strip">')
    t = t[:cta] + '<!--IWF:SVC-B-->\n' + rest + '\n<!--/IWF:SVC-B-->\n' + t[cta:]

    # drop an unverified claim from the old template
    t = re.sub(r"We&apos;ve handled thousands of compliance filings across [^.<]*\. ", '', t)

    if '<!--IWF:SVC-CSS-->' not in t:
        t = t.replace('<link rel="stylesheet" href="/assets/site.css"><!--IWF:CSS-->', CSS + '\n<link rel="stylesheet" href="/assets/site.css"><!--IWF:CSS-->', 1)
    if '<!--IWF:SVC-JS-->' not in t:
        idx = t.rfind('<script src="/assets/site.js">')
        t = t[:idx] + FAQ_JS + '\n' + t[idx:]
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(t)


def main():
    data = load_content()
    titles = {f[:-5]: title_of(f[:-5]) for f in os.listdir(SVC_DIR) if f.endswith('.html') and f != 'index.html'}
    import build_site  # menu labels are the cleanest service names
    for m in build_site.MENUS:
        for _, items in m['cols']:
            for label, href, _ in items:
                s = href.rsplit('/', 1)[-1][:-5]
                if s in titles and '/' not in label:
                    titles.setdefault('_menu_' + s, label)
    for k in [k for k in titles if k.startswith('_menu_')]:
        titles[k[6:]] = titles.pop(k)
    missing_rel = [(s, r) for s, d in data.items() for r in d.get('r', []) if r not in titles]
    if missing_rel:
        raise ValueError(f'related links to missing pages: {missing_rel}')
    done = 0
    for slug, d in sorted(data.items()):
        page = os.path.join(SVC_DIR, slug + '.html')
        if not os.path.exists(page):
            print('skip (no page):', slug)
            continue
        txt = open(page, encoding='utf-8').read()
        if 'class="what-is"' in txt and '<!--IWF:SVC-A-->' not in txt:
            print('skip (already a full page):', slug)
            continue
        apply(slug, d, titles)
        done += 1
    print(f'rebuilt {done} service pages')


if __name__ == '__main__':
    main()
