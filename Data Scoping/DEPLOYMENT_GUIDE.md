# 🚀 DEPLOYMENT GUIDE — Data Readiness Questionnaire

## What You're Deploying

| File | What It Does |
|------|-------------|
| `index.html` | The questionnaire prospects fill out |
| `admin.html` | Where your team generates unique links per prospect |
| `Google_Apps_Script.js` | The backend that saves responses to Google Sheets |

---

## STEP 1: Set Up Google Sheets (5 min)

1. Go to **[sheets.google.com](https://sheets.google.com)** → Create new spreadsheet
2. Name it **"Data Readiness Submissions"**
3. Rename the first tab (bottom of screen) to **"Drafts"**
4. Add a second tab → name it **"Submissions"**

**In the "Drafts" tab**, paste these headers across Row 1:
```
Company Slug | Last Saved | Contact Name | Email | Phone | Q1 | Q1 Notes | Q2 | Q2 Notes | Q3 | Q3 Notes | Q4 | Q4 Notes | Q5 | Q5 Notes | Q6 | Q6 Notes | Q7 | Q7 Notes | Q8 | Q8 Notes | Files | Submitted
```

**In the "Submissions" tab**, paste these headers across Row 1:
```
Company Slug | Submitted At | Contact Name | Email | Phone | Q1 | Q1 Notes | Q2 | Q2 Notes | Q3 | Q3 Notes | Q4 | Q4 Notes | Q5 | Q5 Notes | Q6 | Q6 Notes | Q7 | Q7 Notes | Q8 | Q8 Notes | Files
```

---

## STEP 2: Deploy the Apps Script (3 min)

1. In the same spreadsheet, go to **Extensions → Apps Script**
2. Delete everything in the editor
3. Paste the **entire contents** of `Google_Apps_Script.js`
4. **Optional**: On the line that says `var NOTIFY_EMAIL = '';` — add your team email to get notified on submissions
5. Hit **Save** (Ctrl+S / Cmd+S)
6. Click **Deploy → New deployment**
7. Click the ⚙️ gear → select **Web app**
8. Set:
   - Description: `Questionnaire webhook`
   - Execute as: **Me**
   - Who has access: **Anyone**
9. Click **Deploy** → **Authorize access** → choose your Google account → Allow
10. **Copy the Web app URL** — you'll need it in the next step

> ⚠️ The URL looks like: `https://script.google.com/macros/s/ABCDEF.../exec`

---

## STEP 3: Add the URL to Your HTML (1 min)

Open `index.html` and find this line near the top of the `<script>` block:

```javascript
var GOOGLE_SCRIPT_URL = 'YOUR_GOOGLE_APPS_SCRIPT_URL_HERE';
```

Replace `YOUR_GOOGLE_APPS_SCRIPT_URL_HERE` with the URL you copied. Keep the quotes.

---

## STEP 4: Deploy to Netlify (2 min)

1. Go to **[app.netlify.com](https://app.netlify.com)** → Sign up or log in (free)
2. From the dashboard, look for **"Deploy manually"** or drag-and-drop area
3. Create a folder on your computer called `supercat-data` and put these 2 files in it:
   - `index.html`
   - `admin.html`
4. **Drag the entire folder** onto Netlify
5. It deploys in ~10 seconds → you get a URL like `random-name-123.netlify.app`
6. Click **Site configuration → Change site name** → set it to something like `supercat-data`
   - Your URL becomes: `supercat-data.netlify.app`

**Optional: Custom domain**
- In Netlify, go to **Domain settings → Add custom domain**
- Follow their instructions to point e.g. `data.supercat.com` to your Netlify site

---

## STEP 5: Update the Admin Page Base URL (30 sec)

Open `admin.html` and find this line:

```javascript
var BASE_URL = window.location.origin + '/';
```

This auto-detects your domain, so **if you deploy both files to the same Netlify site, you don't need to change anything**. But if you want to hardcode it:

```javascript
var BASE_URL = 'https://supercat-data.netlify.app/';
```

---

## HOW IT WORKS

### For Sales:
1. Go to `supercat-data.netlify.app/admin.html`
2. Type the prospect company name → click Generate
3. Copy the link → send it to the prospect (email, Slack, whatever)

### For the Prospect:
1. They open the link → land directly on the questionnaire
2. They answer questions at their own pace — **progress auto-saves**
3. They can close the tab, come back later, share the link with a colleague — everything is saved
4. When done, they hit **Submit**

### For Your Team:
1. Responses appear in the Google Sheet in real-time
2. "Drafts" tab shows in-progress questionnaires
3. "Submissions" tab shows completed ones
4. Optional email notification fires on each submission

---

## REDEPLOYING AFTER CHANGES

If you edit `index.html` or `admin.html`:
1. Go to Netlify dashboard → your site → **Deploys**
2. Drag the updated folder again → new version is live in seconds

If you edit the Apps Script:
1. Go to Apps Script editor → make changes → Save
2. Click **Deploy → Manage deployments → Edit (pencil icon) → Version: New version → Deploy**

---

## TROUBLESHOOTING

**"Missing Link" error when opening questionnaire**
→ The URL needs `?c=company-slug` at the end. Use the admin page to generate proper links.

**Submissions not appearing in Google Sheets**
→ Check that the URL in `index.html` matches your deployed Apps Script URL exactly (including `/exec` at the end).

**CORS errors in browser console**
→ The fetch uses `mode: 'no-cors'` which should handle this. If you see issues, make sure the Apps Script is deployed with "Who has access: Anyone".
