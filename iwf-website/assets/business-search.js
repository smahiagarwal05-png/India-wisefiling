/* Business Search: validates and decodes GSTIN, PAN, CIN, LLPIN, DIN and Udyam numbers client-side.
   Nothing is sent to any server. Format checks only: status must be confirmed on official portals. */
(function () {
  var STATES = {
    '01': 'Jammu & Kashmir', '02': 'Himachal Pradesh', '03': 'Punjab', '04': 'Chandigarh', '05': 'Uttarakhand', '06': 'Haryana',
    '07': 'Delhi', '08': 'Rajasthan', '09': 'Uttar Pradesh', '10': 'Bihar', '11': 'Sikkim', '12': 'Arunachal Pradesh', '13': 'Nagaland',
    '14': 'Manipur', '15': 'Mizoram', '16': 'Tripura', '17': 'Meghalaya', '18': 'Assam', '19': 'West Bengal', '20': 'Jharkhand',
    '21': 'Odisha', '22': 'Chhattisgarh', '23': 'Madhya Pradesh', '24': 'Gujarat', '25': 'Daman & Diu (legacy)', '26': 'Dadra & Nagar Haveli and Daman & Diu',
    '27': 'Maharashtra', '28': 'Andhra Pradesh (legacy)', '29': 'Karnataka', '30': 'Goa', '31': 'Lakshadweep', '32': 'Kerala', '33': 'Tamil Nadu',
    '34': 'Puducherry', '35': 'Andaman & Nicobar Islands', '36': 'Telangana', '37': 'Andhra Pradesh', '38': 'Ladakh', '97': 'Other Territory', '99': 'Centre Jurisdiction'
  };
  var ROC_STATES = {
    AN: 'Andaman & Nicobar', AP: 'Andhra Pradesh', AR: 'Arunachal Pradesh', AS: 'Assam', BR: 'Bihar', CH: 'Chandigarh', CT: 'Chhattisgarh', CG: 'Chhattisgarh',
    DN: 'Dadra & Nagar Haveli', DD: 'Daman & Diu', DL: 'Delhi', GA: 'Goa', GJ: 'Gujarat', HR: 'Haryana', HP: 'Himachal Pradesh', JK: 'Jammu & Kashmir',
    JH: 'Jharkhand', KA: 'Karnataka', KL: 'Kerala', LA: 'Ladakh', LD: 'Lakshadweep', MP: 'Madhya Pradesh', MH: 'Maharashtra', MN: 'Manipur', ML: 'Meghalaya',
    MZ: 'Mizoram', NL: 'Nagaland', OR: 'Odisha', OD: 'Odisha', PY: 'Puducherry', PB: 'Punjab', RJ: 'Rajasthan', SK: 'Sikkim', TN: 'Tamil Nadu',
    TG: 'Telangana', TS: 'Telangana', TR: 'Tripura', UP: 'Uttar Pradesh', UR: 'Uttarakhand', UT: 'Uttarakhand', WB: 'West Bengal'
  };
  var PAN_TYPES = { P: 'Individual', C: 'Company', H: 'Hindu Undivided Family (HUF)', F: 'Firm / LLP', A: 'Association of Persons', T: 'Trust', B: 'Body of Individuals', L: 'Local Authority', J: 'Artificial Juridical Person', G: 'Government' };
  var CIN_CLASS = {
    PTC: 'Private limited company', PLC: 'Public limited company', OPC: 'One Person Company', NPL: 'Not-for-profit (Section 8) company',
    GOI: 'Company owned by the Government of India', SGC: 'State Government company', GAP: 'Public company limited by guarantee', GAT: 'Private company limited by guarantee',
    ULL: 'Public unlimited company', ULT: 'Private unlimited company', FLC: 'Financial lease company', FTC: 'Subsidiary of a foreign company'
  };
  var CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';

  function gstinCheck(g) {
    var sum = 0;
    for (var i = 0; i < 14; i++) {
      var v = CHARS.indexOf(g[i]) * (i % 2 === 0 ? 1 : 2);
      sum += Math.floor(v / 36) + (v % 36);
    }
    return CHARS[(36 - (sum % 36)) % 36];
  }

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function row(k, v) { return '<dt>' + esc(k) + '</dt><dd>' + v + '</dd>'; }
  function card(title, ok, rows, verify) {
    return '<div class="card"><span class="kicker">' + esc(title) + '</span><h3 class="' + (ok ? 'ok' : 'bad') + '">' + (ok ? '✓ Format is valid' : '✗ This does not look valid') + '</h3>' +
      '<dl class="kv" style="margin-top:1rem">' + rows.join('') + '</dl>' +
      (verify ? '<p style="margin-top:1.2rem;font-size:.88rem">Format checks cannot confirm the registration is active. <a href="' + verify[1] + '" target="_blank" rel="noopener">' + esc(verify[0]) + ' ↗</a></p>' : '') + '</div>';
  }
  function panRows(p) {
    return [row('PAN', '<code>' + esc(p) + '</code>'), row('Holder type', esc(PAN_TYPES[p[3]] || 'Unknown (' + p[3] + ')')),
      row('Name initial', esc(p[4]) + (p[3] === 'P' ? ' (first letter of surname)' : ' (first letter of the name)'))];
  }

  function decode(raw) {
    var v = raw.toUpperCase().replace(/\s+/g, '');
    if (!v) return '';
    // GSTIN
    if (v.length === 15) {
      var fmt = /^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$/.test(v);
      var exp = fmt ? gstinCheck(v) : null;
      var ok = fmt && exp === v[14] && !!STATES[v.slice(0, 2)];
      var rows = [row('GSTIN', '<code>' + esc(v) + '</code>'),
        row('State', esc(STATES[v.slice(0, 2)] || 'Unknown state code ' + v.slice(0, 2))),
        row('PAN inside', '<code>' + esc(v.slice(2, 12)) + '</code> (' + esc(PAN_TYPES[v[5]] || 'unknown type') + ')'),
        row('Registration no.', esc(v[12]) + ' for this PAN in this state'),
        row('Check digit', fmt ? (exp === v[14] ? '<span class="ok">Matches (' + esc(v[14]) + ')</span>' : '<span class="bad">Expected ' + esc(exp) + ', found ' + esc(v[14]) + '. Likely a typo.</span>') : '<span class="bad">Pattern does not match a GSTIN</span>')];
      return card('GSTIN', ok, rows, ['Confirm on the GST portal', 'https://services.gst.gov.in/services/searchtp']);
    }
    // PAN
    if (v.length === 10 && /^[A-Z]{3}/.test(v)) {
      var okp = /^[A-Z]{3}[PCHFATBLJG][A-Z][0-9]{4}[A-Z]$/.test(v);
      return card('PAN', okp, okp ? panRows(v) : [row('PAN', '<code>' + esc(v) + '</code>'), row('Expected', '5 letters, 4 digits, 1 letter, with a valid holder type as the 4th letter')], ['Verify PAN on the income tax portal', 'https://eportal.incometax.gov.in/']);
    }
    // CIN
    if (v.length === 21) {
      var m = /^([LU])([0-9]{5})([A-Z]{2})([0-9]{4})([A-Z]{3})([0-9]{6})$/.exec(v);
      if (!m) return card('CIN', false, [row('CIN', '<code>' + esc(v) + '</code>'), row('Expected', 'L/U, 5-digit industry code, 2-letter state, year, 3-letter class, 6-digit number')], null);
      var yr = +m[4], now = new Date().getFullYear();
      var okc = !!ROC_STATES[m[3]] && !!CIN_CLASS[m[5]] && yr >= 1850 && yr <= now;
      return card('Corporate Identification Number', okc, [
        row('CIN', '<code>' + esc(v) + '</code>'), row('Listing status', m[1] === 'L' ? 'Listed on a stock exchange' : 'Unlisted'),
        row('Industry (NIC) code', esc(m[2])), row('State of registration', esc(ROC_STATES[m[3]] || 'Unknown (' + m[3] + ')')),
        row('Year of incorporation', esc(m[4]) + (yr > now ? ' <span class="bad">(in the future)</span>' : '')), row('Company class', esc(CIN_CLASS[m[5]] || 'Unknown (' + m[5] + ')')),
        row('ROC registration no.', esc(m[6]))], ['Look up master data on MCA', 'https://www.mca.gov.in/']);
    }
    // LLPIN
    if (/^[A-Z]{3}-?[0-9]{4}$/.test(v)) {
      return card('LLP Identification Number', true, [row('LLPIN', '<code>' + esc(v.slice(0, 3) + '-' + v.slice(-4)) + '</code>'), row('Entity', 'Limited Liability Partnership registered with MCA')], ['Look up LLP master data on MCA', 'https://www.mca.gov.in/']);
    }
    // DIN
    if (/^[0-9]{8}$/.test(v)) {
      return card('Director Identification Number', true, [row('DIN', '<code>' + esc(v) + '</code>'), row('Note', 'DINs are 8 digits. Check KYC status before the director signs any MCA form.')], ['Check DIN status on MCA', 'https://www.mca.gov.in/']);
    }
    // Udyam
    if (/^UDYAM-?[A-Z]{2}-?[0-9]{2}-?[0-9]{7}$/.test(v)) {
      var u = v.replace(/-/g, '');
      return card('Udyam Registration Number', !!ROC_STATES[u.slice(5, 7)], [row('Udyam no.', '<code>UDYAM-' + esc(u.slice(5, 7)) + '-' + esc(u.slice(7, 9)) + '-' + esc(u.slice(9)) + '</code>'),
        row('State', esc(ROC_STATES[u.slice(5, 7)] || 'Unknown')), row('District code', esc(u.slice(7, 9)))], ['Verify on the Udyam portal', 'https://udyamregistration.gov.in/']);
    }
    return '<div class="card"><h3 class="bad">We could not recognise this number</h3><p style="margin-top:.5rem">Supported formats: GSTIN (15 characters), PAN (10), CIN (21), LLPIN (AAA-1234), DIN (8 digits) and Udyam (UDYAM-XX-00-0000000).</p></div>';
  }

  var input = document.getElementById('bsInput'), out = document.getElementById('bsResult');
  if (!input) return;
  function go() { out.innerHTML = decode(input.value); }
  document.getElementById('bsGo').addEventListener('click', go);
  input.addEventListener('keydown', function (e) { if (e.key === 'Enter') go(); });
  input.addEventListener('input', function () { if (input.value.replace(/\s/g, '').length >= 8) go(); else out.innerHTML = ''; });
  document.querySelectorAll('[data-try]').forEach(function (b) { b.addEventListener('click', function () { input.value = b.getAttribute('data-try'); go(); }); });
  window.IWFDecode = decode; window.IWFGstinCheck = gstinCheck;
})();
