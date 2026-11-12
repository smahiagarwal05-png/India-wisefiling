"""Content pages for IndiaWiseFilings. Called by build_site.py.

All copy here is original to IndiaWiseFilings. Facts in the learning-center
guides were checked in November 2026; re-check them when the law changes.
Anything shown inside <span class="placeholder"> must be filled in before launch.
"""
import html

e = html.escape
S = '/services/'
REVIEWED = 'Last reviewed: November 2026'


def ph(text):
    return f'<span class="placeholder">{e(text)}</span>'


def lead_form(service, title='Get a <em>call back</em>', sub='Share your details and an advisor will WhatsApp you shortly.', extra_fields='', button='Send my details →', message_label='Anything to add? (optional)'):
    return f'''<div class="form-card">
  <h3>{title}</h3>
  <p class="sub">{sub}</p>
  <form data-lead-form="{e(service)}" novalidate>
    <label>Your name</label><input name="name" type="text" required placeholder="e.g. Ravi Kumar">
    <label>Phone (with WhatsApp)</label><input name="phone" type="tel" required placeholder="9876543210">
    <label>Email (optional)</label><input name="email" type="email" placeholder="you@email.com">
    {extra_fields}
    <label>{message_label}</label><textarea name="message"></textarea>
    <button type="submit">{button}</button>
    <div class="iwf-msg"></div>
  </form>
</div>'''


def faq(items):
    return ''.join(f'<div class="faq-item"><div class="faq-q">{e(q)}</div><div class="faq-a"><p>{a}</p></div></div>' for q, a in items)


def cta(title='Ready to get <em>started?</em>', text='Tell us what you need. An advisor will share pricing, documents and timelines on WhatsApp.', service='General enquiry'):
    return f'''<section class="cta-strip"><h2>{title}</h2><p>{text}</p>
<div class="btn-row"><a href="/contact.html" class="btn btn-primary" data-lead="{e(service)}">Talk to an advisor →</a><a href="/services/" class="btn btn-ghost">Browse all services</a></div></section>'''


# ---------------------------------------------------------------------------
# Learning center guides
# ---------------------------------------------------------------------------
GUIDES = [
    {
        'slug': 'who-needs-gst-registration', 'cat': 'GST', 'title': 'Who needs GST registration in India?',
        'desc': 'Turnover thresholds, the cases where registration is compulsory regardless of turnover, and what you need to apply.',
        'related': [('New GST Registration', S + 'gst-registration.html'), ('Composition Scheme', S + 'composition-scheme.html'), ('GST Amendment', S + 'gst-amendment.html')],
        'body': '''
<p>GST registration gives your business a 15-character GSTIN, lets you charge GST on invoices and lets you claim input tax credit on what you buy. Whether you must register depends on your turnover, what you sell and where you sell it.</p>
<h2>The turnover thresholds</h2>
<p>Registration becomes compulsory once your <strong>aggregate turnover</strong> in a financial year crosses the threshold that applies to you. Aggregate turnover is calculated on a PAN-India basis and includes taxable, exempt and export supplies.</p>
<table><tr><th>Type of supplier</th><th>Most states</th><th>Special category states</th></tr>
<tr><td>Supplying only goods</td><td>₹40 lakh</td><td>₹20 lakh (₹10 lakh in a few states)</td></tr>
<tr><td>Supplying services, or goods and services</td><td>₹20 lakh</td><td>₹10 lakh</td></tr></table>
<p>The ₹40 lakh limit for goods applies only in states that have adopted it, so check the rule for your state before relying on it.</p>
<h2>When you must register regardless of turnover</h2>
<ul>
<li>You make inter-state supplies of goods (selling goods to a buyer in another state).</li>
<li>You sell goods through an e-commerce marketplace that collects tax at source, subject to the limited relaxations notified for small sellers.</li>
<li>You are a casual taxable person or a non-resident taxable person making taxable supplies in India.</li>
<li>You are liable to pay tax under reverse charge.</li>
<li>You are required to deduct TDS or collect TCS under GST, or you operate an e-commerce platform.</li>
<li>You are an Input Service Distributor or you supply online information and database services from outside India to Indian consumers.</li>
</ul>
<h2>Voluntary registration</h2>
<p>You can register even below the threshold. Businesses often do this to claim input tax credit, to sell to larger companies that insist on a GSTIN, or to list on marketplaces. Once registered you must file returns every period, even when there is nothing to report.</p>
<h2>Composition scheme</h2>
<p>Small businesses with turnover up to ₹1.5 crore (₹75 lakh in some special category states) can opt for the composition scheme and pay tax at a flat, low rate with quarterly payments and an annual return. Service providers have a separate limit of ₹50 lakh. Composition dealers cannot claim input tax credit or make inter-state sales.</p>
<h2>Documents you will need</h2>
<ul>
<li>PAN of the business (or of the proprietor)</li>
<li>Aadhaar of the proprietor, partners or directors, for authentication</li>
<li>Proof of business address: electricity bill, property tax receipt, rent agreement or NOC from the owner</li>
<li>Incorporation certificate, partnership deed or LLP agreement, as applicable</li>
<li>Bank account details and a photograph of the authorised signatory</li>
</ul>
<div class="callout">Thresholds and exceptions change by notification. Confirm your position on the GST portal or with a professional before you decide not to register.</div>
'''},
    {
        'slug': 'gstin-format-explained', 'cat': 'GST', 'title': 'Understanding your GSTIN: what each character means',
        'desc': 'How the 15-character GST number is built from the state code, PAN, entity number and a check digit.',
        'related': [('Business Search (GSTIN checker)', '/business-search.html'), ('New GST Registration', S + 'gst-registration.html')],
        'body': '''
<p>Every GST registration gets a 15-character Goods and Services Tax Identification Number. It is not random: each part tells you something about the business.</p>
<table><tr><th>Characters</th><th>Meaning</th><th>Example (27AAPFU0939F1ZV)</th></tr>
<tr><td>1 to 2</td><td>State code of the registration</td><td>27 = Maharashtra</td></tr>
<tr><td>3 to 12</td><td>PAN of the business</td><td>AAPFU0939F</td></tr>
<tr><td>13</td><td>Entity number for that PAN in that state (1 to 9, then A to Z)</td><td>1 = first registration</td></tr>
<tr><td>14</td><td>Default character, currently Z</td><td>Z</td></tr>
<tr><td>15</td><td>Check character calculated from the first 14</td><td>V</td></tr></table>
<h2>Why the check character matters</h2>
<p>The last character is computed from the first fourteen using a modulus-36 formula. If someone mistypes a GSTIN on an invoice, the check character usually no longer matches. Our <a href="/business-search.html">free GSTIN checker</a> runs this test instantly, so you can catch typos before you claim input tax credit on a wrong number.</p>
<h2>The PAN inside the GSTIN</h2>
<p>The fourth character of the PAN shows the holder type: <strong>P</strong> for an individual, <strong>C</strong> for a company, <strong>F</strong> for a firm or LLP, <strong>H</strong> for a HUF, <strong>T</strong> for a trust, <strong>A</strong> for an association of persons and <strong>G</strong> for government.</p>
<h2>One PAN, many GSTINs</h2>
<p>A business needs a separate GSTIN in every state where it makes taxable supplies, and may take more than one in a state for separate business verticals. All of them share the same PAN and differ in the state code and the entity number.</p>
<div class="callout">A valid format does not prove a GSTIN is active. Always confirm the status on the official GST portal\'s "Search Taxpayer" page before relying on it.</div>
'''},
    {
        'slug': 'gst-return-due-dates', 'cat': 'GST', 'title': 'GST returns and due dates: GSTR-1, GSTR-3B, GSTR-9',
        'desc': 'Which returns a regular taxpayer files, monthly versus quarterly (QRMP) filing, and the default due dates.',
        'related': [('GSTR-1 Filing', S + 'gstr-1-filing.html'), ('GSTR-3B Filing', S + 'gstr-3b-filing.html'), ('GSTR-9 Annual Return', S + 'gstr-9-annual-return.html'), ('Compliance Calendar', '/compliance-calendar.html')],
        'body': '''
<p>A regular GST taxpayer files two returns every period and one return every year. If your turnover is up to ₹5 crore you can choose the Quarterly Return Monthly Payment (QRMP) scheme and file quarterly while paying tax monthly.</p>
<table><tr><th>Return</th><th>What it reports</th><th>Monthly filers</th><th>QRMP filers</th></tr>
<tr><td>GSTR-1</td><td>Outward supplies (your sales)</td><td>11th of next month</td><td>13th of the month after the quarter (optional IFF by the 13th for B2B invoices in months 1 and 2)</td></tr>
<tr><td>GSTR-3B</td><td>Summary return and tax payment</td><td>20th of next month</td><td>22nd or 24th of the month after the quarter, depending on your state</td></tr>
<tr><td>PMT-06</td><td>Monthly tax payment under QRMP</td><td>Not applicable</td><td>25th of months 1 and 2 of the quarter</td></tr>
<tr><td>GSTR-9</td><td>Annual return</td><td colspan="2">31 December after the financial year. Mandatory above ₹2 crore turnover.</td></tr>
<tr><td>GSTR-9C</td><td>Reconciliation statement</td><td colspan="2">With GSTR-9, for turnover above ₹5 crore (self-certified)</td></tr></table>
<h2>Composition taxpayers</h2>
<p>Composition dealers pay tax quarterly through CMP-08 by the 18th of the month after each quarter and file one annual return, GSTR-4, by 30 April.</p>
<h2>What happens if you file late</h2>
<ul>
<li>A late fee is charged per day of delay for GSTR-1 and GSTR-3B, with a lower rate for nil returns and a cap based on turnover.</li>
<li>Interest at 18% a year is charged on tax paid late, calculated on the cash portion of the liability.</li>
<li>You cannot file GSTR-1 for a period until earlier returns are filed, and continued non-filing can lead to suspension or cancellation of your registration.</li>
<li>Your buyers may not see your invoices in their GSTR-2B, which blocks their input tax credit and damages the relationship.</li>
</ul>
<h2>File nil returns too</h2>
<p>If you had no sales and no purchases in a period, you still have to file. Nil GSTR-1 and GSTR-3B can be filed quickly, including by SMS, but missing them still attracts late fees.</p>
<div class="callout">Due dates on this page are the statutory defaults. The government frequently extends them by notification. Check our <a href="/compliance-calendar.html">compliance calendar</a> and the GST portal for the current dates.</div>
'''},
    {
        'slug': 'private-limited-vs-llp-vs-opc', 'cat': 'Startup', 'title': 'Private Limited vs LLP vs OPC: which structure should you choose?',
        'desc': 'A side-by-side comparison of ownership, liability, compliance load, tax and fundraising for the three most common structures.',
        'related': [('Private Limited Company', S + 'private-limited-company.html'), ('Limited Liability Partnership', S + 'limited-liability-partnership.html'), ('One Person Company', S + 'one-person-company.html'), ("Founder's Guide", '/founders-guide.html')],
        'body': '''
<p>All three structures give you limited liability, a separate legal identity and the ability to own assets and sign contracts in the entity\'s name. The right choice depends on who owns the business, whether you plan to raise equity and how much compliance you can manage.</p>
<table><tr><th></th><th>Private Limited Company</th><th>LLP</th><th>One Person Company</th></tr>
<tr><td>Owners</td><td>2 to 200 shareholders</td><td>2 or more partners, no upper limit</td><td>1 member (a natural person who is an Indian citizen)</td></tr>
<tr><td>Management</td><td>At least 2 directors, one resident in India</td><td>At least 2 designated partners, one resident in India</td><td>At least 1 director, plus a nominee</td></tr>
<tr><td>Raising equity</td><td>Easy: issue shares to investors, ESOPs possible</td><td>Difficult: investors cannot hold shares</td><td>Limited: must convert to raise equity</td></tr>
<tr><td>Statutory audit</td><td>Always required</td><td>Only above ₹40 lakh turnover or ₹25 lakh contribution</td><td>Always required</td></tr>
<tr><td>Annual MCA filings</td><td>AOC-4, MGT-7/7A, ADT-1 and others</td><td>Form 8 and Form 11</td><td>AOC-4 and MGT-7A</td></tr>
<tr><td>Income tax</td><td>22% concessional regime available (plus surcharge and cess)</td><td>30% flat (plus surcharge and cess), no tax on profit distribution</td><td>Same as a private company</td></tr>
<tr><td>Best for</td><td>Startups planning to raise funding or issue ESOPs</td><td>Professional firms, family businesses, consultancies</td><td>Solo founders who want limited liability</td></tr></table>
<h2>Choose a private limited company if</h2>
<ul><li>You plan to raise angel or venture funding, or want to offer ESOPs.</li><li>You want to apply for DPIIT recognition under Startup India, which is more common for companies.</li><li>You want the credibility a "Pvt Ltd" name brings with enterprise customers and banks.</li></ul>
<h2>Choose an LLP if</h2>
<ul><li>You are running a services or professional firm with partners who will share profits.</li><li>You want lower compliance and no mandatory audit while you are small.</li><li>You do not expect to bring in equity investors.</li></ul>
<h2>Choose an OPC if</h2>
<ul><li>You are the only founder and want limited liability with a single owner.</li><li>You are comfortable converting to a private limited company later, which the law now allows at any time.</li></ul>
<h2>What about sole proprietorships and partnerships?</h2>
<p>They are the quickest to start, since they need little more than a GST or Shop Act registration and a bank account. But the owners are personally liable for business debts, and these structures cannot raise equity. Many founders start as proprietors and incorporate once revenue picks up.</p>
<div class="callout">Tax rates and thresholds change with each Budget. Confirm current figures with a CA before you decide.</div>
'''},
    {
        'slug': 'annual-compliance-private-limited-company', 'cat': 'MCA', 'title': 'Annual compliance checklist for a private limited company',
        'desc': 'Every recurring MCA and tax filing a private company must make, with default timelines and what happens if you miss them.',
        'related': [('ROC Annual Filing', S + 'roc-annual-filing.html'), ('Director KYC', S + 'director-kyc.html'), ('DPT-3 Filing', S + 'dpt-3-filing.html'), ('Board Meeting Minutes', S + 'board-meeting-minutes.html')],
        'body': '''
<p>A private limited company has to file with the Registrar of Companies (ROC) every year even if it had no revenue. Missing these filings leads to additional fees that keep growing, and continued default can get the company struck off and its directors disqualified.</p>
<h2>Event-based filings in the first year</h2>
<ul>
<li><strong>Appoint the first auditor</strong> within 30 days of incorporation.</li>
<li><strong>INC-20A</strong>, the declaration of commencement of business, within 180 days of incorporation, once the subscription money has reached the company\'s bank account.</li>
<li><strong>Share certificates</strong> to subscribers within 60 days of incorporation.</li>
</ul>
<h2>Every year</h2>
<table><tr><th>Requirement</th><th>Default timeline</th></tr>
<tr><td>Board meetings</td><td>At least 4 a year with no more than 120 days between two meetings (small companies and OPCs: at least one in each half of the year)</td></tr>
<tr><td>Annual General Meeting (AGM)</td><td>Within 6 months of the financial year end, so by 30 September (first AGM within 9 months of the first year end)</td></tr>
<tr><td>ADT-1 (auditor appointment)</td><td>Within 15 days of the AGM at which the auditor is appointed</td></tr>
<tr><td>AOC-4 (financial statements)</td><td>Within 30 days of the AGM</td></tr>
<tr><td>MGT-7 or MGT-7A (annual return)</td><td>Within 60 days of the AGM</td></tr>
<tr><td>DPT-3 (return of deposits and outstanding loans)</td><td>By 30 June</td></tr>
<tr><td>MSME Form 1 (dues to MSME suppliers beyond 45 days)</td><td>Half-yearly, by 30 April and 31 October</td></tr>
<tr><td>Income tax return</td><td>By 31 October (companies are always audited)</td></tr>
<tr><td>DIR-3 KYC Web for each director</td><td>Once every three financial years, by 30 June, plus within 30 days of any change in contact details</td></tr></table>
<h2>Also keep track of</h2>
<ul>
<li>Statutory registers (members, directors, charges) kept up to date at the registered office.</li>
<li>Director disclosures (MBP-1 and DIR-8) at the first board meeting of the year.</li>
<li>GST and TDS returns, which run on their own monthly and quarterly cycles.</li>
</ul>
<h2>What late filing costs</h2>
<p>MCA charges an additional fee for each day a form is late, on top of the normal filing fee, with no cap for most forms. Directors of a company that has not filed financial statements or annual returns for three continuous years can be disqualified for five years.</p>
<div class="callout">MCA rules and timelines change by notification. Our <a href="/compliance-calendar.html">compliance calendar</a> lists the upcoming defaults; confirm the current position on the MCA portal.</div>
'''},
    {
        'slug': 'itr-forms-and-due-dates', 'cat': 'Income Tax', 'title': 'Which ITR form should you file, and by when?',
        'desc': 'ITR-1 to ITR-7 in plain language, with the due dates that apply after Budget 2026.',
        'related': [('ITR for Salaried', S + 'itr-salaried.html'), ('Freelancer ITR', S + 'itr-freelancer.html'), ('Business ITR', S + 'itr-business.html'), ('Capital Gains Filing', S + 'itr-capital-gains.html')],
        'body': '''
<p>The form you file depends on the type of income you have and the kind of taxpayer you are. Filing on the wrong form can lead to a defective-return notice, so it is worth getting right.</p>
<table><tr><th>Form</th><th>Who uses it</th></tr>
<tr><td>ITR-1 (Sahaj)</td><td>Resident individuals with salary or pension, one house property, other sources such as interest, and limited long-term capital gains, with total income up to ₹50 lakh</td></tr>
<tr><td>ITR-2</td><td>Individuals and HUFs without business income, including those with capital gains, more than one house property, foreign assets or income above ₹50 lakh</td></tr>
<tr><td>ITR-3</td><td>Individuals and HUFs with business or professional income, including freelancers and partners in firms</td></tr>
<tr><td>ITR-4 (Sugam)</td><td>Residents who opt for presumptive taxation on business or professional income, within the prescribed limits</td></tr>
<tr><td>ITR-5</td><td>Firms, LLPs, associations of persons and bodies of individuals</td></tr>
<tr><td>ITR-6</td><td>Companies</td></tr>
<tr><td>ITR-7</td><td>Trusts, political parties, research institutions and similar entities</td></tr></table>
<h2>Due dates</h2>
<p>Budget 2026 separated the due dates for salaried and non-audit business taxpayers.</p>
<table><tr><th>Who</th><th>Due date</th></tr>
<tr><td>ITR-1 and ITR-2 filers</td><td>31 July</td></tr>
<tr><td>ITR-3 and ITR-4 filers who do not need a tax audit</td><td>31 August</td></tr>
<tr><td>Taxpayers whose accounts must be audited, including all companies</td><td>31 October (tax audit report by 30 September)</td></tr>
<tr><td>Transfer pricing cases</td><td>30 November</td></tr>
<tr><td>Belated return</td><td>31 December</td></tr>
<tr><td>Revised return</td><td>31 March</td></tr></table>
<h2>Before you file</h2>
<ul>
<li>Match your income and TDS with Form 26AS and the Annual Information Statement (AIS).</li>
<li>Decide between the new and old tax regimes. Business taxpayers who want the old regime must opt for it on time.</li>
<li>Keep proofs of deductions, rent receipts and capital gains statements ready.</li>
<li>Verify the return within 30 days of filing, usually through Aadhaar OTP, or it is treated as not filed.</li>
</ul>
<div class="callout">The Income-tax Act, 2025 has replaced the 1961 Act from 1 April 2026, and form names and section numbers are being updated. Confirm the form and date that apply to you on the income tax portal or with a CA.</div>
'''},
    {
        'slug': 'trademark-registration-process', 'cat': 'Trademark', 'title': 'Trademark registration in India: the step-by-step process',
        'desc': 'From searching the register to receiving your certificate, with timelines and the points where applications usually get stuck.',
        'related': [('Trademark Search', S + 'trademark-search.html'), ('Trademark Registration', S + 'trademark-registration.html'), ('Trademark Objection', S + 'trademark-objection.html'), ('Trademark Opposition', S + 'trademark-opposition.html')],
        'body': '''
<p>A registered trademark gives you the exclusive right to use your brand name or logo for the goods and services it covers, and the right to sue anyone who copies it. Registration lasts 10 years and can be renewed indefinitely.</p>
<ol class="steps-list">
<li><strong>Search the register</strong>Check the trademark registry for identical or similar marks in your class before you file. Most refusals come from conflicts that a proper search would have caught.</li>
<li><strong>Pick the right class</strong>Goods and services are divided into 45 classes. File in every class where you trade or plan to trade, since protection only covers the classes you apply in.</li>
<li><strong>File the application (Form TM-A)</strong>Once filed, you get an application number and can start using the ™ symbol. The government fee is lower for individuals, startups and small enterprises than for other applicants.</li>
<li><strong>Examination</strong>The registry examines the application and issues an examination report. If there is an objection, you must reply within 30 days of receiving the report.</li>
<li><strong>Hearing, if needed</strong>If the examiner is not satisfied with the reply, a hearing is scheduled where you or your attorney can argue the case.</li>
<li><strong>Publication in the Trade Marks Journal</strong>Accepted marks are published so the public can object. Anyone can file an opposition within four months of publication.</li>
<li><strong>Registration</strong>If there is no opposition, or the opposition is decided in your favour, the mark is registered and you can use the ® symbol.</li>
</ol>
<h2>Common reasons for objection</h2>
<ul>
<li>The mark is descriptive of the goods or services (for example, "Fresh Juice" for juices).</li>
<li>It is similar to an existing registered or pending mark.</li>
<li>It uses a geographical name, a common surname or a word that is common in the trade.</li>
<li>The specification of goods or services is vague or in the wrong class.</li>
</ul>
<h2>Protecting your brand abroad</h2>
<p>Indian registration only protects you in India. To protect your brand in other countries, you can file directly in each country or use the Madrid Protocol to file one international application designating many countries.</p>
<div class="callout">Timelines depend on the registry\'s workload and on whether objections or oppositions are raised. Use our <a href="/services/trademark-search.html">trademark search</a> service before filing.</div>
'''},
    {
        'slug': 'dir-3-kyc-three-year-cycle', 'cat': 'MCA', 'title': 'DIR-3 KYC is now once every three years: what changed',
        'desc': 'MCA replaced the annual director KYC with a three-year cycle from 31 March 2026. Here is who files, when, and the catch.',
        'related': [('Director KYC', S + 'director-kyc.html'), ('DIN Reactivation', S + 'din-reactivation.html'), ('DIN Application', S + 'din-application.html')],
        'body': '''
<p>Every person who holds a Director Identification Number (DIN) has to confirm their KYC details with the Ministry of Corporate Affairs. Until March 2026 this was an annual filing due by 30 September. Amended rules notified on 31 December 2025 changed the cycle with effect from 31 March 2026.</p>
<h2>What changed</h2>
<table><tr><th></th><th>Before 31 March 2026</th><th>From 31 March 2026</th></tr>
<tr><td>How often</td><td>Every financial year</td><td>Once every three consecutive financial years</td></tr>
<tr><td>Due date</td><td>30 September</td><td>30 June</td></tr>
<tr><td>Form</td><td>DIR-3 KYC e-form or DIR-3 KYC Web</td><td>Form DIR-3 KYC Web only</td></tr></table>
<h2>Who has to file</h2>
<p>Anyone holding a DIN as on 31 March of a financial year, whether or not they currently sit on a board. Designated partners of LLPs who hold a DIN are covered too.</p>
<h2>The catch: changes must be reported within 30 days</h2>
<p>The three-year cycle does not mean you can ignore your KYC in between. If your mobile number, email address or residential address changes, you must update it through DIR-3 KYC Web within 30 days of the change. An update filed for a change does not restart your three-year cycle.</p>
<h2>What happens if you miss it</h2>
<p>MCA marks the DIN as deactivated. A deactivated director cannot sign or file forms for any company, which can hold up annual filings and other changes. Reactivation requires filing the KYC with a late fee.</p>
<h2>Practical tips</h2>
<ul>
<li>Keep a simple record of every director\'s DIN, the year of their last full KYC and their next due year. MCA does not show you the next due date.</li>
<li>Drafts of the old form saved before 31 March 2026 were cancelled, so file afresh on the new form.</li>
<li>Make sure the director\'s mobile and email are their own: OTPs are sent to both during filing.</li>
</ul>
<div class="callout">This summary reflects the amended rules as reported in 2026. Confirm your own cycle on the MCA portal before you decide not to file.</div>
'''},
    {
        'slug': 'udyam-registration-guide', 'cat': 'Registrations', 'title': 'Udyam registration: the free MSME certificate explained',
        'desc': 'Who qualifies as micro, small or medium, what Udyam registration gets you, and how to register.',
        'related': [('Udyam Registration', S + 'udyam-registration.html'), ('MSME Form 1', S + 'msme-form-1.html'), ('Startup India', S + 'startup-india.html')],
        'body': '''
<p>Udyam registration is the government\'s official MSME registration. It is free, paperless and based on Aadhaar and PAN. Once registered, your business gets a permanent Udyam Registration Number and an e-certificate.</p>
<h2>Who counts as an MSME</h2>
<p>Classification uses both investment in plant, machinery or equipment and annual turnover. The limits revised from 1 April 2025 are:</p>
<table><tr><th>Category</th><th>Investment up to</th><th>Turnover up to</th></tr>
<tr><td>Micro</td><td>₹2.5 crore</td><td>₹10 crore</td></tr>
<tr><td>Small</td><td>₹25 crore</td><td>₹100 crore</td></tr>
<tr><td>Medium</td><td>₹125 crore</td><td>₹500 crore</td></tr></table>
<p>Exports are excluded when calculating turnover for classification.</p>
<h2>What registration gets you</h2>
<ul>
<li>Protection against delayed payments: buyers must pay registered micro and small suppliers within the agreed period, capped at 45 days, or pay interest.</li>
<li>Access to collateral-free loans under government credit guarantee schemes and priority sector lending.</li>
<li>Preference in government procurement, including exemption from earnest money deposits in many tenders.</li>
<li>Eligibility for state and central subsidy schemes, and concessions on trademark and patent fees.</li>
</ul>
<h2>How to register</h2>
<ol class="steps-list">
<li><strong>Keep Aadhaar and PAN ready</strong>For a proprietorship, the owner\'s Aadhaar; for a firm, the managing partner\'s; for a company or LLP, the authorised signatory\'s, plus the entity PAN.</li>
<li><strong>Enter business details on the Udyam portal</strong>Name, address, bank account, NIC activity codes and number of employees.</li>
<li><strong>Investment and turnover are picked up automatically</strong>They are linked from your income tax and GST data, so keep those filings up to date.</li>
<li><strong>Download the certificate</strong>It is issued online and does not need renewal, but you should update details when they change.</li>
</ol>
<div class="callout">Registration on the official portal is free. If anyone charges you a government fee for Udyam registration, ask what you are paying for. We charge only a professional fee when you want us to do it for you.</div>
'''},
]


def guide_pages(page, SITE):
    for g in GUIDES:
        related = ''.join(f'<li><a href="{h}">{e(l)} →</a></li>' for l, h in g['related'])
        others = ''.join(f'<li><a href="/learn/{o["slug"]}.html">{e(o["title"])}</a></li>' for o in GUIDES if o['slug'] != g['slug'] and o['cat'] == g['cat'])
        if not others:
            others = ''.join(f'<li><a href="/learn/{o["slug"]}.html">{e(o["title"])}</a></li>' for o in GUIDES[:4] if o['slug'] != g['slug'])
        body = f'''<section class="page-hero" style="padding-bottom:1.5rem"><div class="inner">
  <div class="eyebrow">{e(g["cat"])} guide</div>
  <h1>{e(g["title"])}</h1>
  <p class="lede">{e(g["desc"])}</p>
  <div class="meta">{REVIEWED} · Written by the {e(SITE["brand"])} compliance team</div>
</div></section>
<section class="prose-wrap"><div class="prose-grid">
  <article class="prose">{g["body"]}
  <p style="margin-top:2rem;font-size:.88rem;color:var(--muted)">This guide is general information, not legal or tax advice for your situation. <a href="/legal/disclaimer.html">Read our disclaimer</a>.</p></article>
  <aside class="side">
    <div class="card"><span class="kicker">Get it done</span><h3>Let an expert handle it</h3><ul>{related}</ul>
      <a href="/contact.html" class="btn btn-primary" style="margin-top:1rem;width:100%" data-lead="{e(g["related"][0][0])}">Talk to an advisor</a></div>
    <div class="card"><span class="kicker">Keep reading</span><ul>{others}</ul></div>
  </aside>
</div></section>
{cta()}'''
        page(f'/learn/{g["slug"]}.html', f'{g["title"]} | {SITE["brand"]} Learning Center', g['desc'], body,
             crumbs=[('Learning Center', '/learn/'), (g['cat'], None)])

    cats = []
    for g in GUIDES:
        if g['cat'] not in cats:
            cats.append(g['cat'])
    chips = '<button class="chip on" type="button" data-cat="All">All</button>' + ''.join(f'<button class="chip" type="button" data-cat="{e(c)}">{e(c)}</button>' for c in cats)
    cards = ''.join(f'<a class="card guide" data-cat="{e(g["cat"])}" href="/learn/{g["slug"]}.html"><span class="kicker">{e(g["cat"])}</span><h3>{e(g["title"])}</h3><p>{e(g["desc"])}</p><span class="more">Read guide →</span></a>' for g in GUIDES)
    body = f'''<section class="page-hero"><div class="inner">
  <div class="eyebrow">Learning Center</div>
  <h1>Plain-language guides to <em>Indian business compliance.</em></h1>
  <p class="lede">GST, income tax, MCA filings, trademarks and registrations explained without the jargon. Written and reviewed by our compliance team.</p>
</div></section>
<section class="section" style="padding-top:0"><div class="inner">
  <div class="chip-row" id="guideFilter">{chips}</div>
  <div class="grid-3" id="guideGrid">{cards}</div>
</div></section>
<section class="section alt"><div class="inner grid-2" style="align-items:center">
  <div><h2>Never miss a <em>due date.</em></h2><p class="sub">See every GST, TDS, ITR, payroll and ROC deadline coming up in the next 60 days.</p><a href="/compliance-calendar.html" class="btn btn-primary">Open the compliance calendar →</a></div>
  <div><h2>Starting a <em>business?</em></h2><p class="sub">Our founder\'s guide walks you from choosing a structure to your first year of filings.</p><a href="/founders-guide.html" class="btn btn-ghost">Read the founder\'s guide →</a></div>
</div></section>
{cta()}'''
    js = '''<script>(function(){var bar=document.getElementById('guideFilter');bar.addEventListener('click',function(ev){var b=ev.target.closest('.chip');if(!b)return;
bar.querySelectorAll('.chip').forEach(function(x){x.classList.toggle('on',x===b)});var c=b.getAttribute('data-cat');
document.querySelectorAll('#guideGrid .guide').forEach(function(g){g.style.display=(c==='All'||g.getAttribute('data-cat')===c)?'':'none'})})})();</script>'''
    page('/learn/index.html', f'Learning Center: GST, Tax and Compliance Guides | {SITE["brand"]}', 'Free guides on GST registration and returns, income tax filing, MCA compliance, trademarks and MSME registration in India.', body, crumbs=[('Learning Center', None)], extra_js=js)


# ---------------------------------------------------------------------------
# Company pages
# ---------------------------------------------------------------------------
def company_pages(page, SITE, MENUS):
    wa = f'https://wa.me/{SITE["whatsapp"]}'
    brand = SITE['brand']

    # ---- About ----
    cats = ''.join(f'<a class="card" href="/services/#{m["slug"]}"><span class="kicker">{e(m["label"])}</span><h3>{e(m["blurb"]).capitalize()}</h3><span class="more">See services →</span></a>' for m in MENUS)
    body = f'''<section class="page-hero"><div class="inner">
  <div class="eyebrow">About {e(brand)}</div>
  <h1>Compliance should not be the hardest part of <em>running a business.</em></h1>
  <p class="lede">{e(brand)} helps founders, small businesses and professionals in India register, file and stay compliant without chasing paperwork. You tell us what you need; a qualified professional does the work and keeps you updated on WhatsApp.</p>
</div></section>
<section class="section alt"><div class="inner">
  <h2>What we <em>believe</em></h2><p class="sub">The principles behind how we work with every customer.</p>
  <div class="grid-3">
    <div class="card"><span class="kicker">01</span><h3>Prices you can see upfront</h3><p>Our professional fee is shown before you pay. Government fees are charged at actuals and listed separately, so you know exactly where your money goes.</p></div>
    <div class="card"><span class="kicker">02</span><h3>Real professionals do the work</h3><p>Filings are prepared and reviewed by Chartered Accountants, Company Secretaries and lawyers in our network, not by a chatbot.</p></div>
    <div class="card"><span class="kicker">03</span><h3>Updates where you already are</h3><p>You get status updates, document requests and deadline reminders on WhatsApp, so nothing waits in an inbox.</p></div>
    <div class="card"><span class="kicker">04</span><h3>Plain language, always</h3><p>We explain what a filing is for, what it costs and what happens if you miss it, in words that make sense.</p></div>
    <div class="card"><span class="kicker">05</span><h3>Your data stays yours</h3><p>Documents are shared only with the professional handling your work. Read our <a href="/legal/confidentiality.html">confidentiality policy</a>.</p></div>
    <div class="card"><span class="kicker">06</span><h3>We stay after the first filing</h3><p>Registration is the start. We track your recurring GST, TDS, ROC and payroll deadlines so you stay compliant all year.</p></div>
  </div>
</div></section>
<section class="section"><div class="inner">
  <h2>What we <em>do</em></h2><p class="sub">Over 150 services across nine areas, from your first registration to expanding abroad.</p>
  <div class="grid-3">{cats}</div>
</div></section>
<section class="section alt"><div class="inner">
  <h2>How it <em>works</em></h2>
  <ol class="steps-list">
    <li><strong>Tell us what you need</strong>Pick a service or describe your situation. If you are not sure what applies, an advisor will help you work it out.</li>
    <li><strong>Get a clear quote</strong>We confirm the price, the documents required and the timeline on WhatsApp before you pay anything.</li>
    <li><strong>Share documents securely</strong>Upload or send your documents; a dedicated professional prepares the filing.</li>
    <li><strong>Review and file</strong>You review the draft, we file it with the authority and send you the acknowledgement and final certificate.</li>
  </ol>
</div></section>
<section class="section"><div class="inner grid-2">
  <div class="card"><span class="kicker">Company details</span><h3>{e(SITE["legal_name"])}</h3><p>{ph(SITE["cin"])}<br>{ph(SITE["address"])}<br>Email: <a href="mailto:{e(SITE["email"])}">{e(SITE["email"])}</a><br>WhatsApp: <a href="{wa}">{e(SITE["whatsapp_label"])}</a></p></div>
  <div class="card"><span class="kicker">Work with us</span><h3>Join the team or our professional network</h3><p>We are hiring across operations, sales and engineering, and we welcome CAs, CSs and lawyers who want to join our partner network.</p><p style="margin-top:1rem"><a href="/careers.html" class="btn btn-primary">See open roles</a> <a href="/partners.html" class="btn btn-ghost">Become a partner</a></p></div>
</div></section>
{cta()}'''
    page('/about.html', f'About Us | {brand}', f'{brand} helps Indian businesses register, file taxes and stay compliant with transparent pricing and qualified professionals.', body, crumbs=[('About us', None)])

    # ---- Contact ----
    topics = '<label>What do you need help with?</label><select name="topic"><option value="">Choose one</option><option>Starting a business</option><option>GST</option><option>Income tax / TDS</option><option>Trademark / IP</option><option>MCA / ROC compliance</option><option>Accounting / payroll</option><option>Global expansion</option><option>An existing order</option><option>Something else</option></select>'
    body = f'''<section class="hero" id="start"><div class="hero-grid">
  <div>
    <div class="eyebrow">Contact us</div>
    <h1>Talk to a real <em>advisor.</em></h1>
    <p class="lede">Questions about a filing, a quote or an order in progress? Message us and the right person will get back to you, usually within working hours on the same day.</p>
    <div class="grid-2" style="margin-top:2rem">
      <a class="card" href="{wa}" target="_blank" rel="noopener"><span class="kicker">WhatsApp (fastest)</span><h3>{e(SITE["whatsapp_label"])}</h3><p>Chat with an advisor</p></a>
      <a class="card" href="mailto:{e(SITE["email"])}"><span class="kicker">Email</span><h3 style="word-break:break-all">{e(SITE["email"])}</h3><p>For documents and detailed queries</p></a>
      <div class="card"><span class="kicker">Hours</span><h3>{e(SITE["hours"])}</h3><p>Closed on national holidays</p></div>
      <div class="card"><span class="kicker">Registered office</span><h3 style="font-size:1rem">{ph(SITE["address"])}</h3><p>Meetings by appointment only</p></div>
    </div>
  </div>
  {lead_form('Contact form', title='Send us a <em>message</em>', sub='We will reply on WhatsApp or email.', extra_fields=topics, message_label='Your message')}
</div></section>
<section class="faq">
  <h2 style="font-family:Fraunces,serif;font-weight:400;font-size:2rem;margin-bottom:1rem">Before you <em style="color:var(--saffron-deep)">ask</em></h2>
  {faq([
    ('How quickly will you respond?', 'Most messages received during working hours get a reply the same day. WhatsApp is the fastest way to reach us.'),
    ('I already placed an order. Who do I contact?', 'Message us on WhatsApp from the number you used when you ordered, and mention your order or payment reference. Your request will go to the professional handling your work.'),
    ('Do you have an office I can visit?', 'Our services are delivered online so you never need to visit. If you need an in-person meeting, ask us and we will arrange an appointment.'),
    ('How do I raise a complaint?', f'Email {e(SITE["email"])} with the subject "Grievance". It will be acknowledged within 48 hours. See our <a href="/legal/terms.html">terms</a> for the full grievance process.'),
  ])}
</section>'''
    page('/contact.html', f'Contact Us | {brand}', f'Contact {brand} on WhatsApp or email for help with registrations, GST, income tax, trademarks and compliance.', body, crumbs=[('Contact us', None)])

    # ---- Careers ----
    roles = [
        ('Operations', 'Chartered Accountant / CA Associate', 'Prepare and review GST, income tax and audit work for a varied client base.'),
        ('Operations', 'Company Secretary / CS Associate', 'Handle incorporations, ROC filings, changes and secretarial records.'),
        ('Operations', 'Trademark and IP Executive', 'Run searches, draft applications and track objections and oppositions.'),
        ('Sales', 'Business Advisor (inside sales)', 'Help customers pick the right service and close quotes on WhatsApp and phone.'),
        ('Customer success', 'Customer Success Associate', 'Keep customers updated, collect documents and make sure orders finish on time.'),
        ('Engineering', 'Full-stack Developer', 'Build the website, CRM and the tools our professionals use every day.'),
    ]
    role_cards = ''.join(f'<div class="card"><span class="kicker">{e(t)}</span><h3>{e(r)}</h3><p>{e(d)}</p><a href="#apply" class="more" onclick="document.querySelector(\'#apply select\').value=\'{e(r)}\'">Apply for this role →</a></div>' for t, r, d in roles)
    opts = ''.join(f'<option>{e(r)}</option>' for _, r, _ in roles)
    body = f'''<section class="page-hero"><div class="inner">
  <div class="eyebrow">We're hiring!</div>
  <h1>Help us make compliance <em>simple for every business.</em></h1>
  <p class="lede">We are a small team building a better way for Indian businesses to handle their filings. If you like clear work, real ownership and customers who say thank you, we would like to hear from you.</p>
</div></section>
<section class="section" style="padding-top:0"><div class="inner">
  <h2>Open <em>roles</em></h2><p class="sub">Roles and locations change often. If you do not see a fit, apply anyway and tell us what you would like to do.</p>
  <div class="grid-3">{role_cards}</div>
</div></section>
<section class="section alt"><div class="inner grid-3">
  <div class="card"><h3>Learn across the stack</h3><p>Work on GST, tax, company law and IP for businesses in every industry, not one narrow process.</p></div>
  <div class="card"><h3>Own your outcomes</h3><p>Small teams mean your work reaches customers directly and you see the result.</p></div>
  <div class="card"><h3>Flexible by default</h3><p>Many roles can be done remotely, with clear hours so evenings stay yours.</p></div>
</div></section>
<section class="hero" id="apply"><div class="hero-grid">
  <div><h2 style="font-family:Fraunces,serif;font-weight:400;font-size:2.2rem;line-height:1.1;margin-bottom:1rem">Apply in <em style="color:var(--saffron-deep)">two minutes</em></h2>
  <p class="lede">Share your details and a link to your CV or LinkedIn. We read every application and reply to shortlisted candidates within a week.</p></div>
  {lead_form('Careers application', title='Your <em>application</em>', sub='We will contact you on WhatsApp or email.', extra_fields=f'<label>Role</label><select name="role"><option value="">Choose a role</option>{opts}<option>Something else</option></select><label>CV or LinkedIn link</label><input name="cv" type="url" placeholder="https://">', message_label='Why you? (optional)', button='Submit application →')}
</div></section>'''
    page('/careers.html', f'Careers | {brand}', f'Open roles at {brand} for CAs, CSs, IP executives, business advisors and developers.', body, crumbs=[('Careers', None)])

    # ---- Refer & Earn ----
    reward = SITE['refer_reward']
    body = f'''<section class="hero" id="start"><div class="hero-grid">
  <div>
    <div class="eyebrow">Refer &amp; Earn 🎁</div>
    <h1>Know a business that needs help? <em>Earn {e(reward)}.</em></h1>
    <p class="lede">Refer a friend, client or fellow founder. When they complete their first paid order with us, you get <strong>{e(reward)}</strong> and they get priority handling on their order.</p>
    <ol class="steps-list" style="margin-top:2rem">
      <li><strong>Share their details</strong>Fill in the form with your details and theirs. Let them know we will reach out.</li>
      <li><strong>We take it from there</strong>An advisor contacts them, understands what they need and shares a quote.</li>
      <li><strong>You get paid</strong>Once their order is paid and work starts, we send your reward by UPI or bank transfer.</li>
    </ol>
  </div>
  {lead_form('Referral', title='Refer <em>someone</em>', sub='First your details, then theirs.', extra_fields='<label>Their name</label><input name="friend_name" type="text" placeholder="Friend or client name"><label>Their phone</label><input name="friend_phone" type="tel" placeholder="9876543210"><label>What do they need?</label><input name="friend_need" type="text" placeholder="e.g. GST registration, company incorporation">', message_label='Anything we should know? (optional)', button='Submit referral →')}
</div></section>
<section class="faq">
  <h2 style="font-family:Fraunces,serif;font-weight:400;font-size:2rem;margin-bottom:1rem">Referral <em style="color:var(--saffron-deep)">terms</em></h2>
  {faq([
    ('When do I get my reward?', 'After the person you referred pays for their first order and work begins. We usually pay within 15 working days of that.'),
    ('Is there a limit to how many people I can refer?', 'No. You earn a reward for every referral that becomes a paying customer.'),
    ('Do they have to be new customers?', 'Yes. The person you refer must not have placed an order with us before, and must not already be in touch with our team for the same service.'),
    ('Can I refer myself or my own company?', 'No. Self-referrals and referrals between the same group of people or companies do not qualify.'),
    ('Can the programme change?', f'{e(brand)} may change or end the programme at any time. Referrals submitted before a change will be honoured on the terms that applied when they were made.'),
  ])}
</section>'''
    page('/refer.html', f'Refer & Earn | {brand}', f'Refer a business to {brand} and earn {reward} when they complete their first paid order.', body, crumbs=[('Refer & Earn', None)])

    # ---- Partner network ----
    body = f'''<section class="hero" id="start"><div class="hero-grid">
  <div>
    <div class="eyebrow">Partner network</div>
    <h1>For CAs, CSs and lawyers: <em>more clients, less admin.</em></h1>
    <p class="lede">Join the {e(brand)} professional network. We bring you verified customers with their documents collected, and pay you on time for the work you deliver.</p>
    <div class="grid-2" style="margin-top:2rem">
      <div class="card"><h3>Steady flow of work</h3><p>Incorporations, GST, ITR, ROC filings, trademarks and drafting in the areas you choose.</p></div>
      <div class="card"><h3>No chasing customers</h3><p>We handle sales, payments and document collection. You focus on the professional work.</p></div>
      <div class="card"><h3>Work from anywhere</h3><p>Pick up tasks remotely and set your own capacity.</p></div>
      <div class="card"><h3>Clear payouts</h3><p>Fixed fee per task, agreed before you accept it.</p></div>
    </div>
  </div>
  {lead_form('Partner application', title='Join the <em>network</em>', sub='We verify every professional before onboarding.', extra_fields='<label>You are a</label><select name="profession"><option value="">Choose one</option><option>Chartered Accountant</option><option>Company Secretary</option><option>Advocate</option><option>Trademark attorney</option><option>Cost accountant</option><option>Tax practitioner</option></select><label>Membership / enrolment number</label><input name="membership" type="text" placeholder="ICAI / ICSI / Bar Council number"><label>City</label><input name="city" type="text">', message_label='Services you want to take on', button='Apply to join →')}
</div></section>'''
    page('/partners.html', f'Partner Network for CAs, CSs and Lawyers | {brand}', f'Join the {brand} network of chartered accountants, company secretaries and lawyers.', body, crumbs=[('Partner network', None)])

    # ---- Founder's guide ----
    body = f'''<section class="page-hero" style="padding-bottom:1.5rem"><div class="inner">
  <div class="eyebrow">Founder's Guide</div>
  <h1>From idea to a fully compliant business: <em>the founder's checklist.</em></h1>
  <p class="lede">Everything you need to set up a business in India properly, in the order you will need it. Each step links to a guide or to a service if you want us to do it.</p>
  <div class="meta">{REVIEWED}</div>
</div></section>
<section class="prose-wrap"><div class="prose-grid"><article class="prose">
<h2>Stage 1: Before you register</h2>
<ul>
<li><strong>Choose your structure.</strong> Private limited company, LLP, OPC, partnership or proprietorship. Read our <a href="/learn/private-limited-vs-llp-vs-opc.html">comparison guide</a>.</li>
<li><strong>Check your name.</strong> Make sure the name is available with MCA and does not conflict with a registered trademark. Run a <a href="{S}trademark-search.html">trademark search</a> early so you do not have to rebrand later.</li>
<li><strong>Decide the founders' split.</strong> Agree equity, roles, vesting and what happens if someone leaves, and put it in a <a href="{S}founders-agreement.html">founders agreement</a>.</li>
<li><strong>Arrange a registered office.</strong> You need an address with proof (utility bill plus NOC or rent agreement). A <a href="{S}virtual-office.html">virtual office</a> works if you do not have one.</li>
</ul>
<h2>Stage 2: Register the entity</h2>
<ul>
<li>Get Digital Signature Certificates for directors or partners (<a href="{S}dsc-for-directors.html">DSC</a>).</li>
<li>File the incorporation application. For a company this is the SPICe+ form, which also issues PAN and TAN and opens a bank account. See <a href="{S}private-limited-company.html">Private Limited</a>, <a href="{S}limited-liability-partnership.html">LLP</a> or <a href="{S}one-person-company.html">OPC</a> registration.</li>
<li>For a proprietorship or partnership, register under GST or the Shop Act and open a current account. See <a href="{S}sole-proprietorship.html">sole proprietorship</a> and <a href="{S}partnership-firm.html">partnership firm</a>.</li>
</ul>
<h2>Stage 3: The first 180 days</h2>
<ul>
<li>Deposit the subscription money and file <a href="{S}commencement-of-business.html">INC-20A</a> within 180 days.</li>
<li>Appoint the first auditor within 30 days and hold the first board meeting.</li>
<li>Get <a href="{S}gst-registration.html">GST registration</a> if you cross the threshold, sell goods inter-state or sell on marketplaces. Read <a href="/learn/who-needs-gst-registration.html">who needs GST</a>.</li>
<li>Register under the Shop and Establishment Act of your state (<a href="{S}shop-act-registration.html">Shop Act</a>) and for <a href="{S}professional-tax.html">professional tax</a> where applicable.</li>
<li>Get <a href="{S}udyam-registration.html">Udyam (MSME) registration</a>: it is free and protects you against late payments.</li>
<li>Apply for <a href="{S}startup-india.html">DPIIT recognition</a> under Startup India if you are eligible.</li>
<li>File your <a href="{S}trademark-registration.html">trademark application</a> for your name and logo.</li>
<li>Sector licences: <a href="{S}fssai-registration.html">FSSAI</a> for food, <a href="{S}import-export-code.html">IEC</a> for imports and exports, <a href="{S}trade-license.html">trade licence</a> from the local body.</li>
</ul>
<h2>Stage 4: When you hire</h2>
<ul>
<li>Use proper <a href="{S}employment-agreement.html">employment agreements</a> and <a href="{S}nda-drafting.html">NDAs</a>.</li>
<li>Register for <a href="{S}pf-registration.html">EPF</a> once you have 20 employees, and <a href="{S}esi-registration.html">ESI</a> once you have 10 (the ESI threshold can differ by state).</li>
<li>Run payroll with TDS on salary, PF and ESI challans and payslips. Our <a href="{S}hr-payroll-service.html">HR and payroll service</a> does this monthly.</li>
</ul>
<h2>Stage 5: Your first year of compliance</h2>
<ul>
<li>Monthly or quarterly <a href="{S}gstr-3b-filing.html">GST returns</a> and <a href="{S}tds-return-filing.html">TDS returns</a>.</li>
<li><a href="{S}accounting-services.html">Bookkeeping</a> every month, so year-end is not a scramble.</li>
<li>Annual <a href="{S}roc-annual-filing.html">ROC filings</a> (AOC-4, MGT-7/7A), the <a href="{S}statutory-audit.html">statutory audit</a> and the company <a href="{S}itr-business.html">income tax return</a>.</li>
<li>Use the <a href="/compliance-calendar.html">compliance calendar</a> to see what is due next, and read the <a href="/learn/annual-compliance-private-limited-company.html">annual compliance checklist</a>.</li>
</ul>
<div class="callout">Want one team to handle all of this? Tell us your stage and we will put together a single plan with one price.</div>
</article>
<aside class="side"><div class="card"><span class="kicker">Get started</span><h3>Plan your setup with an advisor</h3><p>We will tell you exactly which registrations you need, and what they cost, for your business.</p><a href="/contact.html" class="btn btn-primary" style="margin-top:1rem;width:100%" data-lead="Founder setup plan">Get my setup plan</a></div>
<div class="card"><span class="kicker">Read next</span><ul>{"".join(f'<li><a href="/learn/{g["slug"]}.html">{e(g["title"])}</a></li>' for g in GUIDES[:5])}</ul></div></aside>
</div></section>
{cta(service='Founder setup plan')}'''
    page('/founders-guide.html', f"Founder's Guide to Starting a Business in India | {brand}", 'A step-by-step checklist for founders: choosing a structure, registering, the first 180 days, hiring and the first year of compliance.', body, crumbs=[("Founder's Guide", None)])

    # ---- Compliance calendar ----
    body = f'''<section class="page-hero"><div class="inner">
  <div class="eyebrow">Compliance Calendar</div>
  <h1>Every deadline coming up in the <em>next 60 days.</em></h1>
  <p class="lede">GST returns, TDS deposits, income tax returns, payroll contributions and ROC filings, calculated from today's date. Click any item to have us file it for you.</p>
</div></section>
<section class="section" style="padding-top:0"><div class="inner">
  <div data-iwf-calendar data-days="60" data-filters></div>
  <p style="margin-top:1.5rem;font-size:.85rem;color:var(--muted)">These are the statutory default dates. The government often extends due dates by notification, so confirm the current date on the GST, income tax, EPFO or MCA portal. Some dates depend on your own circumstances (for example, the date of your AGM).</p>
</div></section>
{cta(title='Want us to track this <em>for you?</em>', text='Our compliance plans file every return on time and remind you before anything is due.', service='Compliance plan')}'''
    page('/compliance-calendar.html', f'Compliance Calendar: GST, TDS, ITR and ROC Due Dates | {brand}', 'Upcoming GST, TDS, income tax, payroll and MCA due dates for Indian businesses in the next 60 days.', body, crumbs=[('Compliance Calendar', None)], extra_js='<script src="/assets/calendar.js"></script>')

    # ---- Business search ----
    body = f'''<section class="page-hero"><div class="inner">
  <div class="eyebrow">Business Search</div>
  <h1>Check a GSTIN, PAN, CIN or LLPIN <em>in seconds.</em></h1>
  <p class="lede">Paste any Indian business identifier. We check the format and check digit, decode what it tells you, and link you to the official portal to confirm it is active.</p>
  <div class="search-box" style="margin-top:1.5rem">
    <input id="bsInput" type="text" autocomplete="off" spellcheck="false" placeholder="e.g. 27AAPFU0939F1ZV or U72900KA2019PTC123456" aria-label="Business identifier" style="text-transform:uppercase">
    <button class="btn btn-primary" id="bsGo" type="button">Check</button>
  </div>
  <div class="chip-row" style="margin-top:1rem"><span style="font-size:.85rem;color:var(--muted);align-self:center">Try:</span>
    <button class="chip" type="button" data-try="27AAPFU0939F1ZV">GSTIN</button><button class="chip" type="button" data-try="AAPFU0939F">PAN</button><button class="chip" type="button" data-try="U72900KA2019PTC123456">CIN</button><button class="chip" type="button" data-try="AAB-1234">LLPIN</button></div>
  <div class="result" id="bsResult"></div>
</div></section>
<section class="section alt"><div class="inner">
  <h2>Verify on the <em>official portals</em></h2><p class="sub">A valid format does not prove a registration is active. Always confirm on the government source.</p>
  <div class="grid-3">
    <a class="card" href="https://services.gst.gov.in/services/searchtp" target="_blank" rel="noopener"><span class="kicker">GST portal</span><h3>Search taxpayer by GSTIN or PAN</h3><p>Status, legal name, trade name and filing history.</p><span class="more">Open GST portal ↗</span></a>
    <a class="card" href="https://www.mca.gov.in/" target="_blank" rel="noopener"><span class="kicker">MCA</span><h3>Company and LLP master data</h3><p>Status, directors, incorporation date and filings.</p><span class="more">Open MCA ↗</span></a>
    <a class="card" href="https://eportal.incometax.gov.in/" target="_blank" rel="noopener"><span class="kicker">Income tax</span><h3>Verify PAN status</h3><p>Check that a PAN is valid and active.</p><span class="more">Open e-filing portal ↗</span></a>
    <a class="card" href="https://tmrsearch.ipindia.gov.in/eregister/" target="_blank" rel="noopener"><span class="kicker">IP India</span><h3>Trademark status</h3><p>Look up an application by number or proprietor.</p><span class="more">Open IP India ↗</span></a>
    <a class="card" href="https://udyamregistration.gov.in/" target="_blank" rel="noopener"><span class="kicker">Udyam</span><h3>Verify MSME registration</h3><p>Confirm a Udyam Registration Number.</p><span class="more">Open Udyam portal ↗</span></a>
    <a class="card" href="/learn/gstin-format-explained.html"><span class="kicker">Guide</span><h3>How a GSTIN is built</h3><p>State code, PAN, entity number and check digit explained.</p><span class="more">Read the guide →</span></a>
  </div>
</div></section>
{cta(title='Need a registration of your <em>own?</em>', text='GST, company, LLP, MSME or trademark: we handle the whole process.', service='Business registration')}'''
    page('/business-search.html', f'Business Search: GSTIN, PAN, CIN and LLPIN Checker | {brand}', 'Free tool to validate and decode Indian GSTIN, PAN, CIN and LLPIN numbers, with links to official verification portals.', body, crumbs=[('Business Search', None)], extra_js='<script src="/assets/business-search.js"></script>')


# ---------------------------------------------------------------------------
# Legal pages
# ---------------------------------------------------------------------------
def legal_pages(page, SITE):
    brand, legal = SITE['brand'], SITE['legal_name']
    contact = f'<p><strong>{e(legal)}</strong><br>{ph(SITE["address"])}<br>Email: <a href="mailto:{e(SITE["email"])}">{e(SITE["email"])}</a><br>WhatsApp: {e(SITE["whatsapp_label"])}</p>'
    nav = [('Terms & Conditions', '/legal/terms.html'), ('Privacy Policy', '/legal/privacy.html'), ('Refund Policy', '/legal/refund.html'), ('Confidentiality Policy', '/legal/confidentiality.html'), ('Disclaimer', '/legal/disclaimer.html')]
    docs = {
        'terms': ('Terms & Conditions', f'The terms that apply when you use the {brand} website and services.', f'''
<p>These terms govern your use of the website at {e(SITE["domain"])} and the services you order through it. "We", "us" and "{e(brand)}" mean {e(legal)}. "You" means the person or business using the website or ordering a service. By placing an order you agree to these terms.</p>
<h2>1. What we do</h2>
<p>We are a technology platform that connects you with qualified professionals (Chartered Accountants, Company Secretaries, advocates and other experts) who prepare and file applications, returns and documents on your behalf. We are not a government body, and we do not grant registrations, licences or approvals. Those decisions are made by the relevant authority.</p>
<h2>2. Your responsibilities</h2>
<ul><li>Give us information and documents that are complete, accurate and genuine, and tell us promptly if anything changes.</li>
<li>Review drafts we share with you and confirm them before filing. You are responsible for the contents of anything filed in your name.</li>
<li>Respond to requests for documents, OTPs or signatures in time. Delays on your side may delay the work or lead to late fees charged by the authority.</li>
<li>Use the website lawfully and not attempt to disrupt or misuse it.</li></ul>
<h2>3. Quotes, fees and payment</h2>
<p>Our professional fee for each service is shown on the website or in the quote we send you. Government fees, stamp duty and third-party charges are extra unless the quote says otherwise, and are passed on at actuals. Prices include or exclude GST as stated at the time of order. Work starts after payment is received.</p>
<h2>4. Timelines</h2>
<p>Timelines on our website are estimates based on typical processing. Authorities may take longer, raise queries or reject applications, and we are not responsible for delays caused by them or by incomplete information.</p>
<h2>5. Outcomes</h2>
<p>We will carry out the work with reasonable skill and care. We cannot guarantee that an authority will approve an application, accept a name or trademark, or decide a matter in your favour.</p>
<h2>6. Refunds</h2>
<p>Refunds are governed by our <a href="/legal/refund.html">Refund Policy</a>.</p>
<h2>7. Confidentiality and data</h2>
<p>We handle your information as described in our <a href="/legal/privacy.html">Privacy Policy</a> and <a href="/legal/confidentiality.html">Confidentiality Policy</a>.</p>
<h2>8. Intellectual property</h2>
<p>The website, its design, text and software belong to {e(legal)} or its licensors. Documents we prepare for you may be used by you for your own business.</p>
<h2>9. Limitation of liability</h2>
<p>To the extent permitted by law, our total liability for any claim relating to a service is limited to the professional fee you paid us for that service. We are not liable for indirect or consequential losses, or for penalties arising from information you supplied or from delays on your side.</p>
<h2>10. Grievances</h2>
<p>If you are unhappy with our service, write to our Grievance Officer, {ph(SITE["grievance_officer"])}, at <a href="mailto:{e(SITE["email"])}">{e(SITE["email"])}</a> with the subject "Grievance". We will acknowledge your complaint within 48 hours and aim to resolve it within 15 days.</p>
<h2>11. Governing law</h2>
<p>These terms are governed by the laws of India. Courts at {ph("City (TODO)")} have exclusive jurisdiction.</p>
<h2>12. Changes</h2>
<p>We may update these terms from time to time. The version on this page at the time of your order applies to that order.</p>
<h2>Contact</h2>{contact}'''),
        'privacy': ('Privacy Policy', 'How we collect, use, share and protect your personal data.', f'''
<p>This policy explains how {e(legal)} collects and uses personal data when you use our website or services. We process personal data in line with the Digital Personal Data Protection Act, 2023 and other applicable Indian law.</p>
<h2>1. What we collect</h2>
<ul><li><strong>Details you give us:</strong> name, phone number, email, business details, and the documents needed for your service (such as PAN, Aadhaar, address proof, photographs, financial statements and bank details).</li>
<li><strong>Payment information:</strong> processed by our payment gateway. We receive confirmation of payment but do not store your full card or banking credentials.</li>
<li><strong>Usage data:</strong> pages visited, device and browser information and approximate location, collected through cookies and similar technologies.</li>
<li><strong>Communications:</strong> messages you send us on WhatsApp, email or phone.</li></ul>
<h2>2. Why we use it</h2>
<ul><li>To provide the service you asked for, including preparing and filing documents with government authorities.</li>
<li>To contact you about your enquiry or order, including on WhatsApp.</li>
<li>To send reminders about deadlines relevant to the services you use. You can opt out at any time.</li>
<li>To process payments, prevent fraud and meet legal and tax obligations.</li>
<li>To improve our website and services.</li></ul>
<h2>3. Who we share it with</h2>
<ul><li>The professional handling your work, who is bound by confidentiality.</li>
<li>Government portals and authorities, as needed to file your application or return.</li>
<li>Service providers who help us run the business (hosting, payments, messaging), under contracts that require them to protect your data.</li>
<li>Authorities, where we are legally required to share it.</li></ul>
<p>We do not sell your personal data.</p>
<h2>4. Retention</h2>
<p>We keep your data for as long as needed to provide the service and to meet legal record-keeping requirements, after which it is deleted or anonymised.</p>
<h2>5. Your rights</h2>
<p>You can ask to access, correct or erase your personal data, withdraw consent for marketing, and nominate someone to exercise your rights. Contact us using the details below. Some data must be retained by law even after you ask us to delete it.</p>
<h2>6. Security</h2>
<p>We use access controls, encryption in transit and limited access on a need-to-know basis to protect your data. No system is completely secure; if a breach affects you we will notify you and the authorities as required by law.</p>
<h2>7. Cookies</h2>
<p>We use cookies to keep the website working and to understand how it is used. You can control cookies through your browser settings.</p>
<h2>8. Grievance Officer</h2>
<p>{ph(SITE["grievance_officer"])}<br>Email: <a href="mailto:{e(SITE["email"])}">{e(SITE["email"])}</a></p>
<h2>Contact</h2>{contact}'''),
        'refund': ('Refund Policy', 'When you can get a refund, how much, and how to ask for one.', f'''
<p>We want you to be happy with our service. This policy explains when refunds are available. It forms part of our <a href="/legal/terms.html">Terms &amp; Conditions</a>.</p>
<h2>1. Before work starts</h2>
<p>If you cancel before we have started work on your order, you get a full refund of our professional fee.</p>
<h2>2. After work starts</h2>
<p>Once a professional has started work (for example, drafting documents, running searches or preparing a return), we refund the professional fee minus the value of the work already completed. We will tell you how this was worked out.</p>
<h2>3. After filing</h2>
<p>Once an application, return or document has been filed with an authority, the professional fee for that filing is not refundable, because the work has been delivered.</p>
<h2>4. Government and third-party fees</h2>
<p>Government fees, stamp duty and other charges paid to third parties on your behalf cannot be refunded by us once paid. If an authority refunds any amount, we will pass it on to you.</p>
<h2>5. When an application is rejected</h2>
<p>An authority's decision to reject or query an application is not, by itself, grounds for a refund. If the rejection was caused by an error on our part, we will refile at no extra professional fee or refund our fee for that service.</p>
<h2>6. Delays on our side</h2>
<p>If we fail to start work within the timeline we committed to, for reasons within our control, you can cancel and receive a full refund of the professional fee.</p>
<h2>7. How to ask</h2>
<p>Email <a href="mailto:{e(SITE["email"])}">{e(SITE["email"])}</a> or WhatsApp us with your order details. Approved refunds are processed to the original payment method within 7 to 10 working days.</p>
<h2>Contact</h2>{contact}'''),
        'confidentiality': ('Confidentiality Policy', 'How we keep your business information and documents confidential.', f'''
<p>Filing for a business means handling sensitive information: identity documents, financial statements, ownership details and plans that are not yet public. This policy sets out how we keep it confidential.</p>
<h2>1. What we treat as confidential</h2>
<p>Everything you share with us about your business or yourself, including documents, financial data, business plans, brand names before filing, and the fact that you are our customer.</p>
<h2>2. Who can see it</h2>
<ul><li>Only the professional and the team members assigned to your work, and only as much as they need.</li>
<li>Every professional in our network and every employee signs a confidentiality agreement before handling customer work.</li>
<li>Information is shared with authorities only to the extent needed to file on your behalf.</li></ul>
<h2>3. How we protect it</h2>
<ul><li>Documents are stored on access-controlled systems and transmitted over encrypted connections.</li>
<li>Access is removed when a professional or employee no longer works on your matter.</li>
<li>We do not use your information to market to others or share it with third parties for their own purposes.</li></ul>
<h2>4. Exceptions</h2>
<p>We may disclose information if required by law, court order or a government authority, or with your consent.</p>
<h2>5. After your work is done</h2>
<p>We retain records only for as long as required by law and our professional obligations, then delete them securely.</p>
<h2>6. Questions or concerns</h2>
<p>If you believe your information has been mishandled, write to <a href="mailto:{e(SITE["email"])}">{e(SITE["email"])}</a> immediately.</p>
<h2>Contact</h2>{contact}'''),
        'disclaimer': ('Disclaimer', 'Important information about the content on this website.', f'''
<h2>Not a government website</h2>
<p>{e(brand)} is a private professional-services platform operated by {e(legal)}. It is not affiliated with, endorsed by or acting for the Ministry of Corporate Affairs, the Goods and Services Tax Network, the Income Tax Department, the Trade Marks Registry, EPFO, ESIC or any other government body. You can apply for most registrations directly on the relevant government portal yourself.</p>
<h2>General information only</h2>
<p>Guides, calculators, calendars and other content on this website are for general information. They are not legal, tax or financial advice for your situation. Laws, rates, thresholds and due dates change frequently, and while we try to keep the content current, it may not reflect the latest position. Please consult a qualified professional before acting on it.</p>
<h2>Tools</h2>
<p>The Business Search tool checks the format of identifiers. It does not confirm that a registration is genuine or active. Always verify on the official portal.</p>
<h2>Third-party links</h2>
<p>Links to government portals and other websites are provided for convenience. We are not responsible for their content or availability.</p>
<h2>Professional services</h2>
<p>Services are performed by qualified professionals in our network under our <a href="/legal/terms.html">Terms &amp; Conditions</a>. No professional relationship is formed by reading this website.</p>
<h2>Contact</h2>{contact}'''),
    }
    for slug, (title, desc, text) in docs.items():
        side = ''.join(f'<li><a href="{h}"{" style=\"color:var(--saffron-deep);font-weight:500\"" if h.endswith(slug + ".html") else ""}>{e(l)}</a></li>' for l, h in nav)
        body = f'''<section class="page-hero" style="padding-bottom:1.5rem"><div class="inner">
  <div class="eyebrow">Legal</div><h1>{e(title)}</h1><p class="lede">{e(desc)}</p><div class="meta">Effective date: {ph("DD Month 2026 (TODO)")}</div>
</div></section>
<section class="prose-wrap"><div class="prose-grid"><article class="prose">{text}</article>
<aside class="side"><div class="card"><span class="kicker">Legal</span><ul>{side}</ul></div></aside></div></section>'''
        page(f'/legal/{slug}.html', f'{title} | {brand}', desc, body, crumbs=[('Legal', None), (title, None)])


def build(page, SITE, MENUS):
    guide_pages(page, SITE)
    company_pages(page, SITE, MENUS)
    legal_pages(page, SITE)
