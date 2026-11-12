/* IndiaWiseFilings shared behaviour: mega-menu, mobile drawer, lead modal, WhatsApp button. */
(function () {
  var WHATSAPP = '919319179754';
  var WHATSAPP_LABEL = '+91 93191 79754';
  var API = location.origin + '/api';

  /* ---- desktop mega-menu: hover via CSS, click/keyboard via .iwf-open ---- */
  var megas = document.querySelectorAll('.iwf-has-mega');
  function closeAll(except) {
    megas.forEach(function (li) {
      if (li !== except) {
        li.classList.remove('iwf-open');
        var b = li.querySelector('.iwf-trigger');
        if (b) b.setAttribute('aria-expanded', 'false');
      }
    });
  }
  megas.forEach(function (li) {
    var btn = li.querySelector('.iwf-trigger');
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = !li.classList.contains('iwf-open');
      closeAll(li);
      li.classList.toggle('iwf-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    li.addEventListener('mouseleave', function () {
      li.classList.remove('iwf-open');
      btn.setAttribute('aria-expanded', 'false');
    });
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.iwf-has-mega')) closeAll(null);
  });

  /* ---- mobile drawer ---- */
  var drawer = document.querySelector('.iwf-drawer');
  function openDrawer() { if (!drawer) return; drawer.classList.add('iwf-show'); document.body.style.overflow = 'hidden'; }
  function closeDrawer() { if (!drawer) return; drawer.classList.remove('iwf-show'); document.body.style.overflow = ''; }
  document.querySelectorAll('.iwf-burger').forEach(function (b) { b.addEventListener('click', openDrawer); });
  if (drawer) {
    drawer.addEventListener('click', function (e) {
      if (e.target === drawer || e.target.closest('.iwf-drawer-close')) closeDrawer();
    });
  }


  /* ---- header search ---- */
  var sp = document.querySelector('.iwf-search');
  if (sp) {
    var items = []; try { items = JSON.parse(sp.getAttribute('data-items') || '[]'); } catch (e) {}
    var sin = sp.querySelector('.iwf-search-input'), sres = sp.querySelector('.iwf-search-results');
    function sesc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
    function sdraw() {
      var q = sin.value.trim().toLowerCase(), words = q.split(/\s+/).filter(Boolean);
      var hits = !q ? items.filter(function (i) { return /Private Limited|New GST|Trademark Registration|Salaried|ROC Annual|Udyam|FSSAI Registration|UAE Company/.test(i[0]); })
        : items.filter(function (i) { var s = (i[0] + ' ' + i[2]).toLowerCase(); return words.every(function (w) { return s.indexOf(w) > -1; }); });
      sres.innerHTML = hits.length ? hits.slice(0, 12).map(function (i, k) { return '<a href="' + sesc(i[1]) + '"' + (k === 0 && q ? ' class="iwf-active"' : '') + '>' + sesc(i[0]) + '<span>' + sesc(i[2]) + '</span></a>'; }).join('')
        : '<p>No match. <a href="/contact.html" data-lead="' + sesc(sin.value) + '" style="color:var(--saffron-deep)">Ask an advisor about "' + sesc(sin.value) + '"</a></p>';
    }
    function sopen() { sp.classList.add('iwf-show'); closeAll(null); sdraw(); setTimeout(function () { sin.focus(); }, 30); }
    function sclose() { sp.classList.remove('iwf-show'); }
    document.querySelectorAll('.iwf-search-btn').forEach(function (b) { b.addEventListener('click', function (e) { e.stopPropagation(); sp.classList.contains('iwf-show') ? sclose() : sopen(); }); });
    sp.querySelector('.iwf-search-close').addEventListener('click', sclose);
    sin.addEventListener('input', sdraw);
    sin.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') sclose();
      if (e.key === 'Enter') { var a = sres.querySelector('a'); if (a) { e.preventDefault(); location.href = a.getAttribute('href'); } }
    });
    document.addEventListener('click', function (e) { if (!e.target.closest('.iwf-search') && !e.target.closest('.iwf-search-btn')) sclose(); });
  }

  /* ---- lead modal: reuse the page's own if it has one, otherwise inject ours ---- */
  if (typeof window.openLeadModal !== 'function') {
    var wrap = document.createElement('div');
    wrap.innerHTML =
      '<div class="iwf-modal-bg" id="iwfModalBg">' +
      ' <div class="iwf-modal" role="dialog" aria-modal="true" aria-labelledby="iwfModalTitle">' +
      '  <div class="iwf-modal-head">' +
      '   <button class="iwf-modal-x" type="button" aria-label="Close">×</button>' +
      '   <h3 id="iwfModalTitle">Talk to an <em>advisor</em></h3>' +
      '   <p>Share a few details and we will WhatsApp you with pricing, documents needed and timelines.</p>' +
      '   <span class="iwf-modal-svc" id="iwfModalSvc">General enquiry</span>' +
      '  </div>' +
      '  <form id="iwfModalForm" novalidate>' +
      '   <label for="iwf-name">Your name</label><input id="iwf-name" name="name" type="text" required placeholder="e.g. Ravi Kumar">' +
      '   <label for="iwf-phone">Phone (with WhatsApp)</label><input id="iwf-phone" name="phone" type="tel" required placeholder="9876543210">' +
      '   <label for="iwf-email">Email (optional)</label><input id="iwf-email" name="email" type="email" placeholder="you@email.com">' +
      '   <label for="iwf-message">Anything to add? (optional)</label><textarea id="iwf-message" name="message" placeholder="State, budget, urgency, etc."></textarea>' +
      '   <button type="submit">Send my details →</button>' +
      '   <div class="iwf-msg" id="iwfModalMsg"></div>' +
      '   <p class="iwf-alt">Or WhatsApp us at <a href="https://wa.me/' + WHATSAPP + '" target="_blank" rel="noopener">' + WHATSAPP_LABEL + '</a></p>' +
      '  </form>' +
      ' </div>' +
      '</div>';
    document.body.appendChild(wrap.firstChild);
    var bg = document.getElementById('iwfModalBg');
    var svc = document.getElementById('iwfModalSvc');
    var form = document.getElementById('iwfModalForm');
    var msg = document.getElementById('iwfModalMsg');
    window.openLeadModal = function (service) {
      svc.textContent = service || 'General enquiry';
      msg.className = 'iwf-msg'; msg.textContent = '';
      bg.classList.add('iwf-show');
      document.body.style.overflow = 'hidden';
      setTimeout(function () { document.getElementById('iwf-name').focus(); }, 80);
    };
    window.closeLeadModal = function () { bg.classList.remove('iwf-show'); document.body.style.overflow = ''; };
    bg.addEventListener('click', function (e) { if (e.target === bg || e.target.closest('.iwf-modal-x')) window.closeLeadModal(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { window.closeLeadModal(); closeDrawer(); } });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      window.iwfSubmitLead({
        name: form.name.value, phone: form.phone.value, email: form.email.value,
        message: form.message.value, service: svc.textContent, source: 'site-modal:' + location.pathname
      }, msg, form.querySelector('button[type=submit]')).then(function (ok) {
        if (ok) { form.reset(); setTimeout(window.closeLeadModal, 2200); }
      });
    });
  }

  /* ---- shared lead submit helper, used by the modal and by page forms ---- */
  window.iwfSubmitLead = function (data, msgEl, btn) {
    function show(kind, text) { if (msgEl) { msgEl.className = 'iwf-msg ' + (kind === 'ok' ? 'iwf-ok' : 'iwf-err'); msgEl.textContent = text; } }
    var name = (data.name || '').trim(), phone = (data.phone || '').replace(/\D/g, '').slice(-10);
    if (!name || !phone) { show('err', 'Name and phone are required.'); return Promise.resolve(false); }
    if (!/^[6-9][0-9]{9}$/.test(phone)) { show('err', 'Please enter a valid 10-digit Indian mobile number.'); return Promise.resolve(false); }
    var orig = btn ? btn.textContent : '';
    if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }
    return fetch(API + '/leads/capture', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: name, phone: phone, email: (data.email || '').trim() || null,
        service: data.service || 'General enquiry', message: (data.message || '').trim() || null,
        source: data.source || location.pathname
      })
    }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) { if (!d.ok) throw new Error('capture'); show('ok', '✓ Got it! An advisor will WhatsApp you shortly.'); return true; })
      .catch(function () { show('err', 'Something went wrong. Please WhatsApp us at ' + WHATSAPP_LABEL + '.'); return false; })
      .finally(function () { if (btn) { btn.disabled = false; btn.textContent = orig; } });
  };

  /* ---- [data-lead] opens the modal; [data-iwf-start] jumps to the page form if there is one ---- */
  document.addEventListener('click', function (e) {
    var a = e.target.closest('[data-lead],[data-iwf-start]');
    if (!a) return;
    if (a.hasAttribute('data-iwf-start')) {
      var target = document.getElementById('start');
      if (target) { e.preventDefault(); closeDrawer(); target.scrollIntoView({ behavior: 'smooth' }); return; }
    }
    e.preventDefault();
    closeDrawer();
    window.openLeadModal(a.getAttribute('data-lead') || 'General enquiry');
  });

  /* ---- floating WhatsApp button ---- */
  if (!document.querySelector('.iwf-wa')) {
    var wa = document.createElement('a');
    wa.className = 'iwf-wa';
    wa.href = 'https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent('Hi, I need help with ');
    wa.target = '_blank'; wa.rel = 'noopener';
    wa.setAttribute('aria-label', 'Chat on WhatsApp');
    wa.innerHTML = '<svg viewBox="0 0 32 32" fill="#fff"><path d="M16 3C9 3 3.3 8.6 3.3 15.6c0 2.2.6 4.4 1.7 6.3L3 29l7.3-1.9c1.8 1 3.9 1.5 5.9 1.5 7 0 12.7-5.7 12.7-12.6S23 3 16 3zm0 23.1c-1.9 0-3.8-.5-5.4-1.5l-.4-.2-4.3 1.1 1.2-4.2-.3-.4c-1.1-1.7-1.6-3.6-1.6-5.6C5.2 9.8 10 5.1 16 5.1s10.7 4.7 10.7 10.5S21.9 26.1 16 26.1zm5.9-7.9c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2-.2.3-.8 1-1 1.2-.2.2-.4.2-.7.1-.3-.2-1.4-.5-2.6-1.6-1-.9-1.6-1.9-1.8-2.2-.2-.3 0-.5.1-.7l.5-.6c.2-.2.2-.4.3-.6.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.2 1.4 3.5c.2.2 2.4 3.6 5.7 5 .8.3 1.4.5 1.9.7.8.3 1.6.2 2.2.1.7-.1 1.9-.8 2.2-1.5.3-.8.3-1.4.2-1.5-.1-.2-.3-.3-.6-.4z"/></svg>';
    document.body.appendChild(wa);
  }
})();
