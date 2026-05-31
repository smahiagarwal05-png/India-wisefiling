/**
 * Database layer — sql.js (pure-JS SQLite, no native compilation)
 * Persists to data/crm.db on every write, with a debounced flush.
 */
const initSqlJs = require('sql.js');
const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, '..', 'data');
const DB_PATH = path.join(DATA_DIR, 'crm.db');
if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });

let db = null;
let SQL = null;
let flushTimer = null;

/** Persist the in-memory DB to disk (debounced to avoid thrashing). */
function scheduleFlush() {
  if (flushTimer) clearTimeout(flushTimer);
  flushTimer = setTimeout(flushNow, 150);
}

function flushNow() {
  if (!db) return;
  if (flushTimer) { clearTimeout(flushTimer); flushTimer = null; }
  const data = db.export();
  fs.writeFileSync(DB_PATH, Buffer.from(data));
}

/** Initialise DB: load from disk if present, else create fresh. */
async function init() {
  SQL = await initSqlJs();
  if (fs.existsSync(DB_PATH)) {
    const fileBuffer = fs.readFileSync(DB_PATH);
    db = new SQL.Database(fileBuffer);
  } else {
    db = new SQL.Database();
  }
  createSchema();
  flushNow();
  // Safety: flush on exit
  process.on('SIGINT', () => { flushNow(); process.exit(0); });
  process.on('SIGTERM', () => { flushNow(); process.exit(0); });
  return db;
}

function createSchema() {
  db.run(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      email TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL,
      role TEXT NOT NULL DEFAULT 'agent',  -- admin | agent
      created_at TEXT NOT NULL DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS leads (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      email TEXT,
      phone TEXT NOT NULL,
      service TEXT,                 -- e.g. "Company Registration"
      source TEXT DEFAULT 'website',-- website | referral | ad | whatsapp
      status TEXT NOT NULL DEFAULT 'new',
      -- new | contacted | quoted | paid | in_progress | completed | lost
      value INTEGER DEFAULT 0,      -- quoted amount in rupees
      assigned_to INTEGER,          -- users.id
      message TEXT,                 -- what the lead wrote
      utm TEXT,                     -- json blob of marketing params
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      updated_at TEXT NOT NULL DEFAULT (datetime('now')),
      FOREIGN KEY (assigned_to) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS activities (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      lead_id INTEGER NOT NULL,
      user_id INTEGER,
      type TEXT NOT NULL,           -- note | status_change | call | email | whatsapp | payment
      content TEXT,
      meta TEXT,                    -- json
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      FOREIGN KEY (lead_id) REFERENCES leads(id)
    );

    CREATE TABLE IF NOT EXISTS orders (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      lead_id INTEGER,
      razorpay_order_id TEXT,
      razorpay_payment_id TEXT,
      plan TEXT,
      amount INTEGER,               -- rupees
      status TEXT DEFAULT 'created',-- created | paid | failed | refunded
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      FOREIGN KEY (lead_id) REFERENCES leads(id)
    );

    CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
    CREATE INDEX IF NOT EXISTS idx_leads_phone ON leads(phone);
    CREATE INDEX IF NOT EXISTS idx_activities_lead ON activities(lead_id);
  `);
  scheduleFlush();
}

/** Run a write query with params. Returns { lastInsertId, changes }. */
function run(sql, params = []) {
  const stmt = db.prepare(sql);
  stmt.bind(params);
  stmt.step();
  stmt.free();
  const idRes = db.exec('SELECT last_insert_rowid() AS id');
  const lastInsertId = idRes.length ? idRes[0].values[0][0] : null;
  scheduleFlush();
  return { lastInsertId };
}

/** Get a single row as an object, or null. */
function get(sql, params = []) {
  const stmt = db.prepare(sql);
  stmt.bind(params);
  let row = null;
  if (stmt.step()) row = stmt.getAsObject();
  stmt.free();
  return row;
}

/** Get all rows as an array of objects. */
function all(sql, params = []) {
  const stmt = db.prepare(sql);
  stmt.bind(params);
  const rows = [];
  while (stmt.step()) rows.push(stmt.getAsObject());
  stmt.free();
  return rows;
}

module.exports = { init, run, get, all, flushNow };
