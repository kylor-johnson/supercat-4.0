// ============================================================
// SUPERCAT DATA READINESS — Google Apps Script
// ============================================================
// 
// SETUP (takes ~5 minutes):
//
// 1. Create a new Google Sheet → name it "Data Readiness Submissions"
//
// 2. Create TWO tabs (sheets) at the bottom:
//    - Rename "Sheet1" to "Drafts"
//    - Click the "+" to add a new tab, name it "Submissions"
//
// 3. In the "Drafts" tab, Row 1 headers (A through V):
//    Company Slug | Last Saved | Contact Name | Email | Phone | Q1 | Q1 Notes | Q2 | Q2 Notes | Q3 | Q3 Notes | Q4 | Q4 Notes | Q5 | Q5 Notes | Q6 | Q6 Notes | Q7 | Q7 Notes | Q8 | Q8 Notes | Files
//
// 4. In the "Submissions" tab, Row 1 headers (same columns + Submitted At):
//    Company Slug | Submitted At | Contact Name | Email | Phone | Q1 | Q1 Notes | Q2 | Q2 Notes | Q3 | Q3 Notes | Q4 | Q4 Notes | Q5 | Q5 Notes | Q6 | Q6 Notes | Q7 | Q7 Notes | Q8 | Q8 Notes | Files
//
// 5. Go to Extensions → Apps Script
// 6. Delete everything → paste this entire file → Save (Ctrl+S)
// 7. Click Deploy → New deployment
//    - Type: Web app
//    - Execute as: Me
//    - Who has access: Anyone
// 8. Click Deploy → Authorize → Copy the URL
// 9. Paste the URL into BOTH files:
//    - index.html → line that says GOOGLE_SCRIPT_URL = '...'
//    - (That's it — admin.html doesn't need it)
//
// OPTIONAL: Set your notification email on line 26 below.
// ============================================================

var NOTIFY_EMAIL = '';  // e.g. 'team@supercat.com' — leave empty to skip notifications


// ============================================================
// POST handler — receives drafts and submissions
// ============================================================
function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var action = data._action || 'draft';
    var slug = data._company || 'unknown';

    if (action === 'submit') {
      // --- Final submission ---
      var subSheet = ss.getSheetByName('Submissions');
      if (!subSheet) {
        subSheet = ss.insertSheet('Submissions');
        subSheet.appendRow(['Company Slug','Submitted At','Contact Name','Email','Phone','Q1','Q1 Notes','Q2','Q2 Notes','Q3','Q3 Notes','Q4','Q4 Notes','Q5','Q5 Notes','Q6','Q6 Notes','Q7','Q7 Notes','Q8','Q8 Notes','Files']);
      }

      subSheet.appendRow([
        slug,
        new Date().toLocaleString('en-US', { timeZone: 'America/Denver' }),
        data.contact_name || '',
        data.contact_email || '',
        data.contact_phone || '',
        data.q1 || '', data.q1_notes || '',
        data.q2 || '', data.q2_notes || '',
        data.q3 || '', data.q3_notes || '',
        data.q4 || '', data.q4_notes || '',
        data.q5 || '', data.q5_notes || '',
        data.q6 || '', data.q6_notes || '',
        data.q7 || '', data.q7_notes || '',
        data.q8 || '', data.q8_notes || '',
        data._files || ''
      ]);

      // Mark draft as submitted
      markDraftSubmitted(ss, slug);

      // Send notification
      if (NOTIFY_EMAIL) {
        var displayName = slug.replace(/-/g, ' ').replace(/\b\w/g, function(l) { return l.toUpperCase(); });
        MailApp.sendEmail({
          to: NOTIFY_EMAIL,
          subject: '✅ Data Readiness Submitted: ' + displayName,
          body: 'New submission from ' + displayName + '\n' +
                'Contact: ' + (data.contact_name || 'Not provided') + ' (' + (data.contact_email || 'no email') + ')\n\n' +
                'View responses: ' + ss.getUrl()
        });
      }

      return ContentService.createTextOutput(JSON.stringify({ status: 'ok' })).setMimeType(ContentService.MimeType.JSON);

    } else {
      // --- Draft save (auto-save) ---
      var draftSheet = ss.getSheetByName('Drafts');
      if (!draftSheet) {
        draftSheet = ss.insertSheet('Drafts');
        draftSheet.appendRow(['Company Slug','Last Saved','Contact Name','Email','Phone','Q1','Q1 Notes','Q2','Q2 Notes','Q3','Q3 Notes','Q4','Q4 Notes','Q5','Q5 Notes','Q6','Q6 Notes','Q7','Q7 Notes','Q8','Q8 Notes','Files','Submitted']);
      }

      var rowData = [
        slug,
        new Date().toLocaleString('en-US', { timeZone: 'America/Denver' }),
        data.contact_name || '',
        data.contact_email || '',
        data.contact_phone || '',
        data.q1 || '', data.q1_notes || '',
        data.q2 || '', data.q2_notes || '',
        data.q3 || '', data.q3_notes || '',
        data.q4 || '', data.q4_notes || '',
        data.q5 || '', data.q5_notes || '',
        data.q6 || '', data.q6_notes || '',
        data.q7 || '', data.q7_notes || '',
        data.q8 || '', data.q8_notes || '',
        data._files || '',
        ''  // Submitted flag (empty for drafts)
      ];

      // Upsert: find existing row for this company or create new one
      var existingRow = findRowBySlug(draftSheet, slug);
      if (existingRow > 0) {
        // Update existing row
        var range = draftSheet.getRange(existingRow, 1, 1, rowData.length);
        range.setValues([rowData]);
      } else {
        draftSheet.appendRow(rowData);
      }

      return ContentService.createTextOutput(JSON.stringify({ status: 'ok' })).setMimeType(ContentService.MimeType.JSON);
    }

  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ status: 'error', message: err.toString() })).setMimeType(ContentService.MimeType.JSON);
  }
}


// ============================================================
// GET handler — loads existing draft for a company
// ============================================================
function doGet(e) {
  try {
    var action = (e.parameter && e.parameter.action) || '';
    var slug = (e.parameter && e.parameter.c) || '';

    if (action === 'load' && slug) {
      var ss = SpreadsheetApp.getActiveSpreadsheet();
      var draftSheet = ss.getSheetByName('Drafts');

      if (!draftSheet) {
        return jsonResponse({ status: 'ok', draft: null });
      }

      var row = findRowBySlug(draftSheet, slug);
      if (row <= 0) {
        return jsonResponse({ status: 'ok', draft: null });
      }

      var values = draftSheet.getRange(row, 1, 1, 23).getValues()[0];
      var draft = {
        _company: values[0],
        _saved_at: values[1],
        contact_name: values[2],
        contact_email: values[3],
        contact_phone: values[4],
        q1: values[5],  q1_notes: values[6],
        q2: values[7],  q2_notes: values[8],
        q3: values[9],  q3_notes: values[10],
        q4: values[11], q4_notes: values[12],
        q5: values[13], q5_notes: values[14],
        q6: values[15], q6_notes: values[16],
        q7: values[17], q7_notes: values[18],
        q8: values[19], q8_notes: values[20],
        _files: values[21],
        _submitted: values[22] === 'YES'
      };

      return jsonResponse({ status: 'ok', draft: draft });
    }

    // Default: health check
    return ContentService.createTextOutput('Supercat Data Readiness webhook is live.').setMimeType(ContentService.MimeType.TEXT);

  } catch (err) {
    return jsonResponse({ status: 'error', message: err.toString() });
  }
}


// ============================================================
// Helpers
// ============================================================

function findRowBySlug(sheet, slug) {
  var data = sheet.getDataRange().getValues();
  for (var i = 1; i < data.length; i++) {
    if (data[i][0] === slug) return i + 1;  // 1-indexed
  }
  return -1;
}

function markDraftSubmitted(ss, slug) {
  var draftSheet = ss.getSheetByName('Drafts');
  if (!draftSheet) return;
  var row = findRowBySlug(draftSheet, slug);
  if (row > 0) {
    // Column 23 = "Submitted" flag
    draftSheet.getRange(row, 23).setValue('YES');
  }
}

function jsonResponse(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
