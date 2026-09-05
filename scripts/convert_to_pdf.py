#!/usr/bin/env python3
"""
Convert HTML to PDF using Chrome headless
"""
import subprocess
import sys
import os

def html_to_pdf(html_file, pdf_file):
    """Convert HTML to PDF using Chrome headless"""
    
    # Get absolute paths
    html_path = os.path.abspath(html_file)
    pdf_path = os.path.abspath(pdf_file)
    
    # Use Chrome headless to print to PDF
    cmd = [
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '--headless',
        '--disable-gpu',
        '--print-to-pdf=' + pdf_path,
        '--no-margins',
        'file://' + html_path
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"Successfully created PDF: {pdf_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"stderr: {e.stderr.decode()}")
        return False
    except FileNotFoundError:
        print("Chrome not found. Trying with chromium...")
        # Try chromium as fallback
        cmd[0] = '/Applications/Chromium.app/Contents/MacOS/Chromium'
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"Successfully created PDF: {pdf_path}")
            return True
        except:
            print("Neither Chrome nor Chromium found.")
            return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: convert_to_pdf.py <input.html> <output.pdf>")
        sys.exit(1)
    
    html_file = sys.argv[1]
    pdf_file = sys.argv[2]
    
    if not os.path.exists(html_file):
        print(f"Error: HTML file not found: {html_file}")
        sys.exit(1)
    
    success = html_to_pdf(html_file, pdf_file)
    sys.exit(0 if success else 1)
