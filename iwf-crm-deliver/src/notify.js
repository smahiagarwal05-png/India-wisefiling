/**
 * Notifications — Email (nodemailer) + WhatsApp (provider-agnostic).
 *
 * Both are optional: if env vars aren't set, calls are logged and skipped,
 * so the CRM keeps working before you've wired up providers.
 */
const nodemailer = require('nodemailer');

// ---------- EMAIL ----------
let mailer = null;
function getMailer() {
  if (mailer) return mailer;
  if (!process.env.SMTP_HOST) return null;
  mailer = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port: parseInt(process.env.SMTP_PORT || '587', 10),
    secure: process.env.SMTP_SECURE === 'true',
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASS
    }
  });
  return mailer;
}

async function sendEmail(to, subject, html) {
  const m = getMailer();
  if (!m || !to) {
    console.log(`[email skipped] to=${to} subject="${subject}"`);
    return { skipped: true };
  }
  try {
    await m.sendMail({
      from: process.env.SMTP_FROM || '"IndiaWiseFiling" <noreply@indiawisefiling.com>',
      to, subject, html
    });
    return { sent: true };
  } catch (err) {
    console.error('[email error]', err.message);
    return { error: err.message };
  }
}

// ---------- WHATSAPP ----------
// Works with WATI, AiSensy, or Meta Cloud API. Set WHATSAPP_PROVIDER + creds.
// Default: logs only (so you can build before wiring a provider).
async function sendWhatsApp(phone, message, templateName = null) {
  const provider = process.env.WHATSAPP_PROVIDER;
  if (!provider || !phone) {
    console.log(`[whatsapp skipped] to=${phone} msg="${message?.slice(0, 50)}..."`);
    return { skipped: true };
  }

  // Normalise Indian numbers to 91XXXXXXXXXX
  let num = String(phone).replace(/\D/g, '');
  if (num.length === 10) num = '91' + num;

  try {
    if (provider === 'meta') {
      // Meta WhatsApp Cloud API
      const res = await fetch(
        `https://graph.facebook.com/v21.0/${process.env.WHATSAPP_PHONE_ID}/messages`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${process.env.WHATSAPP_TOKEN}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            messaging_product: 'whatsapp',
            to: num,
            type: 'text',
            text: { body: message }
          })
        }
      );
      const data = await res.json();
      if (!res.ok) throw new Error(JSON.stringify(data));
      return { sent: true, data };
    }

    if (provider === 'wati') {
      // WATI API
      const res = await fetch(
        `${process.env.WATI_ENDPOINT}/api/v1/sendSessionMessage/${num}?messageText=${encodeURIComponent(message)}`,
        {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${process.env.WATI_TOKEN}` }
        }
      );
      const data = await res.json();
      if (!res.ok) throw new Error(JSON.stringify(data));
      return { sent: true, data };
    }

    console.log(`[whatsapp] unknown provider "${provider}"`);
    return { skipped: true };
  } catch (err) {
    console.error('[whatsapp error]', err.message);
    return { error: err.message };
  }
}

// ---------- READY-MADE MESSAGES ----------
const templates = {
  newLeadToTeam: (lead) => ({
    subject: `New lead: ${lead.name} — ${lead.service || 'General enquiry'}`,
    html: `
      <h2>New lead received</h2>
      <p><b>Name:</b> ${lead.name}</p>
      <p><b>Phone:</b> ${lead.phone}</p>
      <p><b>Email:</b> ${lead.email || '—'}</p>
      <p><b>Service:</b> ${lead.service || '—'}</p>
      <p><b>Message:</b> ${lead.message || '—'}</p>
      <p><b>Source:</b> ${lead.source}</p>
      <p>Log in to the CRM to assign and follow up.</p>
    `
  }),
  welcomeToLead: (lead) =>
    `Hi ${lead.name}, thanks for reaching out to IndiaWiseFiling about ${lead.service || 'our services'}! ` +
    `One of our experts will call you within 30 minutes. — Team IWF`,
  statusUpdate: (lead, status) => {
    const map = {
      contacted: `Hi ${lead.name}, our advisor has reviewed your request for ${lead.service}. We'll share next steps shortly.`,
      quoted: `Hi ${lead.name}, your quote for ${lead.service} is ready: ₹${lead.value}. Reply YES to proceed.`,
      paid: `Hi ${lead.name}, payment received! Your ${lead.service} filing has started. We'll keep you updated here.`,
      in_progress: `Hi ${lead.name}, good news — your ${lead.service} is now being processed by our team.`,
      completed: `Hi ${lead.name}, your ${lead.service} is complete! Documents are in your dashboard. Thank you for choosing IWF.`
    };
    return map[status] || null;
  }
};

module.exports = { sendEmail, sendWhatsApp, templates };
