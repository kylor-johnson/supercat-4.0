#!/bin/bash
# Template for downloading Magic Lite product images
# This template saves images directly to the correct iCloud folder

# ============================================================================
# CONFIGURATION
# ============================================================================

# Output directory - UPDATE THIS PATH if folder structure changes
OUTPUT_DIR="/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/Magic Lite/Images"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# ============================================================================
# FUNCTIONS
# ============================================================================

# Function to download and convert image
download_image() {
    local url="$1"
    local output_file="$2"
    
    if [ -f "$OUTPUT_DIR/$output_file" ]; then
        echo "  ⊙ Skipped (exists): $output_file"
        return 0
    fi
    
    # Download to temp file
    temp_file=$(mktemp)
    if curl -s -L -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
         -o "$temp_file" "$url" 2>/dev/null; then
        
        # Check if file is valid and not empty
        if [ -s "$temp_file" ]; then
            # Convert to JPG using sips (macOS built-in)
            sips -s format jpeg "$temp_file" --out "$OUTPUT_DIR/$output_file" >/dev/null 2>&1
            
            if [ $? -eq 0 ]; then
                echo "  ✓ Downloaded: $output_file"
                rm -f "$temp_file"
                return 0
            else
                echo "  ✗ Failed to convert: $output_file"
                rm -f "$temp_file"
                return 1
            fi
        else
            echo "  ✗ Failed: $output_file (empty file)"
            rm -f "$temp_file"
            return 1
        fi
    else
        echo "  ✗ Failed: $output_file (download error)"
        rm -f "$temp_file"
        return 1
    fi
}

# ============================================================================
# MAIN SCRIPT
# ============================================================================

echo "Starting image downloads..."
echo "Output directory: $OUTPUT_DIR"
echo ""

# ============================================================================
# EXAMPLE: Download images for a product
# ============================================================================

# Example product: Under Cabinet Light
# echo "=== PRODUCT-CODE-HERE ==="
# download_image "https://magiclite.com/wp-content/uploads/YYYY/MM/image-name.png" "PRODUCT-CODE.jpg"
# download_image "https://magiclite.com/wp-content/uploads/YYYY/MM/image-name-2.png" "PRODUCT-CODE-2.jpg"
# download_image "https://magiclite.com/wp-content/uploads/YYYY/MM/image-name-3.png" "PRODUCT-CODE-3.jpg"

# ============================================================================
# ADD YOUR PRODUCT DOWNLOADS BELOW
# ============================================================================

# TODO: Add product image downloads here
# Format:
# echo "=== PRODUCT-CODE ==="
# download_image "IMAGE-URL" "PRODUCT-CODE.jpg"
# download_image "IMAGE-URL-2" "PRODUCT-CODE-2.jpg"
# etc.

echo ""
echo "============================================================"
echo "Download complete!"
echo "Images saved to: $OUTPUT_DIR"
echo "============================================================"

# ============================================================================
# USAGE INSTRUCTIONS
# ============================================================================

# 1. Copy this template to a new file (e.g., download_under_cabinet_images.sh)
# 2. Add your product image URLs in the section above
# 3. Make executable: chmod +x download_under_cabinet_images.sh
# 4. Run: ./download_under_cabinet_images.sh
# 5. Images will be saved directly to the Images folder
# 6. No manual moving required!

# ============================================================================
# TIPS
# ============================================================================

# To find image URLs:
# curl -s "https://magiclite.com/product/category/subcategory/product-name/" | \
#   grep -o 'https://magiclite.com/wp-content/uploads/[^"]*\.png' | \
#   grep -v webp | grep -v '116x116\|32x32\|192x192\|180x180\|270x270\|300x'

# To extract product codes from a page:
# curl -s "PRODUCT-URL" | grep -o 'Product Code.*' | head -5
