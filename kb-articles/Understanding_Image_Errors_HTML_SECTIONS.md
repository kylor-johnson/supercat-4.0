# Understanding Image Errors - HTML Content for Craft CMS

**Instructions:** Copy each section's HTML below and paste into the corresponding Body field in Craft admin using **Source mode** (click the `</>` button).

---

## Section 1: Overview (Section ID: 41640)

```html
<h2>Overview</h2>
<p>When working with product images in SuperCat, you may encounter several types of image-related issues. Understanding these error types will help you quickly identify the root cause of image issues, apply the correct fix, and prevent similar issues in future imports.</p>

<p><strong>There are 7 common image error types:</strong></p>

<table>
<thead>
<tr><th>Error Type</th><th>What It Means</th><th>Quick Fix</th></tr>
</thead>
<tbody>
<tr><td>1. Product record does not specify an image file name</td><td>The 'ImageFileName' field in your CSV is empty</td><td>Add filename to CSV</td></tr>
<tr><td>2. Missing image: [filename]</td><td>File referenced in CSV does not exist on server</td><td>Upload the missing file to FTP</td></tr>
<tr><td>3. Color Space Warning (CMYK vs sRGB)</td><td>Image is in CMYK color space, may appear dull/gray</td><td>Convert to sRGB before uploading</td></tr>
<tr><td>4. Invalid Image Filename</td><td>Filename contains invalid characters (/, (, ))</td><td>Remove invalid characters</td></tr>
<tr><td>5. Image Limit Exceeded</td><td>Product has more than 6 (or 12) images</td><td>Reduce images or request higher limit</td></tr>
<tr><td>6. Image Processing Error</td><td>File is corrupted or in unsupported format</td><td>Re-export in supported format</td></tr>
<tr><td>7. XMP/Metadata Profile Issues</td><td>Problematic metadata causing processing failures</td><td>Strip metadata from image</td></tr>
</tbody>
</table>

<p>Each error type is explained in detail below with step-by-step resolution instructions.</p>
```

---

## Section 2: Error Type 1 (Section ID: 41701)

```html
<h2>Error Type 1: Product Record Does Not Specify an Image File Name</h2>

<p><strong>What This Error Means:</strong> This error occurs when the product record exists in the database but the 'ImageFileName' field is empty or blank. The system expects the product to have image information but finds none.</p>

<p><strong>Root Cause:</strong> The product was imported or created without any image filename data in the 'ImageFileName' field of your CSV file.</p>

<p><strong>How to Identify:</strong></p>
<ul>
<li>Check the Missing Images report - this error appears in the Message column</li>
<li>Review your product file (CSV) for that item number</li>
<li>Verify the 'ImageFileName' column has a value for that item</li>
</ul>

<p><strong>How to Fix:</strong></p>
<ol>
<li>Open your product CSV and locate the item number. Ensure the 'ImageFileName' column has a value.</li>
<li>Add the correct image filename to the product record in your CSV (e.g., '0900-6015.jpg').</li>
<li>Upload the corresponding image file to FTP if it does not already exist on the server.</li>
<li>Re-import the product file with the corrected image data.</li>
<li>Run the Missing Images report again to confirm the error is resolved.</li>
</ol>

<blockquote><strong>Note:</strong> The 'ImageFileName' column should contain the exact filename matching the uploaded file.</blockquote>
```

---

## Section 3: Error Type 2 (Section ID: 41702)

```html
<h2>Error Type 2: Missing Image [filename]</h2>

<p><strong>What This Error Means:</strong> This error occurs when the product record contains a filename in the 'ImageFileName' field, but the actual image file does NOT exist on the server.</p>

<p><strong>Root Cause:</strong> The product record references an image file that is missing from the server. This can happen if the file was never uploaded, was deleted, was corrupted during upload, or there is a filename mismatch (case sensitivity, typos).</p>

<p><strong>How to Identify:</strong></p>
<ul>
<li>The Missing Images report shows the exact filename that is missing</li>
<li>The product record has image filename data, but the file is not found on the server</li>
</ul>

<p><strong>How to Fix:</strong></p>
<ol>
<li>Locate the image file on your local system.</li>
<li>Verify the filename matches exactly (case-sensitive) what is in your product file. Remember: 'ABC123.jpg' is different from 'abc123.jpg'.</li>
<li>Upload the missing image to the FTP server in your organization image directory.</li>
<li>Wait for sync - images are processed automatically during scheduled sync cycles.</li>
<li>Re-run the Missing Images report to verify the issue is resolved.</li>
</ol>

<blockquote><strong>Important:</strong> Filenames are case-sensitive. Ensure the filename in your product file matches the uploaded file exactly.</blockquote>

<blockquote><strong>Note:</strong> During peak periods (e.g., market season), image processing may take longer. If images are not appearing after 30-45 minutes, wait an additional hour before contacting support.</blockquote>
```

---

## Section 4: Error Type 3 (Section ID: 41641)

```html
<h2>Error Type 3: Color Space Warning (CMYK vs sRGB)</h2>

<p><strong>What This Warning Means:</strong> This warning appears during image import when an image is not in the sRGB color space. Images in CMYK color space may appear dull, gray, or washed out when displayed on iPad or web.</p>

<p><strong>Root Cause:</strong> Some vendors supply print-ready images in CMYK color space. SuperCat and virtually all web/iOS displays expect sRGB color space. When CMYK files are processed for screen display, colors can shift (often toward gray).</p>

<p><strong>Symptoms:</strong></p>
<ul>
<li>Imported images look dull or gray</li>
<li>Colors do not match what you expect on iPad/web</li>
<li>Warning message in import logs: 'The image [filename] is not in the sRGB colorspace'</li>
</ul>

<p><strong>How to Fix:</strong></p>
<ol>
<li><strong>Best option:</strong> Ask your vendor or graphic specialist to provide sRGB versions of all product images.</li>
<li><strong>Alternative:</strong> Convert existing files to sRGB before upload using any standard image editor (Photoshop, GIMP, etc.) - convert the color profile to sRGB, export ensuring the embedded profile is sRGB, then re-upload.</li>
</ol>

<blockquote><strong>Important:</strong> The system will still import CMYK images, but they may display incorrectly. Always use sRGB for best results on digital displays.</blockquote>
```

---

## Section 5: Error Type 4 (Section ID: 41703)

```html
<h2>Error Type 4: Invalid Image Filename</h2>

<p><strong>What This Error Means:</strong> This error occurs during product import when an image filename contains invalid characters or does not meet system naming requirements.</p>

<p><strong>Root Cause:</strong> Image filenames must follow specific rules. Invalid characters include forward slashes (/), parentheses ((and)), and filenames that are only spaces.</p>

<p><strong>Error Messages:</strong></p>
<ul>
<li>'ImageFileName: [filename] is not valid and will not be imported'</li>
<li>'File name: [filename] for Image: [number] is invalid'</li>
</ul>

<p><strong>How to Fix:</strong></p>
<ol>
<li>Remove any /, (, or ) characters from your filenames. Replace spaces-only filenames with actual names.</li>
<li>Use valid characters: alphanumeric, dashes, underscores, and dots. Example: 'ABC123.jpg' or 'ABC-123_main.jpg'.</li>
<li>Update your CSV with corrected filenames and re-import the product file.</li>
</ol>
```

---

## Section 6: Error Type 5 (Section ID: 41642)

```html
<h2>Error Type 5: Image Limit Exceeded</h2>

<p><strong>What This Warning Means:</strong> This warning occurs during product import when a product has more images specified than the maximum allowed. Extra images beyond the limit are not imported.</p>

<p><strong>Root Cause:</strong> SuperCat enforces a maximum number of images per product: 6 images (standard) or 12 images (if extended limit is enabled for your organization).</p>

<p><strong>Error Message:</strong> '[6 or 12] image limit exceeded. ImageFileName [filename1, filename2] not imported.'</p>

<p><strong>How to Fix:</strong></p>
<ol>
<li>Prioritize your images - ensure the most important images are listed first in your CSV. The system imports the first images up to the limit.</li>
<li>Remove excess image references from your product file if you do not need all of them.</li>
<li>If you need more than 6 images per product, <a href="mailto:support@supercatsolutions.com">Contact Support</a> to request the 12-image limit.</li>
</ol>

<blockquote><strong>Note:</strong> No data is lost - the first 6 (or 12) images are imported, and the rest are skipped.</blockquote>
```

---

## Section 7: Error Type 6 (Section ID: 41643)

```html
<h2>Error Type 6: Image Processing Error</h2>

<p><strong>What This Error Means:</strong> This error occurs during image import when an image file fails to process or convert. The file may be corrupted or in an unsupported format.</p>

<p><strong>Root Cause:</strong> Image processing can fail due to corrupted image files, unsupported or invalid image format, ImageMagick conversion failures, file permission issues, or file size issues.</p>

<p><strong>Error Messages:</strong></p>
<ul>
<li>'Error processing image [filename]: [error message]'</li>
<li>'convert_image failed with code [number]: [error details]'</li>
<li>Files may be renamed with '.failed' extension</li>
</ul>

<p><strong>How to Fix:</strong></p>
<ol>
<li>Verify the image file is not corrupted by opening it in an image viewer.</li>
<li>Re-export the image in a supported format: JPG, PNG, GIF, TIF, or TIFF.</li>
<li>Check file size - source files should be under 15 MB before upload, and under 4 MB after processing.</li>
<li>Re-upload the corrected image to FTP and wait for the next sync cycle.</li>
</ol>

<blockquote>💡 <strong>Tip:</strong> If issues persist, <a href="mailto:support@supercatsolutions.com">Contact Support</a> with the filename and error message.</blockquote>
```

---

## Section 8: Error Type 7 (Section ID: 41704)

```html
<h2>Error Type 7: XMP/Metadata Profile Issues</h2>

<p><strong>What This Warning Means:</strong> This error can occur during image import when an image file contains problematic XMP or metadata profiles that cause processing issues.</p>

<p><strong>Root Cause:</strong> Some images contain complex or malformed XMP (Extensible Metadata Platform) profiles that can cause ImageMagick processing issues. This is common with images from professional photography software or certain camera RAW exports.</p>

<p><strong>Error Messages:</strong> Processing failures mentioning XMP or metadata, images failing without clear error messages, or ImageMagick warnings about invalid profiles.</p>

<p><strong>How to Fix:</strong></p>
<ol>
<li>Strip metadata using a tool like ImageOptim (Mac) or similar utility.</li>
<li>Re-export the image from your editing software without metadata embedded.</li>
<li>Alternatively, use command-line tools like exiftool or mogrify to strip XMP metadata.</li>
<li>Re-upload the cleaned image to FTP.</li>
</ol>

<blockquote><strong>Note:</strong> Stripping metadata removes information like camera settings and copyright data. Save a backup of the original file if you need to retain this information.</blockquote>
```

---

## Section 9: Best Practices (Section ID: 41644)

```html
<h2>Best Practices</h2>

<h3>Before Importing</h3>
<ul>
<li>Verify all image files exist and are ready to upload</li>
<li>Check CSV file formatting and image filename accuracy</li>
<li>Use consistent naming conventions (e.g., 'ItemNumber.jpg', 'ItemNumber_2.jpg')</li>
<li>Test with a small batch before full import</li>
<li>Validate filenames match exactly between CSV and actual files (case-sensitive)</li>
<li>Ensure images are in sRGB color space - convert CMYK images before upload</li>
<li>Check filename validity - no /, (, or ) characters</li>
<li>Count images per product - ensure within limit (6 or 12)</li>
<li>Test image files - open each file to verify it is not corrupted</li>
<li>Verify file sizes - source files should be under 15 MB</li>
</ul>

<h3>During Import</h3>
<ul>
<li>Monitor import logs for image-related errors</li>
<li>Validate image file references in the CSV</li>
<li>Upload images before or during product file import</li>
<li>Check file permissions and server accessibility</li>
</ul>

<h3>After Import</h3>
<ul>
<li>Run the Missing Images report to verify all images are found</li>
<li>Test image display in the portal or catalog</li>
<li>Verify image URLs are working correctly</li>
<li>Address any errors found in the report promptly</li>
</ul>

<h3>Ongoing Maintenance</h3>
<ul>
<li>Regular image audits using the Missing Images report</li>
<li>Monitor file storage and cleanup orphaned files</li>
<li>Update image references when files change</li>
<li>Document image management procedures for your team</li>
<li>Establish naming conventions and stick to them</li>
</ul>
```

---

## Section 10: Troubleshooting (Section ID: 41648)

```html
<h2>Troubleshooting</h2>

<h3>Images not displaying in portal?</h3>
<p>Check that the file format is supported (JPG, PNG, GIF, TIF, TIFF). Ensure proper file naming with no special characters. Verify case sensitivity matches between product file and uploaded file.</p>

<h3>Multiple image errors for the same product?</h3>
<p>Review your CSV file structure for consistency. Remove placeholder image references if you do not plan to upload them. Check for encoding issues in the CSV. Verify all referenced files exist before importing.</p>

<h3>Case sensitivity errors?</h3>
<p>If your product file references 'ABC123.jpg' but the file was uploaded as 'abc123.jpg', either rename the image file to match exactly or update the product file to match the uploaded filename.</p>

<h3>Import fails with image errors?</h3>
<p>Fix image references in the CSV file first. Upload missing image files to the server. Re-run the import after corrections. Check import logs for specific error messages.</p>

<h3>Images look dull or gray after import?</h3>
<p>The image is likely in CMYK color space instead of sRGB. Check import logs for color space warnings. Convert images to sRGB before uploading or request sRGB versions from your vendor.</p>

<h3>Image filenames rejected during import?</h3>
<p>The filename contains invalid characters (/, (, )). Remove invalid characters and use alphanumeric characters, dashes, underscores, and dots only.</p>

<h3>Some images not imported (limit exceeded)?</h3>
<p>The product has more images than the limit (6 standard, or 12 if enabled). Prioritize images by listing the most important ones first in your CSV.</p>

<h3>Image processing fails with .failed extension?</h3>
<p>Verify the image opens correctly in an image viewer. Re-export in a supported format. Check file is not corrupted. Ensure file size is under 15 MB (source) / 4 MB (processed). Strip metadata if XMP issues are suspected.</p>

<h3>Need more help?</h3>
<p><a href="mailto:support@supercatsolutions.com">Contact Support</a> with specific error messages from the report, item numbers affected, example filenames causing issues, and a screenshot of the Missing Images report if possible.</p>
```

---

## Sections to CLEAR (paste empty or delete)

These sections should be cleared or deleted as they're now redundant:

- **Section 41705** - Clear (was Quick Troubleshooting Flowchart)
- **Section 41645** - Clear (was Common Issues Part 1)
- **Section 41646** - Clear (was Common Issues Part 2)
- **Section 41647** - Clear (was old Best Practices - now combined in 41644)
- **Section 41649** - Clear (was Summary - now in Overview)

---

## Expected TOC After Updates

1. Overview
2. Error Type 1: Product Record Does Not Specify an Image File Name
3. Error Type 2: Missing Image [filename]
4. Error Type 3: Color Space Warning (CMYK vs sRGB)
5. Error Type 4: Invalid Image Filename
6. Error Type 5: Image Limit Exceeded
7. Error Type 6: Image Processing Error
8. Error Type 7: XMP/Metadata Profile Issues
9. Best Practices
10. Troubleshooting

**NO sub-entries** - all steps use `<ol>` lists which don't appear in TOC.
