/* IndiaWiseFilings compliance calendar.
   Statutory default due dates only. Governments often extend dates, so every
   entry links to the related service and the page tells users to confirm on the
   official portal. Update RULES when the law changes.

   Each rule: { cat, title, who, href, day, months? (1-12, omit = every month), offset? }
   'day' is the day of the month the item falls due. */
(function () {
  var S = '/services/';
  var RULES = [
    // ---- monthly ----
    { cat: 'Income Tax', title: 'TDS / TCS deposit for last month', who: 'Anyone who deducted TDS or collected TCS (March deposit is due 30 April)', href: S + 'tds-return-filing.html', day: 7, months: [1,2,3,5,6,7,8,9,10,11,12] },
    { cat: 'Income Tax', title: 'TDS / TCS deposit for March', who: 'Deductors and collectors', href: S + 'tds-return-filing.html', day: 30, months: [4] },
    { cat: 'GST', title: 'GSTR-7 and GSTR-8', who: 'GST TDS deductors and e-commerce operators (TCS)', href: S + 'gstr-1-filing.html', day: 10 },
    { cat: 'GST', title: 'GSTR-1 (monthly filers)', who: 'Taxpayers filing GSTR-1 monthly', href: S + 'gstr-1-filing.html', day: 11 },
    { cat: 'GST', title: 'IFF / GSTR-1 (QRMP)', who: 'QRMP taxpayers: IFF in month 1 and 2, quarterly GSTR-1 after the quarter', href: S + 'gstr-1-filing.html', day: 13 },
    { cat: 'Payroll', title: 'PF and ESI contributions', who: 'Employers registered under EPF and ESIC', href: S + 'hr-payroll-service.html', day: 15 },
    { cat: 'GST', title: 'GSTR-3B (monthly filers)', who: 'Taxpayers with turnover above ₹5 crore, or who opted out of QRMP', href: S + 'gstr-3b-filing.html', day: 20 },
    { cat: 'GST', title: 'GSTR-3B (QRMP, category X states)', who: 'Quarterly filers in states such as Maharashtra, Karnataka, Gujarat, Tamil Nadu, Kerala, Telangana, AP, MP, Chhattisgarh, Goa', href: S + 'gstr-3b-filing.html', day: 22, months: [1,4,7,10] },
    { cat: 'GST', title: 'GSTR-3B (QRMP, category Y states)', who: 'Quarterly filers in states such as Delhi, UP, Punjab, Haryana, Rajasthan, Bihar, West Bengal and the North East', href: S + 'gstr-3b-filing.html', day: 24, months: [1,4,7,10] },
    { cat: 'GST', title: 'CMP-08 tax payment', who: 'Composition scheme taxpayers', href: S + 'composition-return.html', day: 18, months: [1,4,7,10] },
    // ---- quarterly income tax ----
    { cat: 'Income Tax', title: 'Advance tax instalment', who: 'Taxpayers whose tax for the year exceeds ₹10,000', href: S + 'advance-tax-calculation.html', day: 15, months: [3,6,9,12] },
    { cat: 'Income Tax', title: 'Quarterly TDS return', who: 'All TDS deductors (Q1 by 31 Jul, Q2 by 31 Oct, Q3 by 31 Jan, Q4 by 31 May)', href: S + 'tds-return-filing.html', day: 31, months: [1,5,7,10] },
    // ---- annual: income tax ----
    { cat: 'Income Tax', title: 'Issue salary TDS certificates (Form 16)', who: 'Employers', href: S + 'form-16-generation.html', day: 15, months: [6] },
    { cat: 'Income Tax', title: 'ITR-1 / ITR-2 filing', who: 'Salaried individuals, pensioners and capital gains cases', href: S + 'itr-salaried.html', day: 31, months: [7] },
    { cat: 'Income Tax', title: 'ITR-3 / ITR-4 filing (non-audit)', who: 'Freelancers, professionals and businesses not requiring tax audit', href: S + 'itr-freelancer.html', day: 31, months: [8] },
    { cat: 'Income Tax', title: 'Tax audit report', who: 'Businesses and professionals liable to tax audit', href: S + 'tax-audit.html', day: 30, months: [9] },
    { cat: 'Income Tax', title: 'ITR filing (audit cases)', who: 'Companies and taxpayers whose accounts are audited', href: S + 'itr-business.html', day: 31, months: [10] },
    { cat: 'Income Tax', title: 'ITR filing (transfer pricing cases)', who: 'Taxpayers with international or specified domestic transactions', href: S + 'transfer-pricing-audit.html', day: 30, months: [11] },
    { cat: 'Income Tax', title: 'Belated ITR, last date', who: 'Anyone who missed the original due date', href: S + 'itr-salaried.html', day: 31, months: [12] },
    // ---- annual: GST ----
    { cat: 'GST', title: 'GSTR-4 annual return', who: 'Composition scheme taxpayers', href: S + 'composition-return.html', day: 30, months: [4] },
    { cat: 'GST', title: 'GSTR-9 / GSTR-9C annual return', who: 'Regular taxpayers (GSTR-9 mandatory above ₹2 crore, 9C above ₹5 crore)', href: S + 'gstr-9-annual-return.html', day: 31, months: [12] },
    // ---- annual: MCA ----
    { cat: 'MCA', title: 'MSME Form 1 (Oct to Mar)', who: 'Companies with dues to MSME suppliers older than 45 days', href: S + 'msme-form-1.html', day: 30, months: [4] },
    { cat: 'MCA', title: 'LLP Form 11 annual return', who: 'All LLPs', href: S + 'llp-annual-filing.html', day: 30, months: [5] },
    { cat: 'MCA', title: 'DPT-3 return of deposits', who: 'Companies (other than government companies) with outstanding loans or deposits', href: S + 'dpt-3-filing.html', day: 30, months: [6] },
    { cat: 'MCA', title: 'DIR-3 KYC Web (once every 3 financial years)', who: 'DIN holders whose three-year cycle ends this year', href: S + 'director-kyc.html', day: 30, months: [6] },
    { cat: 'MCA', title: 'Last date to hold AGM', who: 'Companies (6 months from financial year end)', href: S + 'roc-annual-filing.html', day: 30, months: [9] },
    { cat: 'MCA', title: 'ADT-1 auditor appointment', who: 'Companies, within 15 days of the AGM', href: S + 'roc-annual-filing.html', day: 14, months: [10] },
    { cat: 'MCA', title: 'AOC-4 financial statements', who: 'Companies, within 30 days of the AGM', href: S + 'roc-annual-filing.html', day: 30, months: [10] },
    { cat: 'MCA', title: 'LLP Form 8 statement of accounts', who: 'All LLPs', href: S + 'llp-annual-filing.html', day: 30, months: [10] },
    { cat: 'MCA', title: 'MSME Form 1 (Apr to Sep)', who: 'Companies with dues to MSME suppliers older than 45 days', href: S + 'msme-form-1.html', day: 31, months: [10] },
    { cat: 'MCA', title: 'MGT-7 / MGT-7A annual return', who: 'Companies, within 60 days of the AGM', href: S + 'roc-annual-filing.html', day: 29, months: [11] }
  ];

  var MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

  function lastDay(y, m) { return new Date(y, m + 1, 0).getDate(); }

  // Returns sorted upcoming items between today and today + days.
  function upcoming(days, cat) {
    var today = new Date(); today.setHours(0, 0, 0, 0);
    var end = new Date(today); end.setDate(end.getDate() + days);
    var out = [];
    for (var k = 0; k <= Math.ceil(days / 28) + 1; k++) {
      var y = today.getFullYear(), m = today.getMonth() + k;
      y += Math.floor(m / 12); m = m % 12;
      RULES.forEach(function (r) {
        if (cat && cat !== 'All' && r.cat !== cat) return;
        if (r.months && r.months.indexOf(m + 1) < 0) return;
        var d = new Date(y, m, Math.min(r.day, lastDay(y, m)));
        if (d >= today && d <= end) out.push({ date: d, rule: r });
      });
    }
    out.sort(function (a, b) { return a.date - b.date; });
    return out;
  }

  function daysLeft(d) {
    var t = new Date(); t.setHours(0, 0, 0, 0);
    var n = Math.round((d - t) / 86400000);
    return n === 0 ? 'Due today' : n === 1 ? 'Tomorrow' : 'In ' + n + ' days';
  }

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function render(el, items) {
    if (!items.length) { el.innerHTML = '<p class="cal-empty">No statutory due dates in this window.</p>'; return; }
    el.innerHTML = items.map(function (it) {
      var d = it.date, r = it.rule, n = Math.round((d - new Date().setHours(0,0,0,0)) / 86400000);
      return '<a class="cal-row' + (n <= 7 ? ' cal-soon' : '') + '" href="' + r.href + '">' +
        '<span class="cal-date"><b>' + d.getDate() + '</b>' + MONTHS[d.getMonth()] + ' ' + d.getFullYear() + '</span>' +
        '<span class="cal-body"><span class="cal-cat">' + esc(r.cat) + '</span><strong>' + esc(r.title) + '</strong><small>' + esc(r.who) + '</small></span>' +
        '<span class="cal-left">' + daysLeft(d) + ' →</span></a>';
    }).join('');
  }

  window.IWFCalendar = { upcoming: upcoming, render: render, RULES: RULES };

  // Auto-mount: <div data-iwf-calendar data-days="45" data-limit="6" data-filters></div>
  document.querySelectorAll('[data-iwf-calendar]').forEach(function (host) {
    var days = +host.getAttribute('data-days') || 60;
    var limit = +host.getAttribute('data-limit') || 0;
    var list = document.createElement('div'); list.className = 'cal-list';
    var cat = 'All';
    function draw() { var items = upcoming(days, cat); if (limit) items = items.slice(0, limit); render(list, items); }
    if (host.hasAttribute('data-filters')) {
      var bar = document.createElement('div'); bar.className = 'chip-row';
      ['All', 'GST', 'Income Tax', 'MCA', 'Payroll'].forEach(function (c) {
        var b = document.createElement('button'); b.type = 'button'; b.className = 'chip' + (c === 'All' ? ' on' : ''); b.textContent = c;
        b.addEventListener('click', function () { cat = c; bar.querySelectorAll('.chip').forEach(function (x) { x.classList.toggle('on', x === b); }); draw(); });
        bar.appendChild(b);
      });
      host.appendChild(bar);
    }
    host.appendChild(list);
    draw();
  });
})();
