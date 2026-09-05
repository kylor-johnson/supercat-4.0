# Understanding Image Errors in SuperCat - Complete Guide

**Status:** ✅ Validated and Ready for Publication  
**Created by:** Kyla Bosch  
**Category:** Images  
**Last Validated:** January 7, 2026  
**Article ID:** 41623

---

## Overview

When working with product images in SuperCat, you may encounter several types of image-related issues:

1. **Missing Images Report errors** - Two main error types that appear in the "Missing Images from Server" report
2. **Import warnings and errors** - Issues that appear during image import, including:
   - Color space warnings (CMYK vs sRGB)
   - Invalid filename errors
   - Image limit exceeded warnings
   - Image processing errors

This guide explains what these errors mean and how to resolve them.

---

## Common Image Errors

### Error Type 1: "product record doesn't specify an image file name"

**What This Error Means:**

This error occurs when:

- The product record exists in the database
- The product's images field is empty or blank
- The system expects the product to have image information but finds none

**Root Cause:**

The product was imported or created without any image filename data in the ImageFileName field of the CSV file.

**How to Identify:**

- Check the Missing Images report - this error will appear in the "Message" column
- Review your product file (CSV) for that item number
- Verify the ImageFileName column has a value for that item

**How to Fix:**

1. **Check the CSV file** - ensure the ImageFileName column has a value for that item
2. **Add image filename** to the product record in your CSV
3. **Upload the corresponding image file** to FTP (if it exists)
4. **Re-import the product** with proper image data
5. **Verify the image file exists** on the server after upload

**Example Fix:**

In your CSV file, the ImageFileName column should contain:

```csv
ItemNumber,ImageFileName,Description,...
0900-6015,0900-6015.jpg,Product Description,...
```

---

### Error Type 2: "missing image: [filename]"

**What This Error Means:**

This error occurs when:

- The product record exists in the database
- The product's images field contains a filename (e.g., "0100-0133_1.jpg")
- The actual image file does NOT exist on the server
- The system expects the image file to be present but cannot find it

**Root Cause:**

The product record references an image file that is missing from the server. This can happen if:

- The file was never uploaded
- The file was deleted
- The file was corrupted
- There's a filename mismatch (case sensitivity, typos, etc.)

**How to Identify:**

- The Missing Images report will show the exact filename that's missing
- The product record has image filename data, but the file isn't found on the server
- Check if the file exists in your local files before uploading

**How to Fix:**

1. **Locate the image file** on your local system
2. **Verify the filename matches exactly** (case-sensitive) what's in your product file
3. **Upload the missing image** to the FTP server in your organization's image directory
4. **Wait for sync** - images are processed automatically during scheduled sync cycles
5. **Re-run the Missing Images report** to verify the issue is resolved

**Important:** Filenames are case-sensitive. "ABC123.jpg" is different from "abc123.jpg". Ensure the filename in your product file matches the uploaded file exactly.

> **Note:** During peak periods (e.g., market season), image processing may take longer than usual due to high system load. If images aren't appearing after 30-45 minutes, wait an additional hour before contacting support.

---

### Error Type 3: Color Space Warning (CMYK vs sRGB)

**What This Warning Means:**

This warning appears during image import when:

- An image file is uploaded successfully
- The image is not in the sRGB color space (often CMYK instead)
- Colors may appear incorrect (dull, gray, or shifted) when displayed on iPad or web

**Root Cause:**

Some vendors supply print-ready images in **CMYK** color space. SuperCat's platform and virtually all web/iOS displays expect **sRGB** color space. When CMYK files are processed for screen display, colors can shift (often toward gray) and may not match what you expect.

**Symptoms:**

- Imported images look dull or gray
- Colors don't match what's expected on iPad/web
- Warning message appears in import logs: "The image [filename] is not in the sRGB colorspace. This may lead to colors appearing incorrect on the iPad."

**How to Identify:**

1. **Check import logs** - Look for warnings about colorspace during image import
2. **Compare original vs processed image** - CMYK originals typically render noticeably grayer/duller on screen
3. **Inspect image metadata** - Use a tool like exiftool to check the color space:

```bash
exiftool your-image.jpg
```

Look for tags like `PhotometricInterpretation: CMYK` or `ColorMode: CMYK`

**How to Fix:**

**Best Solution:** Ask your vendor or graphic specialist to provide **sRGB** versions of all product images.

**Alternative Solution:**

Convert existing files to sRGB before upload:

1. Open the image in any standard image editor (Photoshop, GIMP, etc.)
2. Convert the color profile to sRGB
3. Export/save ensuring the embedded profile is sRGB
4. Re-upload the corrected images

**Important:** The system will still import CMYK images, but they may display incorrectly. Always use sRGB for best results on digital displays.

---

### Error Type 4: Invalid Image Filename

**What This Error Means:**

This error occurs during product import when:

- An image filename contains invalid characters
- The filename doesn't meet the system's naming requirements
- The filename is rejected and not imported

**Root Cause:**

Image filenames must follow specific rules. Invalid characters include:

- Forward slashes (`/`)
- Parentheses (`(` and `)`)
- Filenames that are only spaces (but not empty)

**Error Messages:**

- "ImageFileName: [filename] is not valid and will not be imported"
- "File name: [filename] for Image: [number] is invalid"
- "Spaces only File name for Image: [number] is invalid"

**How to Fix:**

1. **Remove invalid characters** from filenames:
   - Remove any `/` characters
   - Remove any `(` or `)` characters
   - Replace spaces-only filenames with actual names

2. **Use valid filename format:**
   - Alphanumeric characters, dashes, underscores, and dots are allowed
   - Example: `ABC123.jpg` ✅
   - Example: `ABC(123).jpg` ❌ (contains parentheses)
   - Example: `ABC/123.jpg` ❌ (contains forward slash)

3. **Re-import the product** with corrected filenames

**Example Fix:**

**Invalid:**
```csv
ItemNumber,ImageFileName
0900-6015,0900-6015(image).jpg
```

**Valid:**
```csv
ItemNumber,ImageFileName
0900-6015,0900-6015-image.jpg
```

---

### Error Type 5: Image Limit Exceeded

**What This Error Means:**

This warning occurs during product import when:

- A product has more images specified than the maximum allowed
- The system limits the number of images per product (6 or 12, depending on your organization's settings)
- Extra images beyond the limit are not imported

**Root Cause:**

SuperCat enforces a maximum number of images per product:

- **Standard limit:** 6 images per product
- **Extended limit:** 12 images per product (if enabled for your organization)

**Error Messages:**

- "[6 or 12] image limit exceeded. ImageFileName [filename1, filename2] not imported."
- "[6 or 12] image limit exceeded, image(s) ([filenames]) not imported."

**How to Identify:**

- Check import logs for the warning message
- Review your CSV file - count the number of images listed for the product
- The first 6 (or 12) images will be imported, the rest will be skipped

**How to Fix:**

1. **Prioritize your images** - Ensure the most important images are listed first in your CSV
2. **Remove excess image references** from your product file if you don't need them
3. **Contact SuperCat Support** to request the 12-image limit if you need more than 6 images per product
4. **Re-import** after making changes

**Note:** The system will import the first images up to the limit and skip the rest. No data is lost, but you'll need to decide which images are most important.

---

### Error Type 6: Image Processing Error

**What This Error Means:**

This error occurs during image import when:

- An image file fails to process or convert
- ImageMagick (the image processing tool) encounters an error
- The image file may be corrupted or in an unsupported format

**Root Cause:**

Image processing can fail due to:

- Corrupted image files
- Unsupported or invalid image format
- ImageMagick conversion failures
- File permission issues
- File size issues during processing

**Error Messages:**

- "Error processing image [filename]: [error message]"
- "convert_image failed with code [number]: [error details]"
- Files may be renamed with `.failed` extension

**How to Identify:**

1. **Check import logs** for processing error messages
2. **Look for .failed files** in your import directory
3. **Review error details** in the import log for specific failure reasons

**How to Fix:**

1. **Verify the image file** is not corrupted:
   - Try opening it in an image viewer
   - Check if the file opens correctly on your local system

2. **Re-export the image** in a supported format:
   - Use JPG, PNG, GIF, TIF, or TIFF
   - Ensure the file is properly saved (not corrupted)

3. **Check file size:**
   - **Upload limit:** Source files should be under **15 MB** before upload
   - **Processed limit:** After conversion, the system limits files to **4 MB**

4. **Re-upload the corrected image** to FTP

5. **If issues persist**, contact SuperCat Support with:
   - The filename causing the error
   - The specific error message
   - A sample of the image file (if possible)

---

### Error Type 7: XMP/Metadata Profile Issues

**What This Warning Means:**

This error can occur during image import when:

- An image file contains problematic XMP or metadata profiles
- ImageMagick encounters issues parsing image metadata
- The image may process but with warnings or failures

**Root Cause:**

Some images contain complex or malformed XMP (Extensible Metadata Platform) profiles that can cause ImageMagick processing issues. This is common with images from professional photography software or certain camera RAW exports.

**Error Messages:**

- Processing failures mentioning XMP or metadata
- Images failing without clear error messages
- ImageMagick warnings about invalid profiles

**How to Fix:**

1. **Strip metadata** using a tool like ImageOptim (Mac) or similar utility

2. **Re-export the image** from editing software without metadata embedded

3. **Use command-line tools** to strip XMP:
   ```bash
   exiftool -all= your-image.jpg
   ```
   or
   ```bash
   mogrify -strip your-image.jpg
   ```

4. **Re-upload the cleaned image** to FTP

**Note:** Stripping metadata will remove information like camera settings and copyright data. Save a backup of the original file if you need to retain this information.

---

## Troubleshooting Steps

**Step 1: Identify the Error Type**

- **No filename in product record** → "product record doesn't specify an image file name"
- **Filename exists but file missing** → "missing image: [filename]"
- **Colors look wrong after import** → Check for CMYK/sRGB color space warning in import logs
- **Filename rejected during import** → "ImageFileName: [name] is not valid" (invalid characters)
- **Too many images for product** → "[6 or 12] image limit exceeded" warning
- **Image processing fails** → "Error processing image" or file renamed to `.failed`
- **Metadata/XMP issues** → Processing failures with obscure errors

**Step 2: Check the Data Source**

- **Review the CSV file** for the problematic item number
- **Verify the ImageFileName column** has the correct value
- **Check for typos or formatting issues** in the filename
- **Ensure consistent file extensions** (e.g., `.jpg` vs `.jpeg`)

**Step 3: Verify Image Files**

- **Check if image files exist** in your local system
- **Verify filenames match exactly** (case-sensitive) between CSV and actual files
- **Confirm file formats are supported** (JPG, JPEG, PNG, GIF, TIF, TIFF)
- **Check file sizes** - source files should be under 15 MB
- **Validate filename characters** - no `/`, `(`, or `)` characters
- **Count images per product** - ensure within limit (6 or 12)
- **Test image files** - open them to verify they're not corrupted

**Step 4: Upload and Fix**

- **Upload missing image files** to FTP in the correct directory
- **Update the CSV file** with correct image filenames if needed
- **Re-import the product data** if you made CSV changes
- **Wait for sync** and re-run the report to verify

---

## Prevention Tips

**Before Importing**

1. **Verify all image files exist** and are ready to upload
2. **Check CSV file formatting** and image filename accuracy
3. **Use consistent naming conventions** for image files (e.g., `ItemNumber.jpg`, `ItemNumber_2.jpg`)
4. **Test with a small batch** before full import
5. **Validate filenames** match exactly between CSV and actual files (case-sensitive)
6. **Ensure images are in sRGB color space** - convert CMYK images before upload
7. **Check filename validity** - no `/`, `(`, or `)` characters
8. **Count images per product** - ensure within limit (6 or 12)
9. **Test image files** - open each file to verify it's not corrupted
10. **Verify file sizes** - source files should be under 15 MB

**During Import**

1. **Monitor import logs** for image-related errors
2. **Validate image file references** in the CSV
3. **Upload images before or during** product file import
4. **Check file permissions** and server accessibility

**After Import**

1. **Run the Missing Images report** to verify all images are found
2. **Test image display** in the portal or catalog
3. **Verify image URLs** are working correctly
4. **Address any errors** found in the report promptly

---

## Common Issues and Solutions

**Issue: Images not displaying in portal**

**Possible causes:**
- File permissions on the server
- Image file format not supported
- Improper file naming (special characters, spaces)
- Case sensitivity mismatch

**Solutions:**
- Verify file format is supported (JPG, PNG, GIF, TIF, TIFF)
- Ensure proper file naming (no special characters, match CSV exactly)
- Check case sensitivity matches between product file and uploaded file
- Contact support if file permissions are an issue

---

**Issue: Multiple image errors for same product**

**Possible causes:**
- CSV references images that don't exist
- Placeholder filenames in CSV that were never uploaded
- Multiple image references with typos

**Solutions:**
- Review CSV file structure for consistency
- Remove placeholder image references if you don't plan to upload them
- Check for encoding issues in the CSV
- Verify all referenced files exist before importing

---

**Issue: Case sensitivity errors**

**Problem:** Product file references "ABC123.jpg" but file uploaded as "abc123.jpg"

**Solution:** Either:
- Rename the image file to match the product file exactly (case-sensitive)
- Update the product file to match the uploaded filename exactly

---

**Issue: Import fails with image errors**

**Solutions:**
- Fix image references in the CSV file first
- Upload missing image files to the server
- Re-run the import after corrections
- Check import logs for specific error messages

---

**Issue: Images look dull or gray after import**

**Problem:** Images imported successfully but colors appear washed out, gray, or don't match the original

**Possible cause:** Image is in CMYK color space instead of sRGB

**Solutions:**
- Check import logs for color space warnings
- Verify image color space using metadata tools (exiftool)
- Convert images to sRGB before uploading
- Request sRGB versions from your vendor/photographer

---

**Issue: Image filenames rejected during import**

**Problem:** Import logs show "ImageFileName: [name] is not valid and will not be imported"

**Possible causes:**
- Filename contains invalid characters (`/`, `(`, `)`)
- Filename is only spaces

**Solutions:**
- Remove invalid characters from filenames
- Use alphanumeric characters, dashes, underscores, and dots only
- Rename files and update CSV accordingly
- Re-import after corrections

---

**Issue: Some images not imported (limit exceeded)**

**Problem:** Product has 8 images listed but only 6 were imported

**Possible cause:** Image limit exceeded (standard is 6 per product, 12 if enabled)

**Solutions:**
- Prioritize images - list most important ones first
- Remove excess image references if not needed
- Contact support to enable 12-image limit if needed
- Note: First 6 (or 12) images will be imported, rest are skipped

---

**Issue: Image processing fails with .failed extension**

**Problem:** Image files are renamed to `.failed` extension and not processed

**Possible causes:**
- Corrupted image file
- Unsupported format or invalid image data
- ImageMagick conversion error
- XMP/metadata profile issues

**Solutions:**
- Verify image opens correctly in image viewer
- Re-export image in supported format (JPG, PNG, GIF, TIF, TIFF)
- Check file is not corrupted
- Ensure file size is under 15 MB (source) / 4 MB (processed)
- Strip metadata if XMP issues suspected
- Re-upload corrected image

---

## Best Practices

**Image File Management**

1. **Use descriptive filenames** that match item numbers (e.g., `0900-6015.jpg`)
2. **Maintain consistent file formats** (prefer JPG for photos)
3. **Follow naming patterns** for multiple images (e.g., `SKU.jpg`, `SKU_2.jpg`, `SKU_3.jpg`)
4. **Keep image files organized** and backed up
5. **Verify file sizes** - source files should be under 15 MB before uploading
6. **Always use sRGB color space** - convert CMYK images before upload to ensure accurate colors on digital displays
7. **Avoid invalid characters** in filenames - no `/`, `(`, or `)` characters
8. **Respect image limits** - maximum 6 images per product (or 12 if enabled)
9. **Test files before upload** - verify images open correctly and aren't corrupted

**CSV Import Process**

1. **Validate CSV data** before importing
2. **Test with sample data** first
3. **Monitor import progress** and error logs
4. **Verify results** after import completion
5. **Upload images before or during** product import

**Ongoing Maintenance**

1. **Regular image audits** using the Missing Images report
2. **Monitor file storage** and cleanup orphaned files (see [Orphan Images Report](https://supercatsolutions.com/knowledgebase/orphan-images-report))
3. **Update image references** when files change
4. **Document image management** procedures for your team
5. **Establish naming conventions** and stick to them

---

## Related Knowledge Base Articles

- [Import Product Photo](https://supercatsolutions.com/knowledgebase/import-product-photo) - Detailed image specifications and upload instructions
- [Missing Images Report](https://supercatsolutions.com/knowledgebase/missing-images-report) - How to run and interpret missing image reports
- [Orphan Images Report](https://supercatsolutions.com/knowledgebase/orphan-images-report) - Managing unused image files
- [Image Rotation Issues](https://supercatsolutions.com/knowledgebase/image-rotation-issues) - Fixing images that display sideways

---

## Getting Help

If you continue to experience image-related issues:

1. **Check the Missing Images report** for specific error details and item numbers
2. **Review import logs** for additional error information
3. **Verify file names match exactly** (case-sensitive) between CSV and uploaded files
4. **Contact SuperCat Support** with:
   - Specific error messages from the report
   - Item numbers affected
   - Example filenames that are causing issues
   - Screenshot of the Missing Images report (if possible)

---

## Summary

Understanding these image error types will help you:

- **Quickly identify** the root cause of image issues
- **Apply the correct fix** for each error type
- **Prevent similar issues** in future imports
- **Maintain clean image data** in your SuperCat system

**Key Takeaways:**

**Missing Images Report Errors:**

- **"product record doesn't specify an image file name"** = Data structure issue (missing filename in CSV/product record)
- **"missing image: [filename]"** = File availability issue (filename exists in product record but file not on server)

**Import Warnings/Errors:**

- **Color space warning (CMYK vs sRGB)** = Color profile issue (image will import but may display incorrectly)
- **"ImageFileName: [name] is not valid"** = Invalid filename characters (remove `/`, `(`, `)`)
- **"[6 or 12] image limit exceeded"** = Too many images per product (prioritize or remove excess)
- **"Error processing image"** = Image processing/conversion failure (file may be corrupted)
- **XMP/Metadata issues** = Strip problematic metadata from images

**Each requires a different solution:**

1. Fix the CSV data (add missing filename)
2. Upload the missing file (file not found on server)
3. Convert to sRGB color space (color profile issue)
4. Remove invalid characters from filename
5. Reduce number of images or prioritize them
6. Fix corrupted image file or re-export in supported format
7. Strip metadata for XMP/profile issues

---

*Last updated: January 7, 2026*  
*Validated against: SuperCat codebase, Craft CMS KB, BigQuery Help Scout data*

