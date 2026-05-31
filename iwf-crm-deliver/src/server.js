/**
 * IndiaWiseFiling CRM — main server
 * Leads, pipeline, activities, orders, notifications + admin dashboard.
 */
const express = require('express');
const cors = require('cors');
const crypto = require('crypto');
require('dotenv').config();

const db = require('./db');
const auth = require('./auth');
const notify = require('./notify');

const app = express();
app.use(express.json());
app.use(cors({ origin: (process.env.CORS_ORIGINS || '*').split(',') }));
app.use(express.static(require('path').join(__dirname, '..', 'public')));

const STATUSES = ['new', 'contacted', 'quoted', 'paid', 'in_progress', 'completed', 'lost'];

// Helper: log an activity row
function logActivity(leadId, userId, type, content, meta = null) {
  db.run(
    'INSERT INTO activities (lead_id, user_id, type, content, meta) VALUES (?, ?, ?, ?, ?)',
    [leadId, userId, type, content, meta ? JSON.stringify(meta) : null]
  );
}

// ============================================================
// AUTH ROUTES
// ============================================================
app.post('/api/auth/login', (req, res) => {
  const { email, password } = req.body;
  const user = db.get('SELECT * FROM users WHERE email = ?', [email]);
  if (!user || !auth.verifyPassword(password, user.password_hash)) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  res.json({ token: auth.signToken(user), user: { id: user.id, name: user.name, email: user.email, role: user.role } });
});

// Create a team member (admin only)
app.post('/api/users', auth.requireAuth, auth.requireAdmin, (req, res) => {
  const { name, email, password, role } = req.body;
  if (!name || !email || !password) return res.status(400).json({ error: 'Missing fields' });
  try {
    const { lastInsertId } = db.run(
      'INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)',
      [name, email, auth.hashPassword(password), role === 'admin' ? 'admin' : 'agent']
    );
    res.json({ id: lastInsertId, name, email, role });
  } catch (err) {
    res.status(400).json({ error: 'Email already exists' });
  }
});

app.get('/api/users', auth.requireAuth, (req, res) => {
  res.json(db.all('SELECT id, name, email, role, created_at FROM users ORDER BY id'));
});

// ============================================================
// PUBLIC: capture a lead from the website (no auth)
// ============================================================
app.post('/api/leads/capture', async (req, res) => {
  const { name, phone, email, service, message, source, utm } = req.body;
  if (!name || !phone) return res.status(400).json({ error: 'Name and phone are required' });

  const { lastInsertId } = db.run(
    `INSERT INTO leads (name, email, phone, service, message, source, utm)
     VALUES (?, ?, ?, ?, ?, ?, ?)`,
    [name, email || null, phone, service || null, message || null, source || 'website', utm ? JSON.stringify(utm) : null]
  );

  const lead = db.get('SELECT * FROM leads WHERE id = ?', [lastInsertId]);
  logActivity(lastInsertId, null, 'note', 'Lead captured from ' + (source || 'website'));

  // Fire notifications (non-blocking)
  const teamEmail = process.env.TEAM_EMAIL;
  const t = notify.templates.newLeadToTeam(lead);
  notify.sendEmail(teamEmail, t.subject, t.html);
  notify.sendWhatsApp(lead.phone, notify.templates.welcomeToLead(lead));

  res.json({ ok: true, lead_id: lastInsertId });
});

// ============================================================
// LEADS (auth required)
// ============================================================
// List with filters: ?status=new&assigned_to=2&search=ravi&page=1
app.get('/api/leads', auth.requireAuth, (req, res) => {
  const { status, assigned_to, search, source } = req.query;
  const page = Math.max(1, parseInt(req.query.page || '1', 10));
  const limit = Math.min(100, parseInt(req.query.limit || '50', 10));
  const offset = (page - 1) * limit;

  let where = [], params = [];
  if (status) { where.push('l.status = ?'); params.push(status); }
  if (assigned_to) { where.push('l.assigned_to = ?'); params.push(assigned_to); }
  if (source) { where.push('l.source = ?'); params.push(source); }
  if (search) {
    where.push('(l.name LIKE ? OR l.phone LIKE ? OR l.email LIKE ?)');
    const s = '%' + search + '%';
    params.push(s, s, s);
  }
  const whereSql = where.length ? 'WHERE ' + where.join(' AND ') : '';

  const total = db.get(`SELECT COUNT(*) AS c FROM leads l ${whereSql}`, params).c;
  const rows = db.all(
    `SELECT l.*, u.name AS assigned_name
     FROM leads l LEFT JOIN users u ON u.id = l.assigned_to
     ${whereSql}
     ORDER BY l.updated_at DESC
     LIMIT ? OFFSET ?`,
    [...params, limit, offset]
  );
  res.json({ total, page, limit, leads: rows });
});

// Single lead with full activity timeline
app.get('/api/leads/:id', auth.requireAuth, (req, res) => {
  const lead = db.get('SELECT * FROM leads WHERE id = ?', [req.params.id]);
  if (!lead) return res.status(404).json({ error: 'Lead not found' });
  lead.activities = db.all(
    `SELECT a.*, u.name AS user_name FROM activities a
     LEFT JOIN users u ON u.id = a.user_id
     WHERE a.lead_id = ? ORDER BY a.created_at DESC`,
    [req.params.id]
  );
  lead.orders = db.all('SELECT * FROM orders WHERE lead_id = ? ORDER BY created_at DESC', [req.params.id]);
  res.json(lead);
});

// Update status (triggers notification)
app.patch('/api/leads/:id/status', auth.requireAuth, async (req, res) => {
  const { status } = req.body;
  if (!STATUSES.includes(status)) return res.status(400).json({ error: 'Invalid status' });
  const lead = db.get('SELECT * FROM leads WHERE id = ?', [req.params.id]);
  if (!lead) return res.status(404).json({ error: 'Lead not found' });

  db.run('UPDATE leads SET status = ?, updated_at = datetime(\'now\') WHERE id = ?', [status, req.params.id]);
  logActivity(req.params.id, req.user.id, 'status_change', `Status: ${lead.status} → ${status}`);

  // Notify the customer on key transitions
  const msg = notify.templates.statusUpdate(lead, status);
  if (msg) notify.sendWhatsApp(lead.phone, msg);

  res.json({ ok: true, status });
});

// Update lead fields (assign, value, service, etc.)
app.patch('/api/leads/:id', auth.requireAuth, (req, res) => {
  const allowed = ['name', 'email', 'phone', 'service', 'value', 'assigned_to', 'message', 'source'];
  const sets = [], params = [];
  for (const key of allowed) {
    if (key in req.body) { sets.push(`${key} = ?`); params.push(req.body[key]); }
  }
  if (!sets.length) return res.status(400).json({ error: 'Nothing to update' });
  sets.push("updated_at = datetime('now')");
  params.push(req.params.id);
  db.run(`UPDATE leads SET ${sets.join(', ')} WHERE id = ?`, params);

  if ('assigned_to' in req.body) {
    const u = db.get('SELECT name FROM users WHERE id = ?', [req.body.assigned_to]);
    logActivity(req.params.id, req.user.id, 'note', `Assigned to ${u?.name || 'someone'}`);
  }
  res.json(db.get('SELECT * FROM leads WHERE id = ?', [req.params.id]));
});

// Add a note / call log / etc.
app.post('/api/leads/:id/activities', auth.requireAuth, (req, res) => {
  const { type, content, meta } = req.body;
  const validTypes = ['note', 'call', 'email', 'whatsapp'];
  if (!validTypes.includes(type)) return res.status(400).json({ error: 'Invalid activity type' });
  logActivity(req.params.id, req.user.id, type, content, meta);
  db.run("UPDATE leads SET updated_at = datetime('now') WHERE id = ?", [req.params.id]);
  res.json({ ok: true });
});

// Send a manual WhatsApp/email to the lead from the CRM
app.post('/api/leads/:id/message', auth.requireAuth, async (req, res) => {
  const { channel, content, subject } = req.body;
  const lead = db.get('SELECT * FROM leads WHERE id = ?', [req.params.id]);
  if (!lead) return res.status(404).json({ error: 'Lead not found' });
  let result;
  if (channel === 'email') {
    result = await notify.sendEmail(lead.email, subject || 'IndiaWiseFiling', content);
  } else {
    result = await notify.sendWhatsApp(lead.phone, content);
  }
  logActivity(req.params.id, req.user.id, channel, content);
  res.json({ ok: true, result });
});

// ============================================================
// PIPELINE / DASHBOARD STATS
// ============================================================
app.get('/api/stats', auth.requireAuth, (req, res) => {
  const byStatus = {};
  STATUSES.forEach(s => { byStatus[s] = 0; });
  db.all('SELECT status, COUNT(*) AS c FROM leads GROUP BY status')
    .forEach(r => { byStatus[r.status] = r.c; });

  const total = db.get('SELECT COUNT(*) AS c FROM leads').c;
  const wonValue = db.get("SELECT COALESCE(SUM(value),0) AS v FROM leads WHERE status IN ('paid','in_progress','completed')").v;
  const pipelineValue = db.get("SELECT COALESCE(SUM(value),0) AS v FROM leads WHERE status IN ('quoted')").v;
  const today = db.get("SELECT COUNT(*) AS c FROM leads WHERE date(created_at) = date('now')").c;
  const thisWeek = db.get("SELECT COUNT(*) AS c FROM leads WHERE created_at >= datetime('now','-7 days')").c;

  res.json({ total, byStatus, wonValue, pipelineValue, today, thisWeek, statuses: STATUSES });
});

// ============================================================
// ORDERS / RAZORPAY VERIFICATION (links payment → lead)
// ============================================================
const PRICE_CATALOG = {
  'Starter': 1499, 'Growth': 7999, 'Scale': 24999,
  'company-registration': 7999, 'gst-registration': 1499,
  'itr-individual': 999, 'itr-business': 2499, 'trademark': 4999,
  'llp-registration': 5999, 'mca-annual': 9999, 'fssai': 1999, 'udyam': 999
};

app.post('/api/orders/create', async (req, res) => {
  const { plan, lead_id } = req.body;
  const amount = PRICE_CATALOG[plan];
  if (!amount) return res.status(400).json({ error: 'Invalid plan' });

  // If Razorpay keys exist, create a real order; else return a mock for dev
  let order_id = 'order_mock_' + Date.now();
  if (process.env.RAZORPAY_KEY_ID && process.env.RAZORPAY_KEY_SECRET) {
    try {
      const Razorpay = require('razorpay');
      const rzp = new Razorpay({ key_id: process.env.RAZORPAY_KEY_ID, key_secret: process.env.RAZORPAY_KEY_SECRET });
      const order = await rzp.orders.create({ amount: amount * 100, currency: 'INR', receipt: 'iwf_' + Date.now() });
      order_id = order.id;
    } catch (err) {
      return res.status(500).json({ error: 'Razorpay order failed: ' + err.message });
    }
  }

  db.run('INSERT INTO orders (lead_id, razorpay_order_id, plan, amount, status) VALUES (?, ?, ?, ?, ?)',
    [lead_id || null, order_id, plan, amount, 'created']);
  res.json({ order_id, amount: amount * 100, currency: 'INR' });
});

app.post('/api/orders/verify', (req, res) => {
  const { razorpay_order_id, razorpay_payment_id, razorpay_signature } = req.body;
  const secret = process.env.RAZORPAY_KEY_SECRET;

  // Verify signature if we have a secret (skip in pure-dev mode)
  if (secret && razorpay_signature) {
    const expected = crypto.createHmac('sha256', secret)
      .update(razorpay_order_id + '|' + razorpay_payment_id).digest('hex');
    if (expected !== razorpay_signature) {
      return res.status(400).json({ verified: false, error: 'Invalid signature' });
    }
  }

  db.run("UPDATE orders SET razorpay_payment_id = ?, status = 'paid' WHERE razorpay_order_id = ?",
    [razorpay_payment_id, razorpay_order_id]);
  const order = db.get('SELECT * FROM orders WHERE razorpay_order_id = ?', [razorpay_order_id]);

  if (order?.lead_id) {
    db.run("UPDATE leads SET status = 'paid', value = ?, updated_at = datetime('now') WHERE id = ?",
      [order.amount, order.lead_id]);
    logActivity(order.lead_id, null, 'payment', `Payment received: ₹${order.amount} (${order.plan})`,
      { payment_id: razorpay_payment_id });
    const lead = db.get('SELECT * FROM leads WHERE id = ?', [order.lead_id]);
    if (lead) notify.sendWhatsApp(lead.phone, notify.templates.statusUpdate(lead, 'paid'));
  }
  res.json({ verified: true });
});

// ============================================================
// CSV export of leads (admin)
// ============================================================
app.get('/api/leads-export.csv', auth.requireAuth, (req, res) => {
  const rows = db.all('SELECT id, name, phone, email, service, status, value, source, created_at FROM leads ORDER BY id');
  const header = 'id,name,phone,email,service,status,value,source,created_at\n';
  const csv = header + rows.map(r =>
    [r.id, r.name, r.phone, r.email, r.service, r.status, r.value, r.source, r.created_at]
      .map(v => `"${String(v ?? '').replace(/"/g, '""')}"`).join(',')
  ).join('\n');
  res.header('Content-Type', 'text/csv');
  res.attachment('leads.csv');
  res.send(csv);
});

// Health
app.get('/api/health', (req, res) => res.json({ ok: true, time: new Date().toISOString() }));

// ============================================================
// BOOT
// ============================================================
async function start() {
  await db.init();
  auth.ensureSeedAdmin();
  const PORT = process.env.PORT || 4000;
  app.listen(PORT, () => {
    console.log(`\n  IndiaWiseFiling CRM running on http://localhost:${PORT}`);
    console.log(`  Dashboard: http://localhost:${PORT}/`);
    console.log(`  API health: http://localhost:${PORT}/api/health\n`);
  });
}
start();
