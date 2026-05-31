# IndiaWiseFiling CRM

A complete lead-management backend + admin dashboard for the IndiaWiseFiling website. Captures leads from your site, moves them through a sales pipeline, logs every interaction, links payments, and sends WhatsApp + email notifications.

Built with Node.js + Express + SQLite (via sql.js — no native compilation, deploys anywhere).

---

## What's inside

```
iwf-crm/
├── src/
│   ├── server.js     ← all API routes + boot
│   ├── db.js         ← SQLite layer (auto-persists to data/crm.db)
│   ├── auth.js       ← JWT login + role checks
│   └── notify.js     ← WhatsApp + email senders
├── public/
│   └── index.html    ← the admin dashboard (single-page app)
├── data/             ← database file lives here (auto-created)
├── seed.js           ← optional: fills demo leads to explore the UI
├── .env.example      ← copy to .env and configure
└── package.json
```

---

## Quick start (local)

```bash
# 1. Install dependencies
npm install

# 2. Set up config
cp .env.example .env
# open .env and change JWT_SECRET, ADMIN_EMAIL, ADMIN_PASSWORD

# 3. (Optional) load demo leads to see the dashboard in action
npm run seed

# 4. Start the server
npm start
```

Then open **http://localhost:4000** and log in with the ADMIN_EMAIL / ADMIN_PASSWORD from your `.env`.

---

## The dashboard

- **Pipeline view** — kanban board, 7 stages: New → Contacted → Quoted → Paid → In Progress → Completed (+ Lost)
- **All Leads view** — sortable table with status badges
- **Stats banner** — total leads, today, this week, pipeline value, won revenue
- **Lead drawer** (click any lead) — change status, set deal value, send WhatsApp/email, log calls/notes, see full activity timeline
- **Search & filter** — by name/phone/email and by source
- **Export CSV** — one click, all leads

---

## Connecting your website

Your existing `indiawisefiling.html` should POST leads to the CRM. Add this to any form (or the Razorpay flow):

```javascript
await fetch('https://your-crm-url.com/api/leads/capture', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name:    'Customer Name',
    phone:   '9876543210',     // required
    email:   'customer@email.com',
    service: 'Company Registration',
    message: 'What they typed',
    source:  'website'
  })
});
```

That's it — the lead appears in your CRM instantly, your team gets an email alert, and the customer gets a WhatsApp welcome (once providers are configured).

### Linking payments
When you create a Razorpay order, pass the `lead_id` so payment auto-updates the lead to "Paid":

```javascript
// create order with lead linkage
fetch('/api/orders/create', { method:'POST', headers:{'Content-Type':'application/json'},
  body: JSON.stringify({ plan:'Growth', lead_id: 42 }) });

// after payment success, verify (auto-marks lead paid)
fetch('/api/orders/verify', { method:'POST', headers:{'Content-Type':'application/json'},
  body: JSON.stringify({ razorpay_order_id, razorpay_payment_id, razorpay_signature }) });
```

---

## Notifications

Both channels work in "log-only" mode out of the box (messages print to console), so you can build before signing up for providers. To send for real, fill the relevant `.env` vars.

**Email** — any SMTP provider (Zoho Mail and Amazon SES are cheap for India). Set `SMTP_HOST`, `SMTP_USER`, `SMTP_PASS`.

**WhatsApp** — two providers supported:
- `WHATSAPP_PROVIDER=meta` → Meta WhatsApp Cloud API (set `WHATSAPP_PHONE_ID`, `WHATSAPP_TOKEN`)
- `WHATSAPP_PROVIDER=wati` → WATI (set `WATI_ENDPOINT`, `WATI_TOKEN`)

Notifications fire automatically on: new lead (team alert + customer welcome), and status changes to contacted/quoted/paid/in_progress/completed (customer update).

---

## API reference

All `/api` routes except `/auth/login`, `/leads/capture`, `/orders/*`, and `/health` require a `Authorization: Bearer <token>` header.

| Method | Route | Purpose |
|--------|-------|---------|
| POST | `/api/auth/login` | Get a token |
| POST | `/api/leads/capture` | **Public** — website submits a lead |
| GET | `/api/leads` | List/filter leads (`?status=&search=&source=&page=`) |
| GET | `/api/leads/:id` | One lead + timeline + orders |
| PATCH | `/api/leads/:id/status` | Change status (notifies customer) |
| PATCH | `/api/leads/:id` | Update fields (assign, value, etc.) |
| POST | `/api/leads/:id/activities` | Add note / log call |
| POST | `/api/leads/:id/message` | Send WhatsApp/email to lead |
| GET | `/api/stats` | Dashboard metrics |
| POST | `/api/orders/create` | Create Razorpay order |
| POST | `/api/orders/verify` | Verify payment, mark lead paid |
| GET | `/api/leads-export.csv` | Download all leads |
| POST | `/api/users` | Add team member (admin only) |
| GET | `/api/users` | List team |

---

## Deploying to production

### Railway (easiest, ~₹500/mo)
1. Push this folder to a private GitHub repo
2. railway.app → New Project → Deploy from GitHub
3. Add all your `.env` variables in Railway's Variables tab
4. Railway auto-detects Node and runs `npm start`
5. Add a persistent volume mounted at `/app/data` so the database survives restarts

### Render (has free tier)
Same idea. **Important:** add a persistent disk mounted at `data/`, otherwise the SQLite file resets on each deploy.

### Important production notes
- Set a strong `JWT_SECRET` (random 32+ chars)
- Change `ADMIN_PASSWORD` immediately
- Restrict `CORS_ORIGINS` to your real domain
- The `data/crm.db` file is your entire database — **back it up regularly** (a daily copy to S3/Google Drive is enough at this stage)

---

## Scaling later

SQLite via sql.js comfortably handles tens of thousands of leads. When you outgrow it (multiple team members writing simultaneously, 100k+ leads), migrate to PostgreSQL:
1. The SQL schema in `db.js` is standard — it ports to Postgres with minimal changes
2. Swap the `db.js` layer for `pg` (node-postgres)
3. The rest of the app (routes, auth, dashboard) stays identical

---

## Security checklist before go-live

- [ ] `JWT_SECRET` changed to a long random value
- [ ] `ADMIN_PASSWORD` changed from default
- [ ] `.env` is in `.gitignore` (it is) and never committed
- [ ] `CORS_ORIGINS` limited to your domain
- [ ] HTTPS enabled (Railway/Render do this automatically)
- [ ] Database file backed up regularly
- [ ] Add rate-limiting on `/api/leads/capture` to prevent spam (use `express-rate-limit`)
- [ ] Add a CAPTCHA on the website form (reCAPTCHA / Cloudflare Turnstile)
