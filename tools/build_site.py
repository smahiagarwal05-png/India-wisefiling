#!/usr/bin/env python3
"""
IndiaWiseFilings site builder.

What it does (safe to run any number of times):
  1. Puts the same full header (top bar + mega-menu + mobile drawer) and the same
     full footer on EVERY page: the homepage, all /services/*.html pages and the
     content pages generated below.
  2. Generates the content pages (about, contact, legal, learning center, etc.)
     from tools/content.py.
  3. Generates /services/index.html, the "all services" directory, from the menu.

Usage (from the repo root):
    python3 tools/build_site.py

To add or rename a menu item, edit MENUS below and re-run. To change contact
details, edit SITE below and re-run.
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(os.path.dirname(HERE), 'iwf-website')
sys.path.insert(0, HERE)

# ----------------------------------------------------------------------------
# Site-wide settings. Anything marked TODO is a placeholder you should replace.
# ----------------------------------------------------------------------------
SITE = {
    'brand': 'IndiaWiseFilings',
    'legal_name': 'IndiaWiseFilings Technologies Pvt. Ltd.',
    'domain': 'indiawisefilings.com',
    'whatsapp': '919319179754',
    'whatsapp_label': '+91 93191 79754',
    'email': 'support@indiawisefilings.com',          # TODO confirm this mailbox exists
    'address': 'Registered office address (TODO)',      # TODO add registered office address
    'cin': 'CIN (TODO)',                                # TODO add CIN once incorporated
    'grievance_officer': 'Grievance Officer name (TODO)',  # TODO name a grievance officer
    'hours': 'Mon to Sat, 9:30 am to 7:00 pm IST',
    'refer_reward': '₹500',                            # TODO set your referral reward
    'year': '2026',
}

ARROW = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>'
CARET = '<svg width="10" height="10" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>'

S = '/services/'
# Each item: (label, href, badge) where badge is None, 'Popular' or 'New'.
MENUS = [
    {'label': 'Startup', 'slug': 'startup', 'blurb': '40+ startup registration services', 'cols': [
        ('Company Types', [('Private Limited Company', S + 'private-limited-company.html', 'Popular'), ('Limited Liability Partnership', S + 'limited-liability-partnership.html', None), ('One Person Company', S + 'one-person-company.html', None), ('Partnership Firm', S + 'partnership-firm.html', None), ('Sole Proprietorship', S + 'sole-proprietorship.html', None), ('Nidhi Company', S + 'nidhi-company.html', None), ('Producer Company', S + 'producer-company.html', None)]),
        ('Special Entities', [('Section 8 Company', S + 'section-8-company.html', None), ('Indian Subsidiary', S + 'indian-subsidiary.html', None), ('Foreign Subsidiary', S + 'foreign-subsidiary.html', None), ('Public Limited Company', S + 'public-limited-company.html', None), ('Trust Registration', S + 'trust-registration.html', None), ('Society Registration', S + 'society-registration.html', None)]),
        ('Post-Registration', [('DIN Application', S + 'din-application.html', None), ('DSC for Directors', S + 'dsc-for-directors.html', None), ('Commencement of Business', S + 'commencement-of-business.html', None), ('Add Director', S + 'add-director.html', None), ('Remove Director', S + 'remove-director.html', None), ('Change Registered Office', S + 'change-registered-office.html', None), ('Increase Capital', S + 'increase-capital.html', None)]),
     ], 'promo': ('Featured', 'Pvt Ltd at ₹7,999', 'Name approval, DSC, DIN, incorporation certificate, PAN and TAN.', 'Start incorporation', S + 'private-limited-company.html')},
    {'label': 'Registrations', 'slug': 'registrations', 'blurb': '28 registration services available', 'cols': [
        ('Business Licenses', [('Startup India', S + 'startup-india.html', None), ('Trade License', S + 'trade-license.html', None), ('FSSAI Registration', S + 'fssai-registration.html', 'Popular'), ('FSSAI License', S + 'fssai-license.html', None), ('Halal Certification', S + 'halal-certification.html', None), ('ICEGATE Registration', S + 'icegate-registration.html', None), ('Import Export Code', S + 'import-export-code.html', None)]),
        ('Statutory', [('Legal Entity Identifier', S + 'legal-entity-identifier.html', None), ('ISO Registration', S + 'iso-registration.html', None), ('PF Registration', S + 'pf-registration.html', None), ('ESI Registration', S + 'esi-registration.html', None), ('Professional Tax', S + 'professional-tax.html', None), ('RCMC Registration', S + 'rcmc-registration.html', None), ('TN RERA Agents', S + 'tn-rera-agents.html', None)]),
        ('NGO & Tax Exempt', [('12A and 80G Registration', S + '12a-and-80g-registration.html', None), ('12A Registration', S + '12a-registration.html', None), ('80G Registration', S + '80g-registration.html', None), ('Darpan Registration', S + 'darpan-registration.html', None), ('Certificate of Incumbency', S + 'certificate-of-incumbency.html', None), ('Barcode Registration', S + 'barcode-registration.html', None), ('BIS Registration', S + 'bis-registration.html', None)]),
        ('Other Services', [('Digital Signature', S + 'digital-signature.html', 'Popular'), ('Shop Act Registration', S + 'shop-act-registration.html', None), ('Udyam Registration', S + 'udyam-registration.html', 'Popular'), ('Fire License', S + 'fire-license.html', None), ('Legal Name Change', S + 'legal-name-change.html', None), ('Water Testing', S + 'water-testing.html', None), ('Food Testing', S + 'food-testing.html', None)]),
     ], 'promo': None},
    {'label': 'Trademark', 'slug': 'trademark', 'blurb': 'Protect your brand in India and abroad', 'cols': [
        ('Trademark', [('Trademark Search', S + 'trademark-search.html', 'Popular'), ('Trademark Registration', S + 'trademark-registration.html', None), ('Trademark Objection', S + 'trademark-objection.html', None), ('Trademark Opposition', S + 'trademark-opposition.html', None), ('Trademark Renewal', S + 'trademark-renewal.html', None), ('Trademark Assignment', S + 'trademark-assignment.html', None), ('Trademark Rectification', S + 'trademark-rectification.html', None)]),
        ('International', [('USA Trademark', S + 'usa-trademark.html', None), ('UK Trademark', S + 'uk-trademark.html', None), ('EU Trademark', S + 'eu-trademark.html', None), ('UAE Trademark', S + 'uae-trademark.html', None), ('International Trademark', S + 'international-trademark.html', None), ('Madrid Protocol Filing', S + 'madrid-protocol-filing.html', None)]),
        ('Copyright & Patent', [('Copyright Registration', S + 'copyright-registration.html', None), ('Copyright Objection', S + 'copyright-objection.html', None), ('Patent Registration', S + 'patent-registration.html', None), ('Patent Search', S + 'patent-search.html', None), ('Design Registration', S + 'design-registration.html', None), ('Geographical Indication', S + 'geographical-indication.html', None)]),
     ], 'promo': ('Free tool', 'Free Trademark Search', 'Check if your brand name is already taken before you file.', 'Run free search', S + 'trademark-search.html')},
    {'label': 'GST', 'slug': 'gst', 'blurb': 'Monthly and quarterly GST filing', 'cols': [
        ('GST Registration', [('New GST Registration', S + 'gst-registration.html', 'Popular'), ('GST Amendment', S + 'gst-amendment.html', None), ('GST Cancellation', S + 'gst-cancellation.html', None), ('GST Revocation', S + 'gst-revocation.html', None), ('Composition Scheme', S + 'composition-scheme.html', None), ('Casual Taxable Person', S + 'casual-taxable-person.html', None)]),
        ('GST Returns', [('GSTR-1 Filing', S + 'gstr-1-filing.html', None), ('GSTR-3B Filing', S + 'gstr-3b-filing.html', None), ('GSTR-9 Annual Return', S + 'gstr-9-annual-return.html', None), ('GSTR-9C Audit', S + 'gstr-9c-audit.html', None), ('Nil Return Filing', S + 'nil-return-filing.html', None), ('Composition Return', S + 'composition-return.html', None)]),
        ('GST Refunds & Notice', [('GST Refund', S + 'gst-refund.html', None), ('LUT for Exports', S + 'lut-for-exports.html', None), ('E-Invoicing', S + 'e-invoicing.html', None), ('E-Way Bill', S + 'e-way-bill.html', None), ('GST Notice Reply', S + 'gst-notice-reply.html', None), ('GST Appeal', S + 'gst-appeal.html', None)]),
     ], 'promo': ('Featured', 'GST Filing at ₹999/mo', 'GSTR-1 and GSTR-3B prepared, reconciled and filed every month.', 'Start GST plan', S + 'gstr-3b-filing.html')},
    {'label': 'Income Tax', 'slug': 'income-tax', 'blurb': 'Individual and business tax filing', 'cols': [
        ('ITR Filing', [('Salaried Individuals', S + 'itr-salaried.html', 'Popular'), ('Freelancer ITR', S + 'itr-freelancer.html', None), ('Business ITR', S + 'itr-business.html', None), ('NRI Tax Filing', S + 'itr-nri.html', None), ('Capital Gains Filing', S + 'itr-capital-gains.html', None), ('Crypto Tax Filing', S + 'itr-crypto.html', 'New')]),
        ('TDS & Advance Tax', [('TDS Return Filing', S + 'tds-return-filing.html', None), ('TDS on Property', S + 'tds-on-property.html', None), ('TCS Filing', S + 'tcs-filing.html', None), ('Form 15CA/CB', S + 'form-15ca-cb.html', None), ('Advance Tax Calculation', S + 'advance-tax-calculation.html', None), ('Form 16 Generation', S + 'form-16-generation.html', None)]),
        ('Notices & Audit', [('Income Tax Notice Reply', S + 'income-tax-notice-reply.html', None), ('Tax Audit', S + 'tax-audit.html', None), ('Transfer Pricing Audit', S + 'transfer-pricing-audit.html', None), ('Tax Refund Status', S + 'tax-refund-status.html', None), ('PAN Application', S + 'pan-application.html', None), ('TAN Application', S + 'tan-application.html', None)]),
     ], 'promo': ('Featured', 'ITR Filing from ₹999', 'CA-reviewed return with every deduction you are eligible for.', 'File your ITR', S + 'itr-salaried.html')},
    {'label': 'MCA', 'slug': 'mca', 'blurb': 'Never miss an ROC deadline', 'cols': [
        ('Annual Compliance', [('ROC Annual Filing', S + 'roc-annual-filing.html', 'Popular'), ('LLP Annual Filing', S + 'llp-annual-filing.html', None), ('Director KYC', S + 'director-kyc.html', None), ('DPT-3 Filing', S + 'dpt-3-filing.html', None), ('MSME Form 1', S + 'msme-form-1.html', None), ('Board Meeting Minutes', S + 'board-meeting-minutes.html', None)]),
        ('Company Changes', [('Company Name Change', S + 'company-name-change.html', None), ('Change of Object', S + 'change-of-object.html', None), ('Add / Remove Director', S + 'add-director.html', None), ('Share Transfer', S + 'share-transfer.html', None), ('Increase Authorized Capital', S + 'increase-authorized-capital.html', None), ('Conversion of Company', S + 'conversion-of-company.html', None)]),
        ('Winding Up', [('Company Strike Off', S + 'company-strike-off.html', None), ('LLP Closure', S + 'llp-closure.html', None), ('DIN Reactivation', S + 'din-reactivation.html', None), ('CCFS Scheme', S + 'ccfs-scheme.html', None), ('Dormant Company Status', S + 'dormant-company-status.html', None), ('Revival of Company', S + 'revival-of-company.html', None)]),
     ], 'promo': ('Featured', 'Annual ROC at ₹9,999', 'AOC-4, MGT-7, ADT-1, DIR-3 KYC and board minutes, on time.', 'Get ROC plan', S + 'roc-annual-filing.html')},
    {'label': 'Compliance', 'slug': 'compliance', 'blurb': 'Accounting, audit and payroll, handled for you', 'cols': [
        ('Bookkeeping', [('Accounting Services', S + 'accounting-services.html', 'Popular'), ('Bookkeeping Outsourcing', S + 'bookkeeping-outsourcing.html', None), ('Financial Statements', S + 'financial-statements.html', None), ('MIS Reports', S + 'mis-reports.html', None), ('Virtual CFO Service', S + 'virtual-cfo-service.html', None)]),
        ('Audit & Review', [('Internal Audit', S + 'internal-audit.html', None), ('Statutory Audit', S + 'statutory-audit.html', None), ('GST Audit', S + 'gst-audit.html', None), ('Stock Audit', S + 'stock-audit.html', None), ('Due Diligence', S + 'due-diligence.html', None), ('Forensic Audit', S + 'forensic-audit.html', None)]),
        ('HR & Payroll', [('HR & Payroll Service', S + 'hr-payroll-service.html', 'Popular'), ('Payroll Management', S + 'payroll-management.html', None), ('PF Registration', S + 'pf-registration.html', None), ('ESI Registration', S + 'esi-registration.html', None), ('Professional Tax', S + 'professional-tax.html', None), ('Form 16 Generation', S + 'form-16-generation.html', None)]),
     ], 'promo': ('Featured', 'Payroll, PF and ESI in one plan', 'Salary processing, payslips, PF/ESI challans and TDS on salary every month.', 'Set up payroll', S + 'hr-payroll-service.html')},
    {'label': 'Consultation', 'slug': 'consultation', 'blurb': 'Talk to a CA, CS or lawyer', 'cols': [
        ('Expert Advice', [('CA Consultation', S + 'ca-consultation.html', 'Popular'), ('CS Consultation', S + 'cs-consultation.html', None), ('Lawyer Consultation', S + 'lawyer-consultation.html', None), ('Cross-Border Tax Advice', S + 'cross-border-tax.html', None), ('Virtual CFO Service', S + 'virtual-cfo-service.html', None)]),
        ('Legal Drafting', [('Founders Agreement', S + 'founders-agreement.html', None), ('Shareholders Agreement', S + 'shareholders-agreement.html', None), ('Employment Agreement', S + 'employment-agreement.html', None), ('NDA Drafting', S + 'nda-drafting.html', None), ('Vendor Agreement', S + 'vendor-agreement.html', None), ('Rental Agreement', S + 'rental-agreement.html', None)]),
        ('Business Support', [('Virtual Office', S + 'virtual-office.html', None), ('Notary Service', S + 'notary-service.html', None), ("Founder's Guide", '/founders-guide.html', 'New'), ('Learning Center', '/learn/', None), ('Business Search', '/business-search.html', 'New'), ('Compliance Calendar', '/compliance-calendar.html', 'New')]),
     ], 'promo': ('Talk to an expert', 'Book a CA consultation', 'Get a straight answer on tax, GST or company law from a qualified professional.', 'Book a call', S + 'ca-consultation.html')},
    {'label': 'Global', 'slug': 'global', 'blurb': 'Expand your business worldwide', 'cols': [
        ('🇦🇪 UAE', [('UAE Company Registration', S + 'uae-company-registration.html', 'Popular'), ('UAE Free Zone Setup', S + 'uae-free-zone-setup.html', None), ('UAE Mainland Setup', S + 'uae-mainland-setup.html', None), ('Ajman Free Zone', S + 'ajman-free-zone.html', None), ('UAE eCommerce License', S + 'uae-ecommerce-license.html', None), ('UAE Attestation MOFA', S + 'uae-attestation-mofa.html', None)]),
        ('🇺🇸 USA', [('USA Business Setup', S + 'usa-business-setup.html', None), ('Delaware Incorporation', S + 'delaware-incorporation.html', None), ('Wyoming LLC', S + 'wyoming-llc.html', None), ('USA Trademark', S + 'usa-trademark.html', None), ('EIN Application', S + 'ein-application.html', None), ('USA Tax Filing', S + 'usa-tax-filing.html', None)]),
        ('🇬🇧 UK & 🇸🇬 Singapore', [('UK Company Registration', S + 'uk-company-registration.html', None), ('Singapore Incorporation', S + 'singapore-incorporation.html', None), ('UK VAT Registration', S + 'uk-vat-registration.html', None), ('Singapore GST', S + 'singapore-gst.html', None), ('International Trademark', S + 'international-trademark.html', None), ('Cross-Border Tax', S + 'cross-border-tax.html', None)]),
     ], 'promo': ('Featured', 'UAE Company in 7 days', 'Free Zone setup from AED 5,500. Trade license, visa and bank account support.', 'Start UAE setup', S + 'uae-company-registration.html')},
]

FOOTER_COLS = [
    ('Company', [('About us', '/about.html'), ('Contact us', '/contact.html'), ('Careers', '/careers.html'), ('Refer & Earn', '/refer.html'), ('CA / CS partner network', '/partners.html')]),
    ('Resources', [('Learning Center', '/learn/'), ("Founder's Guide", '/founders-guide.html'), ('Business Search', '/business-search.html'), ('Compliance Calendar', '/compliance-calendar.html'), ('All services', '/services/')]),
    ('Popular', [('Pvt Ltd Registration', S + 'private-limited-company.html'), ('GST Registration', S + 'gst-registration.html'), ('Income Tax Filing', S + 'itr-salaried.html'), ('Trademark Registration', S + 'trademark-registration.html'), ('ROC Annual Filing', S + 'roc-annual-filing.html'), ('UAE Company Setup', S + 'uae-company-registration.html')]),
    ('Legal', [('Terms & Conditions', '/legal/terms.html'), ('Privacy Policy', '/legal/privacy.html'), ('Refund Policy', '/legal/refund.html'), ('Confidentiality Policy', '/legal/confidentiality.html'), ('Disclaimer', '/legal/disclaimer.html')]),
]

e = html.escape


def badge(b):
    if not b:
        return ''
    return f' <span class="iwf-tag{" iwf-tag-new" if b == "New" else ""}">{e(b)}</span>'


def logo(cls='iwf-logo'):
    return f'<a href="/" class="{cls}" aria-label="{e(SITE["brand"])} home"><span class="iwf-logo-mark"></span><span>IndiaWise<em>Filings</em></span></a>'


def header_html():
    lis = []
    for m in MENUS:
        cols = ''.join(
            f'<div class="iwf-col"><h6>{e(t)}</h6><ul>' +
            ''.join(f'<li><a href="{h}">{e(l)}{badge(b)}</a></li>' for l, h, b in items) +
            '</ul></div>' for t, items in m['cols'])
        promo = ''
        if m['promo']:
            tag, title, text, link, href = m['promo']
            promo = (f'<div class="iwf-promo"><div class="iwf-promo-tag">{e(tag)}</div><strong>{e(title)}</strong>'
                     f'<p>{e(text)}</p><a href="{href}">{e(link)} →</a></div>')
        lis.append(
            f'<li class="iwf-has-mega"><button class="iwf-trigger" type="button" aria-expanded="false">{e(m["label"])} {CARET}</button>'
            f'<div class="iwf-mega"><div class="iwf-mega-inner">{cols}{promo}</div>'
            f'<div class="iwf-mega-foot"><span>— {e(m["blurb"])}</span><a href="/services/#{m["slug"]}">View all {e(m["label"])} services {ARROW}</a></div></div></li>')
    drawer_menus = ''.join(
        f'<details><summary>{e(m["label"])}</summary>' +
        ''.join(f'<h6>{e(t)}</h6><ul>' + ''.join(f'<li><a href="{h}">{e(l)}</a></li>' for l, h, b in items) + '</ul>' for t, items in m['cols']) +
        f'<ul><li><a href="/services/#{m["slug"]}"><strong>View all {e(m["label"])} services →</strong></a></li></ul></details>'
        for m in MENUS)
    wa = f'https://wa.me/{SITE["whatsapp"]}'
    search_items = []
    seen = set()
    for m in MENUS:
        for t_, items in m['cols']:
            for l, h, b in items:
                if h not in seen:
                    seen.add(h); search_items.append([l, h, m['label']])
    for l, h in [('Learning Center', '/learn/'), ("Founder's Guide", '/founders-guide.html'), ('Business Search', '/business-search.html'), ('Compliance Calendar', '/compliance-calendar.html'), ('Contact us', '/contact.html'), ('Refer & Earn', '/refer.html'), ('Careers', '/careers.html')]:
        search_items.append([l, h, 'Resources'])
    sjson = html.escape(json.dumps(search_items, ensure_ascii=False), quote=True)
    search_svg = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/><path d="M20 20l-3.5-3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
    return f'''<!--IWF:HEADER-->
<header class="iwf-header">
  <div class="iwf-wrap iwf-bar">
    {logo()}
    <ul class="iwf-menu">{"".join(lis)}
      <li class="iwf-extra"><a href="/refer.html" class="iwf-link">Refer 🎁</a></li>
      <li class="iwf-extra"><a href="/careers.html" class="iwf-link">We're Hiring! 🎉</a></li>
    </ul>
    <div class="iwf-cta">
      <button class="iwf-search-btn" type="button" aria-label="Search services">{search_svg}</button>
      <a href="/crm/" class="iwf-btn iwf-btn-ghost iwf-login">Login</a>
      <button class="iwf-burger" type="button" aria-label="Open menu"><span></span></button>
    </div>
  </div>
  <div class="iwf-search" data-items="{sjson}">
    <div class="iwf-search-inner">
      <input type="text" class="iwf-search-input" placeholder="Search services, e.g. GST registration, trademark, LLP" aria-label="Search services" autocomplete="off">
      <button class="iwf-search-close" type="button" aria-label="Close search">×</button>
      <div class="iwf-search-results"></div>
    </div>
  </div>
</header>
<div class="iwf-drawer" role="dialog" aria-label="Menu"><div class="iwf-drawer-panel">
  <div class="iwf-drawer-head">{logo()}<button class="iwf-drawer-close" type="button" aria-label="Close menu">×</button></div>
  {drawer_menus}
  <div class="iwf-drawer-links"><a href="/refer.html">Refer 🎁</a><a href="/careers.html">We're Hiring! 🎉</a><a href="/learn/">Learning Center</a><a href="/business-search.html">Business Search</a><a href="/compliance-calendar.html">Compliance Calendar</a><a href="/contact.html">Contact us</a></div>
  <div class="iwf-drawer-cta"><a href="/contact.html" class="iwf-btn iwf-btn-dark" data-lead="General enquiry">Talk to an advisor</a><a href="/crm/" class="iwf-btn iwf-btn-ghost">Login</a></div>
</div></div>
<!--/IWF:HEADER-->'''


def footer_html():
    cols = ''.join(
        f'<div class="iwf-foot-col"><h5>{e(t)}</h5><ul>' + ''.join(f'<li><a href="{h}">{e(l)}</a></li>' for l, h in links) + '</ul></div>'
        for t, links in FOOTER_COLS)
    wa = f'https://wa.me/{SITE["whatsapp"]}'
    return f'''<!--IWF:FOOTER-->
<div class="iwf-footer" role="contentinfo"><div class="iwf-wrap">
  <div class="iwf-foot-grid">
    <div class="iwf-foot-brand">
      {logo()}
      <p>An online platform for company registration, tax filing and compliance in India. Work is delivered by independent, qualified CAs, CSs and lawyers.</p>
      <div class="iwf-foot-contact">
        <a href="{wa}" target="_blank" rel="noopener">WhatsApp {e(SITE["whatsapp_label"])}</a>
        <a href="mailto:{e(SITE["email"])}">{e(SITE["email"])}</a>
        <span>{e(SITE["hours"])}</span>
      </div>
    </div>
    {cols}
  </div>
  <div class="iwf-foot-note">{e(SITE["brand"])} is a private professional-services platform. It is not a government website and is not affiliated with the Ministry of Corporate Affairs, GSTN, the Income Tax Department or any other government body. Government fees, where applicable, are charged at actuals in addition to our professional fee.</div>
  <div class="iwf-foot-bottom">
    <div>© {SITE["year"]} {e(SITE["legal_name"].rstrip("."))}. All rights reserved.</div>
    <div class="iwf-foot-legal"><a href="/legal/terms.html">Terms</a><a href="/legal/privacy.html">Privacy</a><a href="/legal/refund.html">Refunds</a><a href="/services/">Sitemap</a></div>
  </div>
</div></div>
<!--/IWF:FOOTER-->'''


HEAD_LINKS = '<link rel="stylesheet" href="/assets/site.css"><!--IWF:CSS-->'
BODY_SCRIPT = '<script src="/assets/site.js"></script><!--IWF:JS-->'
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Geist:wght@300;400;500;600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">'


def apply_chrome(text):
    """Swap in the shared header/footer and make sure the shared CSS/JS are linked."""
    hdr, ftr = header_html(), footer_html()
    if '<!--IWF:HEADER-->' in text:
        text = re.sub(r'<!--IWF:HEADER-->.*?<!--/IWF:HEADER-->', lambda m: hdr, text, count=1, flags=re.S)
    else:
        text, n = re.subn(r'<nav>.*?</nav>', lambda m: hdr, text, count=1, flags=re.S)
        if not n:
            raise ValueError('no <nav> found')
    if '<!--IWF:FOOTER-->' in text:
        text = re.sub(r'<!--IWF:FOOTER-->.*?<!--/IWF:FOOTER-->', lambda m: ftr, text, count=1, flags=re.S)
    else:
        text, n = re.subn(r'<footer>.*?</footer>', lambda m: ftr, text, count=1, flags=re.S)
        if not n:
            raise ValueError('no <footer> found')
    if '<!--IWF:CSS-->' not in text:
        text = text.replace('</head>', HEAD_LINKS + '\n</head>', 1)
    if '<!--IWF:JS-->' not in text:
        idx = text.rfind('</body>')
        text = text[:idx] + BODY_SCRIPT + '\n' + text[idx:]
    return text


def page(path, title, desc, body, crumbs=None, extra_head='', extra_js=''):
    """Write a content page with the shared chrome."""
    crumb_html = ''
    if crumbs:
        parts = ['<a href="/">Home</a>'] + [f'<a href="{h}">{e(l)}</a>' if h else e(l) for l, h in crumbs]
        crumb_html = '<div class="crumb">' + '<span>/</span>'.join(parts) + '</div>'
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="https://{SITE["domain"]}{path.replace("index.html", "")}">
{FONTS}
<link rel="stylesheet" href="/assets/pages.css">
{extra_head}
</head>
<body>
<nav></nav>
<main>
{crumb_html}
{body}
</main>
<footer></footer>
<script>
document.querySelectorAll('.faq-item').forEach(function(i){{i.querySelector('.faq-q').addEventListener('click',function(){{i.classList.toggle('open')}})}});
document.querySelectorAll('form[data-lead-form]').forEach(function(f){{f.addEventListener('submit',function(ev){{ev.preventDefault();
  var fd=new FormData(f),extra=[];fd.forEach(function(v,k){{if(['name','phone','email','message'].indexOf(k)<0&&v)extra.push(k+': '+v)}});
  var m=(fd.get('message')||'');if(extra.length)m=extra.join(' | ')+(m?' | '+m:'');
  window.iwfSubmitLead({{name:fd.get('name')||'',phone:fd.get('phone')||'',email:fd.get('email')||'',message:m,service:f.getAttribute('data-lead-form'),source:'page:'+location.pathname}},f.querySelector('.iwf-msg'),f.querySelector('button[type=submit]')).then(function(ok){{if(ok)f.reset()}});
}})}});
</script>
{extra_js}
</body>
</html>
'''
    out = os.path.join(ROOT, path.lstrip('/'))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as fh:
        fh.write(apply_chrome(doc))


def services_directory():
    blocks = []
    total = set()
    for m in MENUS:
        groups = ''.join(
            f'<div class="dir-group"><h3>{e(t)}</h3><ul>' + ''.join(f'<li><a href="{h}">{e(l)}</a></li>' for l, h, b in items) + '</ul></div>'
            for t, items in m['cols'])
        n = sum(len(i) for _, i in m['cols'])
        total.update(h for _, items in m['cols'] for _, h, _ in items if h.startswith(S))
        blocks.append(f'<div class="dir-cat" id="{m["slug"]}"><h2>{e(m["label"])} <small>{n} SERVICES</small></h2><p class="sub">{e(m["blurb"])}.</p><div class="dir-groups">{groups}</div></div>')
    chips = ''.join(f'<a class="chip" href="#{m["slug"]}">{e(m["label"])}</a>' for m in MENUS)
    body = f'''<section class="page-hero"><div class="inner">
  <div class="eyebrow">All services</div>
  <h1>Every filing your business needs, <em>in one place.</em></h1>
  <p class="lede">{len(total)} services across registrations, tax, MCA compliance, intellectual property, accounting, legal drafting and global expansion. Pick one, or talk to an advisor if you are not sure where to start.</p>
  <div class="search-box"><input id="svcFilter" type="search" placeholder="Search services, e.g. GST, trademark, LLP" aria-label="Search services"></div>
</div></section>
<section class="section" style="padding-top:0"><div class="inner">
  <div class="chip-row">{chips}</div>
  {"".join(blocks)}
  <div class="card" style="text-align:center"><h3>Can't find what you need?</h3><p>We handle many filings that are not listed here. Tell us what you are trying to do.</p><a href="/contact.html" class="btn btn-primary" style="margin-top:1rem" data-lead="Service not listed">Talk to an advisor →</a></div>
</div></section>'''
    js = '''<script>
(function(){var q=document.getElementById('svcFilter');q.addEventListener('input',function(){var v=q.value.trim().toLowerCase();
document.querySelectorAll('.dir-cat').forEach(function(c){var any=false;c.querySelectorAll('.dir-group').forEach(function(g){var gAny=false;
g.querySelectorAll('li').forEach(function(li){var hit=!v||li.textContent.toLowerCase().indexOf(v)>-1;li.style.display=hit?'':'none';if(hit)gAny=true});
g.style.display=gAny?'':'none';if(gAny)any=true});c.style.display=any?'':'none'})})})();
</script>'''
    page('/services/index.html', f'All Services | {SITE["brand"]}', 'Browse every registration, tax, compliance, trademark and global expansion service offered by IndiaWiseFilings.', body, crumbs=[('All services', None)], extra_js=js)


def main():
    import content
    content.build(page, SITE, MENUS)
    services_directory()
    # Apply shared chrome to the homepage and every existing service page.
    targets = [os.path.join(ROOT, 'index.html')] + [
        os.path.join(ROOT, 'services', f) for f in sorted(os.listdir(os.path.join(ROOT, 'services')))
        if f.endswith('.html') and f != 'index.html']
    for p in targets:
        with open(p, encoding='utf-8') as fh:
            t = fh.read()
        new = apply_chrome(t)
        if new != t:
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(new)
    print(f'chrome applied to {len(targets)} existing pages')


if __name__ == '__main__':
    main()
