# Understanding Image Errors in SuperCat - Visual Enhancement Draft

**Article ID:** 41623  
**Draft Date:** January 12, 2026  
**Purpose:** Identify locations for images, screenshots, and hyperlinks to enhance the KB article

---

## Visual Enhancement Summary

This document identifies **17 locations** where images, screenshots, or enhanced links should be added to improve the article's usability.

---

## Section-by-Section Enhancement Recommendations

---

### Overview Section

**Current Content:**
> When working with product images in SuperCat, you may encounter several types of image-related issues...

**🖼️ SUGGESTED IMAGE #1: Admin Console Navigation**
- **Placement:** After the opening paragraph
- **Content:** Screenshot showing Admin Console menu with "Reports > Image Validation" highlighted
- **Source:** Admin Console UI → Tools or Reports menu
- **Why:** Users need to know WHERE to find these errors before understanding what they mean

---

### Error Type 1: "product record doesn't specify an image file name"

**Current Content:**
> **How to Identify:**
> - Check the Missing Images report - this error will appear in the "Message" column

**🖼️ SUGGESTED IMAGE #2: Missing Images Report - Error Type 1**
- **Placement:** After "How to Identify" section
- **Content:** Screenshot of the Missing Images Report showing the specific "product record doesn't specify an image file name" error message in the Message column
- **Source:** Admin Console → Reports → Missing Images from Server report
- **Annotation:** Circle/highlight the error message in the Message column

**🖼️ SUGGESTED IMAGE #3: CSV File Example - ImageFileName Column**
- **Placement:** After the "Example Fix" code block
- **Content:** Screenshot of an Excel/CSV file open with the ImageFileName column highlighted
- **Source:** Sample products.csv file in Excel
- **Why:** Visual learners need to see what a properly formatted CSV looks like

---

### Error Type 2: "missing image: [filename]"

**Current Content:**
> **How to Identify:**
> - The Missing Images report will show the exact filename that's missing

**🖼️ SUGGESTED IMAGE #4: Missing Images Report - Error Type 2**
- **Placement:** After "How to Identify" section
- **Content:** Screenshot of Missing Images Report showing the "missing image: [filename]" error
- **Source:** Admin Console → Reports → Missing Images from Server report
- **Annotation:** Highlight the specific filename shown in the error message

**🔗 SUGGESTED LINK #1: FTP Upload Instructions**
- **Current Text:** "Upload the missing image to the FTP server in your organization's image directory"
- **Enhancement:** Add hyperlink to: [How to Manage FTP Access](https://supercatsolutions.com/knowledgebase/ftp-access) (if exists)
- **Alternative:** Link to internal FTP setup guide

---

### Error Type 3: Color Space Warning (CMYK vs sRGB)

**Current Content:**
> **Symptoms:**
> - Imported images look dull or gray

**🖼️ SUGGESTED IMAGE #5: CMYK vs sRGB Comparison**
- **Placement:** After "Symptoms" section
- **Content:** Side-by-side comparison showing the same product image in CMYK (dull/gray) vs sRGB (vibrant)
- **Source:** Create using real product image - one in CMYK, one converted to sRGB
- **Why:** This is THE most common visual complaint and users need to SEE the difference

**🖼️ SUGGESTED IMAGE #6: Import Log with Color Space Warning**
- **Placement:** After "How to Identify" section
- **Content:** Screenshot of import log showing the color space warning message
- **Source:** Admin Console → File Import Status Report after uploading a CMYK image
- **Annotation:** Highlight the warning text

**🖼️ SUGGESTED IMAGE #7: exiftool Terminal Output**
- **Placement:** After the `exiftool your-image.jpg` command block
- **Content:** Screenshot of terminal showing exiftool output with ColorSpace/PhotometricInterpretation highlighted
- **Source:** Terminal running exiftool on a CMYK image
- **Annotation:** Circle the CMYK-related metadata tags

---

### Error Type 4: Invalid Image Filename

**Current Content:**
> **Error Messages:**
> - "ImageFileName: [filename] is not valid and will not be imported"

**🖼️ SUGGESTED IMAGE #8: Import Error - Invalid Filename**
- **Placement:** After "Error Messages" section
- **Content:** Screenshot of import log/error showing the invalid filename error
- **Source:** Admin Console → File Import Status Report after uploading a file with invalid characters
- **Annotation:** Highlight the specific error message

**📋 SUGGESTED VISUAL #9: Valid vs Invalid Filename Table**
- **Placement:** After the "How to Fix" section
- **Content:** Visual table/infographic showing:
  - ✅ Valid: `ABC123.jpg`, `ABC-123_2.jpg`, `0900-6015.jpg`
  - ❌ Invalid: `ABC(123).jpg`, `ABC/123.jpg`, `   .jpg` (spaces only)
- **Format:** Could be an image or styled HTML table with checkmarks/X marks

---

### Error Type 5: Image Limit Exceeded

**Current Content:**
> **Error Messages:**
> - "[6 or 12] image limit exceeded. ImageFileName [filename1, filename2] not imported."

**🖼️ SUGGESTED IMAGE #10: Import Warning - Image Limit**
- **Placement:** After "Error Messages" section
- **Content:** Screenshot of import warning showing the image limit exceeded message
- **Source:** Admin Console → File Import Status Report after uploading product with 8+ images
- **Annotation:** Highlight the warning and the specific filenames not imported

---

### Error Type 6: Image Processing Error

**Current Content:**
> **How to Identify:**
> - Look for .failed files in your import directory

**🖼️ SUGGESTED IMAGE #11: FTP Directory with .failed Files**
- **Placement:** After "How to Identify" section
- **Content:** Screenshot of FTP client showing image files with .failed extension
- **Source:** FTP directory after a failed image process
- **Why:** Users may not know what a .failed file looks like or where to find it

---

### Error Type 7: XMP/Metadata Profile Issues

**Current Content:**
> **How to Fix:**
> 1. Strip metadata using a tool like ImageOptim (Mac)

**🖼️ SUGGESTED IMAGE #12: ImageOptim Tool**
- **Placement:** After the "Strip metadata" step
- **Content:** Screenshot of ImageOptim (Mac) with an image being processed
- **Source:** ImageOptim application
- **Why:** Many users won't know what ImageOptim looks like or how to use it

---

### Troubleshooting Steps Section

**Current Content:**
> **Step 1: Identify the Error Type**
> - No filename in product record → "product record doesn't specify an image file name"

**📋 SUGGESTED VISUAL #13: Troubleshooting Flowchart**
- **Placement:** At the beginning of the Troubleshooting Steps section
- **Content:** Visual flowchart/decision tree:
  ```
  What error are you seeing?
      ↓
  "product record doesn't specify..." → Go to Error Type 1
  "missing image: [filename]" → Go to Error Type 2
  Colors look wrong → Check import logs for CMYK warning
  Filename rejected → Go to Error Type 4
  Image limit exceeded → Go to Error Type 5
  Processing fails/.failed files → Go to Error Type 6
  ```
- **Format:** Mermaid diagram or designed infographic
- **Why:** Quick visual reference for troubleshooting

---

### Prevention Tips Section

**Current Content:**
> **Before Importing:**
> 1. Verify all image files exist and are ready to upload

**📋 SUGGESTED VISUAL #14: Pre-Import Checklist**
- **Placement:** At the beginning of "Before Importing" section
- **Content:** Visual checklist graphic with checkboxes:
  - ☐ Image files exist locally
  - ☐ Filenames match CSV exactly (case-sensitive)
  - ☐ Images are in sRGB color space
  - ☐ No invalid characters in filenames
  - ☐ Max 6 images per product (or 12 if enabled)
  - ☐ Files under 15 MB
- **Format:** Designed checkbox graphic or PDF download

---

### Common Issues and Solutions Section

**Current Content:**
> **Issue: Images not displaying in portal**

**🖼️ SUGGESTED IMAGE #15: Portal Product View - Missing Image**
- **Placement:** Before the "Possible causes" list
- **Content:** Screenshot of the eCat portal showing a product with a broken/missing image placeholder
- **Source:** eCat Online catalog view with a product missing its image
- **Why:** Users need to see what the problem looks like in context

---

### Related Knowledge Base Articles Section

**Current Content:**
> - [Import Product Photo](https://supercatsolutions.com/knowledgebase/import-product-photo)
> - [Missing Images Report](https://supercatsolutions.com/knowledgebase/missing-images-report)

**🔗 SUGGESTED LINK ENHANCEMENTS:**
- **Verify all links are active and correct:**
  - ✅ Import Product Photo: https://supercatsolutions.com/knowledgebase/import-product-photo (ID: 550)
  - ✅ Missing Images Report: https://supercatsolutions.com/knowledgebase/missing-images-report (ID: 538)
  - ⚠️ Orphan Images Report: Verify URL exists
  - ⚠️ Image Rotation Issues: Verify URL exists

**📋 SUGGESTED VISUAL #16: Related Articles Card**
- **Placement:** In the Related Articles section
- **Content:** Visual card/tile format for related articles instead of plain bullet list
- **Why:** More engaging and easier to scan

---

### Getting Help Section

**Current Content:**
> - Screenshot of the Missing Images report (if possible)

**🖼️ SUGGESTED IMAGE #17: Sample Support Request Format**
- **Placement:** After the bullet list of what to include
- **Content:** Example screenshot showing a well-formatted support request with:
  - Specific error message highlighted
  - Item numbers listed
  - Filename examples
- **Why:** Users often don't know what information to include; showing a good example helps

---

## Screenshot Source Locations in Admin Console

Based on codebase and documentation analysis, here's where to capture each screenshot:

| Screenshot | Location in Admin Console | Notes |
|------------|---------------------------|-------|
| Missing Images Report | Reports → Image Validation → Missing Images from Server | Two variants: all images vs primary only |
| Orphan Images Report | Reports → Image Validation → Orphan Images | Shows unused image files |
| File Import Status Report | After any file import → View Import Status | Shows errors, warnings, success |
| Import Logs | File Status → Import History | Historical import records |
| FTP Directory | Via FTP client (FileZilla, Cyberduck) | Connect to org's image directory |
| Product View (Portal) | eCat Online catalog | Use demo/test org |
| Product View (iPad) | eCat iPad app | Use simulator or device |

---

## Hyperlink Validation Status

| Link | Current URL | Status | Notes |
|------|-------------|--------|-------|
| Import Product Photo | /knowledgebase/import-product-photo | ✅ Active (ID: 550) | Verified |
| Missing Images Report | /knowledgebase/missing-images-report | ✅ Active (ID: 538) | Verified |
| Orphan Images Report | /knowledgebase/orphan-images-report | ⚠️ Verify | Not confirmed |
| Image Rotation Issues | /knowledgebase/image-rotation-issues | ⚠️ Verify | Not confirmed |
| FTP Access Guide | Unknown | ❓ Check | May need to create |

---

## Suggested Image Specifications

For consistency with existing KB articles:

| Attribute | Specification |
|-----------|---------------|
| Format | PNG or JPG |
| Max Width | 800px (full-width), 400px (inline) |
| File Size | Under 500KB |
| Annotations | Red circles/arrows for highlights |
| Alt Text | Required for accessibility |
| Border | 1px light gray border (#E0E0E0) |

---

## Priority Ranking for Visual Additions

### High Priority (Most Impactful)
1. **Image #2** - Missing Images Report showing Error Type 1
2. **Image #4** - Missing Images Report showing Error Type 2
3. **Image #5** - CMYK vs sRGB comparison
4. **Visual #13** - Troubleshooting flowchart
5. **Image #1** - Admin Console navigation

### Medium Priority (Helpful but not critical)
6. **Image #6** - Import log with color space warning
7. **Image #10** - Image limit exceeded warning
8. **Visual #14** - Pre-import checklist
9. **Image #3** - CSV file example
10. **Visual #9** - Valid vs invalid filename table

### Lower Priority (Nice to have)
11. **Image #7** - exiftool terminal output
12. **Image #8** - Invalid filename error
13. **Image #11** - FTP .failed files
14. **Image #12** - ImageOptim tool
15. **Image #15** - Portal missing image view
16. **Visual #16** - Related articles cards
17. **Image #17** - Sample support request

---

## Next Steps

1. **Capture high-priority screenshots** from Admin Console (test org recommended)
2. **Verify/update hyperlinks** for Related Articles section
3. **Create CMYK vs sRGB comparison image** using real product image
4. **Design troubleshooting flowchart** (Mermaid or graphic design tool)
5. **Design pre-import checklist** as downloadable PDF or styled HTML
6. **Review existing KB articles** (Import Product Photo, Missing Images Report) for image style consistency

---

*This document is for review purposes only. No changes have been made to the Craft CMS article.*
