# Move CRM to /crm path — server instructions

## What changed and why

The CRM previously served its dashboard at `/`, which meant it owned the root URL. You want the **marketing website** at `https://indiawisefilings.com/` and the **CRM** at `https://indiawisefilings.com/crm`. So:

| URL | Before | After |
|-----|--------|-------|
| `/` | CRM login screen | Free (your website serves here) |
| `/crm` | (didn't exist) | Redirects to `/crm/` |
| `/crm/` | (didn't exist) | CRM login + dashboard |
| `/api/*` | CRM API | CRM API (unchanged) |

I tested this — `GET /` returns 404, `GET /crm/` returns the dashboard, `GET /api/health` still works. The website can keep posting leads to `/api/leads/capture` exactly as planned.

## What you need to change on the server

Two files. I've attached both updated versions in your outputs.

### File 1: `src/server.js`

Open it:
```bash
nano /var/lib/iwf-crm/app/src/server.js
```

Around **lines 15–17**, you currently have:

```javascript
app.use(express.json());
app.use(cors({ origin: (process.env.CORS_ORIGINS || '*').split(',') }));
app.use(express.static(require('path').join(__dirname, '..', 'public')));
```

Replace with:

```javascript
app.use(express.json());
app.use(cors({ origin: (process.env.CORS_ORIGINS || '*').split(',') }));

// Dashboard lives at /crm (the marketing website owns the root URL).
// e.g. https://indiawisefilings.com/crm  → CRM login + dashboard
app.use('/crm', express.static(require('path').join(__dirname, '..', 'public')));
// If someone visits /crm (no trailing slash), redirect cleanly to /crm/
app.get('/crm', (req, res) => res.redirect('/crm/'));
```

Also around **line 304** (near the end), update the boot log line:

```javascript
console.log(`  Dashboard: http://localhost:${PORT}/crm/`);  // was just /
```

Save (Ctrl+O, Enter, Ctrl+X).

### File 2: `public/index.html`

Just a comment update so future-you remembers the path setup. Optional but recommended.

```bash
nano /var/lib/iwf-crm/app/public/index.html
```

Find this line (around line 225):
```javascript
const API = location.origin + '/api';
```

Replace with:
```javascript
const API = location.origin + '/api';
// The dashboard itself is served from /crm/, but the API stays at /api so
// the marketing website can also POST leads to /api/leads/capture without
// needing to know about /crm.
```

The actual code line is unchanged — the dashboard's API calls keep using `location.origin + '/api'`, which now resolves to `https://indiawisefilings.com/api` exactly as it should.

### Restart PM2

```bash
pm2 restart iwf-crm
pm2 logs iwf-crm --lines 20
```

Look for `Dashboard: http://localhost:4000/crm/` in the logs — confirms the new layout is live.

### Quick verification on the server

```bash
# Should return 404 (dashboard no longer here)
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:4000/

# Should return 200 and the dashboard HTML
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:4000/crm/

# Should return 200 and {"ok":true,...}
curl -s http://localhost:4000/api/health
```

All three should show 404, 200, and the JSON health response respectively.

---

## What's still needed (next steps)

This change alone makes the CRM live at `/crm` *internally*. To make it work at `https://indiawisefilings.com/crm`, you still need:

1. **Update Nginx** so it forwards `/crm` and `/api` to the Node app — see next section
2. **Upload your website HTML** to `/var/www/html/index.html` so `/` serves it
3. **Fix the DNS / IP mismatch** we identified earlier (`indiawisefilings.com` → `13.62.5.233`, but you're on a different EC2 server)
4. **Run certbot** for `indiawisefilings.com`

I'll guide each in order once you've done the file changes above. Confirm the curl outputs first.

---

## New Nginx config (for when you're ready)

This is the config that ties the website + CRM together on one domain. Don't apply it yet — wait until we've sorted the IP issue.

```nginx
limit_req_zone $binary_remote_addr zone=capture:10m rate=10r/m;

server {
    listen 80;
    server_name indiawisefilings.com www.indiawisefilings.com;

    # ACME challenge — for certbot
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
        default_type "text/plain";
    }

    client_max_body_size 25M;

    # CRM dashboard — forwarded to Node
    location /crm {
        proxy_pass http://127.0.0.1:4000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # CRM API — forwarded to Node, with rate-limit on the public capture endpoint
    location /api/leads/capture {
        limit_req zone=capture burst=5 nodelay;
        proxy_pass http://127.0.0.1:4000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api {
        proxy_pass http://127.0.0.1:4000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Marketing website — served as static files
    location / {
        root /var/www/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
}
```

After applying this and running certbot, the layout becomes:

- `https://indiawisefilings.com/` → your marketing website (the HTML file)
- `https://indiawisefilings.com/crm` → CRM login (redirects to `/crm/`)
- `https://indiawisefilings.com/api/leads/capture` → public lead capture (rate-limited)
- `https://indiawisefilings.com/api/*` → CRM API (auth-required for most routes)

---

## Update for `.env` and website

When everything's working, also update:

**`/var/lib/iwf-crm/app/.env`** — set CORS to the production domain:
```
CORS_ORIGINS=https://indiawisefilings.com,https://www.indiawisefilings.com
```
Then `pm2 restart iwf-crm`.

**Your website's lead-capture JavaScript** — point at the production API:
```javascript
const CRM_URL = 'https://indiawisefilings.com';
await fetch(`${CRM_URL}/api/leads/capture`, { ... });
```

Same-origin call (since the website is on `indiawisefilings.com` too), so no CORS preflight overhead.
