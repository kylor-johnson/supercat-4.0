#!/usr/bin/env python3
"""Assemble PACKET.md from the pieces saved in a replay directory.
usage: packet_assemble.py <dir> --conv <id> --t <ISO UTC> [--client "Name"]
Expects: threads.json (rows from replay_threads.sql), optional meetings.md, calendar.json, state.md, folder.md
Writes:  <dir>/PACKET.md and refuses if any thread is after T."""
import argparse, json, re, sys
from pathlib import Path
from datetime import datetime, timezone

def ts(v):
    if isinstance(v, dict): v = v.get("value")
    return datetime.fromisoformat(v.replace("Z", "+00:00"))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("dir"); ap.add_argument("--conv", required=True)
    ap.add_argument("--t", required=True); ap.add_argument("--client", default="")
    a = ap.parse_args(); d = Path(a.dir); T = datetime.fromisoformat(a.t.replace("Z", "+00:00"))
    rows = json.load(open(d / "threads.json"))
    late = [r for r in rows if ts(r["thread_created_at"]) > T]
    if late: sys.exit(f"LEAK: {len(late)} threads after T; first {late[0]['conversation_id']} {late[0]['thread_created_at']}")
    out = [f"# Packet — conversation {a.conv} — cut at {T.isoformat()}", "",
           f"Client: {a.client or '(from threads)'}. Everything below existed at T. Notes after T, later threads, the sent reply: not included.", ""]
    by = {}
    for r in rows: by.setdefault(r["conversation_id"], []).append(r)
    out.append("## 1. Threads (cut at T)")
    for cid, th in by.items():
        h = th[0]; tag = " ← THIS TICKET" if str(cid) == str(a.conv) else ""
        out.append(f"\n### #{h['ticket_number']} ({cid}){tag} — {h['ticket_subject']}\nmailbox {h['mailbox_id']} · assignee {h.get('assignee_email') or 'unassigned'} · tags: {h.get('tags') or '-'}")
        for r in th:
            body = re.sub(r"\n{3,}", "\n\n", (r.get("thread_body") or "").strip())
            # Never trim this ticket's own threads, and never trim a forward: the complaint in a
            # "FW:" message sits below its From: line (a trimmed forward hid the whole issue once).
            fwd = re.match(r"\s*(re:\s*)*(fw|fwd):", (h.get('ticket_subject') or ''), re.I)
            if not tag and not fwd:
                m = re.search(r"\n(On .{5,120}wrote:|-----Original Message-----)", body)
                if m: body = body[:m.start()] + "\n[quoted history trimmed]"
            att = f" · attachments: {r['thread_attachment_count']}" if r.get("thread_attachment_count") else ""
            out.append(f"\n--- {ts(r['thread_created_at']).strftime('%Y-%m-%d %H:%M')} UTC · {r['thread_type']} · {r['thread_author_email']}{att}\n{body}")
    for name, title in [("meetings.md", "## 2. Meetings (cut at T)"), ("calendar.json", "## 2b. Calendar (T-7d → T)"),
                        ("folder.md", "## 3. Client folder"), ("state.md", "## 4. Live state (read-only, updated_at shown)")]:
        p = d / name
        out.append(f"\n{title}\n")
        out.append(p.read_text().strip() if p.exists() else "(none)")
    out.append("\n## LEAK CHECK\nNo thread after T (asserted by this script). Meetings and notes after T excluded by construction.")
    (d / "PACKET.md").write_text("\n".join(out) + "\n"); print(f"wrote {d/'PACKET.md'} ({len(rows)} threads, {len(by)} conversations)")

if __name__ == "__main__": main()
