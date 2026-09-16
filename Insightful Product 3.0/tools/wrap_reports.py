#!/usr/bin/env python3
"""
wrap_reports.py — Batch-wrap Insightful HTML reports with AES password gate.

Usage:
    python3 wrap_reports.py --runs-dir ./runs --output-dir ./deploy [--date 2026-06-17]

Each report gets:
  - AES-256-GCM encrypted content (Web Crypto API in browser)
  - A branded password screen matching the Insightful report aesthetic
  - Auto-generated 8-char password (or override via manifest CSV)

Outputs:
  deploy/{shortname}/index.html   (password-gated)
  deploy/_manifest.csv            (shortname, client_name, password, url)
"""

import argparse
import base64
import hashlib
import json
import os
import re
import sys
from pathlib import Path

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except ImportError:
    print("Installing cryptography package...")
    os.system(f"{sys.executable} -m pip install cryptography -q")
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM


GATE_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{CLIENT_NAME}} — Intelligence Report</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300..800;1,9..40,300..800&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #FAFAF8; --surface: #FFFFFF; --border: #E8E5DE;
      --text: #2C2925; --text-secondary: #6B6660; --text-muted: #9B958C;
      --accent: #C47A4A; --accent-deep: #89523B; --accent-light: #F5EDE6;
      --danger: #C0524A;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'DM Sans', system-ui, sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .gate {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 3rem 2.5rem;
      max-width: 420px;
      width: 90vw;
      text-align: center;
      box-shadow: 0 4px 24px rgba(44,41,37,.06);
    }
    .gate .brand {
      font-size: 0.75rem;
      font-weight: 600;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 0.75rem;
    }
    .gate h1 {
      font-size: 1.35rem;
      font-weight: 700;
      margin-bottom: 0.4rem;
    }
    .gate .sub {
      font-size: 0.88rem;
      color: var(--text-secondary);
      margin-bottom: 2rem;
    }
    .gate input {
      width: 100%;
      padding: 0.85rem 1rem;
      font-family: inherit;
      font-size: 1rem;
      border: 1px solid var(--border);
      border-radius: 8px;
      outline: none;
      text-align: center;
      letter-spacing: 0.15em;
      transition: border-color .2s;
    }
    .gate input:focus { border-color: var(--accent); }
    .gate button {
      width: 100%;
      margin-top: 1rem;
      padding: 0.85rem;
      font-family: inherit;
      font-size: 0.95rem;
      font-weight: 600;
      background: var(--accent);
      color: #fff;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      transition: background .2s;
    }
    .gate button:hover { background: var(--accent-deep); }
    .gate .error {
      margin-top: 1rem;
      font-size: 0.82rem;
      color: var(--danger);
      display: none;
    }
    .bar {
      width: 50px; height: 3px;
      background: var(--accent);
      border-radius: 2px;
      margin: 0 auto 1.5rem;
    }
    .footer {
      margin-top: 2rem;
      font-size: 0.72rem;
      color: var(--text-muted);
    }
  </style>
</head>
<body>
  <div class="gate" id="gate">
    <div class="brand">Insightful &middot; Customer Intelligence</div>
    <h1>{{CLIENT_NAME}}</h1>
    <div class="sub">Enter your access code to view this report.</div>
    <div class="bar"></div>
    <input type="password" id="pw" placeholder="Access code" autofocus
           onkeydown="if(event.key==='Enter')unlock()">
    <button onclick="unlock()">View Report</button>
    <div class="error" id="err">Incorrect access code. Please try again.</div>
    <div class="footer">SuperCat Solutions &middot; Confidential</div>
  </div>

  <script>
    var ENC = "{{CIPHERTEXT}}";
    var SALT = "{{SALT}}";
    var IV = "{{IV}}";

    async function deriveKey(password) {
      var enc = new TextEncoder();
      var keyMaterial = await crypto.subtle.importKey(
        "raw", enc.encode(password), "PBKDF2", false, ["deriveKey"]
      );
      return crypto.subtle.deriveKey(
        { name: "PBKDF2", salt: b64ToBytes(SALT), iterations: 100000, hash: "SHA-256" },
        keyMaterial, { name: "AES-GCM", length: 256 }, false, ["decrypt"]
      );
    }

    function b64ToBytes(b64) {
      var bin = atob(b64);
      var bytes = new Uint8Array(bin.length);
      for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
      return bytes;
    }

    async function unlock() {
      var pw = document.getElementById("pw").value;
      if (!pw) return;
      try {
        var key = await deriveKey(pw);
        var decrypted = await crypto.subtle.decrypt(
          { name: "AES-GCM", iv: b64ToBytes(IV) },
          key, b64ToBytes(ENC)
        );
        var html = new TextDecoder().decode(decrypted);
        sessionStorage.setItem("ir_{{SHORT}}", pw);
        document.open();
        document.write(html);
        document.close();
      } catch (e) {
        document.getElementById("err").style.display = "block";
        document.getElementById("pw").select();
      }
    }

    (async function() {
      var saved = sessionStorage.getItem("ir_{{SHORT}}");
      if (saved) {
        document.getElementById("pw").value = saved;
        await unlock();
      }
    })();
  </script>
</body>
</html>"""


def extract_client_name(html_path: Path) -> str:
    """Pull client name from the <title> tag."""
    text = html_path.read_text("utf-8")[:2000]
    m = re.search(r"<title>\s*(.+?)\s*[—–-]\s*Customer Intelligence", text)
    if m:
        return m.group(1).strip()
    m = re.search(r"<title>\s*(.+?)\s*</title>", text)
    if m:
        return m.group(1).strip()
    return html_path.stem


def generate_password(shortname: str, length: int = 8) -> str:
    """Deterministic but non-obvious password from shortname + secret seed."""
    import secrets
    chars = "abcdefghjkmnpqrstuvwxyz23456789"
    return "".join(secrets.choice(chars) for _ in range(length))


def encrypt_html(html_content: str, password: str) -> tuple[str, str, str]:
    """Encrypt HTML with AES-256-GCM via PBKDF2-derived key. Returns (ciphertext_b64, salt_b64, iv_b64)."""
    salt = os.urandom(16)
    iv = os.urandom(12)

    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000, dklen=32)
    aesgcm = AESGCM(dk)
    ct = aesgcm.encrypt(iv, html_content.encode("utf-8"), None)

    return (
        base64.b64encode(ct).decode(),
        base64.b64encode(salt).decode(),
        base64.b64encode(iv).decode(),
    )


def wrap_report(html_path: Path, output_dir: Path, password: str, shortname: str) -> str:
    """Wrap a single report. Returns client name."""
    html_content = html_path.read_text("utf-8")
    client_name = extract_client_name(html_path)
    ct_b64, salt_b64, iv_b64 = encrypt_html(html_content, password)

    gate_html = GATE_TEMPLATE
    gate_html = gate_html.replace("{{CLIENT_NAME}}", client_name)
    gate_html = gate_html.replace("{{CIPHERTEXT}}", ct_b64)
    gate_html = gate_html.replace("{{SALT}}", salt_b64)
    gate_html = gate_html.replace("{{IV}}", iv_b64)
    gate_html = gate_html.replace("{{SHORT}}", shortname)

    out_path = output_dir / shortname / "index.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(gate_html, "utf-8")
    return client_name


def main():
    parser = argparse.ArgumentParser(description="Batch-wrap Insightful reports with password gate")
    parser.add_argument("--runs-dir", required=True, help="Path to runs/ directory")
    parser.add_argument("--output-dir", required=True, help="Path to deploy output directory")
    parser.add_argument("--date", default="2026-06-17", help="Run date suffix (default: 2026-06-17)")
    parser.add_argument("--manifest-csv", help="Optional CSV with shortname,password overrides")
    args = parser.parse_args()

    runs_dir = Path(args.runs_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    password_overrides = {}
    if args.manifest_csv and Path(args.manifest_csv).exists():
        import csv
        with open(args.manifest_csv) as f:
            for row in csv.DictReader(f):
                password_overrides[row["shortname"]] = row["password"]

    results = []
    for run_folder in sorted(runs_dir.iterdir()):
        if not run_folder.is_dir():
            continue
        name = run_folder.name
        if not name.endswith(f"_{args.date}"):
            continue
        shortname = name.replace(f"_{args.date}", "")

        html_file = run_folder / "output" / f"{name}_intelligence_report.html"
        if not html_file.exists():
            print(f"  SKIP  {shortname} — no output HTML")
            continue

        password = password_overrides.get(shortname, generate_password(shortname))
        client_name = wrap_report(html_file, output_dir, password, shortname)
        results.append((shortname, client_name, password))
        print(f"  OK    {shortname:12s}  {client_name}")

    manifest_path = output_dir / "_manifest.csv"
    with open(manifest_path, "w") as f:
        f.write("shortname,client_name,password,url\n")
        for short, name, pw in results:
            url = f"https://supercat-reports.pages.dev/{short}/"
            f.write(f'{short},"{name}",{pw},{url}\n')

    print(f"\n{'='*60}")
    print(f"  Wrapped {len(results)} reports → {output_dir}/")
    print(f"  Manifest: {manifest_path}")
    print(f"{'='*60}")
    print(f"\n  Deploy:  npx wrangler pages deploy {output_dir} --project-name=supercat-reports")
    print()

    print("CLIENT PASSWORDS:")
    print("-" * 60)
    for short, name, pw in results:
        print(f"  {name:40s}  {pw}")
    print("-" * 60)


if __name__ == "__main__":
    main()
