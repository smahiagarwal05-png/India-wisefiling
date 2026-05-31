/**
 * Auth — JWT-based. Protects the CRM API and dashboard.
 */
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const db = require('./db');

const JWT_SECRET = process.env.JWT_SECRET || 'CHANGE_ME_IN_PRODUCTION';

function hashPassword(plain) {
  return bcrypt.hashSync(plain, 10);
}

function verifyPassword(plain, hash) {
  return bcrypt.compareSync(plain, hash);
}

function signToken(user) {
  return jwt.sign(
    { id: user.id, email: user.email, role: user.role, name: user.name },
    JWT_SECRET,
    { expiresIn: '7d' }
  );
}

/** Express middleware: require a valid token. */
function requireAuth(req, res, next) {
  const header = req.headers.authorization || '';
  const token = header.startsWith('Bearer ') ? header.slice(7) : null;
  if (!token) return res.status(401).json({ error: 'Not authenticated' });
  try {
    req.user = jwt.verify(token, JWT_SECRET);
    next();
  } catch {
    return res.status(401).json({ error: 'Invalid or expired token' });
  }
}

/** Express middleware: require admin role. */
function requireAdmin(req, res, next) {
  if (req.user?.role !== 'admin') {
    return res.status(403).json({ error: 'Admin access required' });
  }
  next();
}

/** Create the first admin if no users exist. */
function ensureSeedAdmin() {
  const count = db.get('SELECT COUNT(*) AS c FROM users');
  if (count.c === 0) {
    const email = process.env.ADMIN_EMAIL || 'admin@indiawisefiling.com';
    const password = process.env.ADMIN_PASSWORD || 'changeme123';
    db.run(
      'INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)',
      ['Admin', email, hashPassword(password), 'admin']
    );
    console.log(`\n  Seed admin created:\n    email: ${email}\n    password: ${password}\n  (change this immediately via env vars)\n`);
  }
}

module.exports = {
  hashPassword, verifyPassword, signToken,
  requireAuth, requireAdmin, ensureSeedAdmin
};
