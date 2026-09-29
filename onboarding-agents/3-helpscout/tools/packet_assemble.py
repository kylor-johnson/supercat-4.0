#!/usr/bin/env python3
"""Assemble PACKET.md from the pieces saved in a replay directory.
usage: packet_assemble.py <dir> --conv <id> --t <ISO UTC> [--client "Name"] [--out PACKET.md]
Expects: threads.json (rows from replay_threads.sql), optional meetings.md, calendar.json, state.md, folder.md,
         fleet.md (replay_fleet_at_t.sql results), scope.json (replay_scope_at_t.sql reading)
Writes:  <dir>/PACKET.md. Refuses if any thread, meeting header, calendar event or fleet row is after T."""
import argparse, json, re, sys
from pathlib import Path
from datetime import datetime, timezone

def ts(v):
    if isinstance(v, dict): v = v.get("value")
    return datetime.fromisoformat(v.replace("Z", "+00:00"))

ISO = re.compile(r"(\d{4}-\d{2}-\d{2})(?:[T ](\d{2}:\d{2}(?::\d{2})?))?")

def after_t(s, T):
    """Every ISO date/time in s that is later than T (date-only values compare by day)."""
    bad = []
    for d, hm in ISO.findall(s):
        if hm:
            v = datetime.fromisoformat(f"{d}T{hm}").replace(tzinfo=timezone.utc)
            if v > T: bad.append(f"{d} {hm}")
        elif d > T.date().isoformat():
            bad.append(d)
    return bad

errs_note = []

def check_sections(d, T):
    """The hand-supplied sections are asserted too, not trusted: a leak in any of them refuses the build."""
    errs = []
    m = d / "meetings.md"
    if m.exists():
        for line in m.read_text().splitlines():
            if line.startswith("## "):
                errs += [f"meetings.md header {x}" for x in after_t(line, T)]
    c = d / "calendar.json"
    if c.exists():
        try:
            cal = json.loads(c.read_text() or "{}")
        except json.JSONDecodeError:
            cal = {}
            errs_note.append("calendar.json is not JSON (not pre-fetched?): calendar cut NOT asserted; the builder must fetch events for [T-7d, T]")
        for ev in cal.get("events", []):
            errs += [f"calendar event {x}" for x in after_t(json.dumps(ev.get("start", ev)), T)]
        w = cal.get("window") or []
        if len(w) == 2: errs += [f"calendar window end {x}" for x in after_t(str(w[1]), T)]
    f = d / "fleet.md"
    if f.exists():
        errs += [f"fleet.md {x}" for x in after_t(f.read_text(), T)]
    return errs

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("dir"); ap.add_argument("--conv", required=True)
    ap.add_argument("--t", required=True); ap.add_argument("--client", default="")
    ap.add_argument("--out", default="PACKET.md", help="file name inside <dir>; use PACKET_rebuilt.md to keep an old packet as the record")
    a = ap.parse_args(); d = Path(a.dir); T = datetime.fromisoformat(a.t.replace("Z", "+00:00"))
    rows = json.load(open(d / "threads.json"))
    late = [r for r in rows if ts(r["thread_created_at"]) > T]
    if late: sys.exit(f"LEAK: {len(late)} threads after T; first {late[0]['conversation_id']} {late[0]['thread_created_at']}")
    bad = check_sections(d, T)
    if bad: sys.exit("LEAK: dated content after T in a hand-supplied section: " + "; ".join(bad[:10]))
    out = [f"# Packet — conversation {a.conv} — cut at {T.isoformat()}", "",
           f"Client: {a.client or '(from threads)'}. Everything below existed at T. Notes after T, later threads, the sent reply: not included.", ""]
    sp = d / "scope.json"
    if sp.exists():
        s = json.loads(sp.read_text())
        out += [f"Scope at T: mailbox {s.get('mailbox_at_t')} · assignee {s.get('assignee_at_t')} ({s.get('basis', 'replay_scope_at_t.sql')}). The mailbox/assignee lines under each ticket below are today's values.", ""]
    else:
        out += ["Scope at T: NOT BUILT (no scope.json). The mailbox/assignee lines below are today's values, not T's.", ""]
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
    for name, title in [("fleet.md", "## 1b. Fleet at T (other clients' tickets T-2h → T; sessions, logins, import fatals T-24h → T)"),
                        ("meetings.md", "## 2. Meetings (cut at T)"), ("calendar.json", "## 2b. Calendar (T-7d → T)"),
                        ("folder.md", "## 3. Client folder"), ("state.md", "## 4. Live state (read-only, updated_at shown)")]:
        p = d / name
        out.append(f"\n{title}\n")
        if p.exists(): out.append(p.read_text().strip())
        elif name == "fleet.md": out.append("NOT BUILT. A fleet-wide incident (other clients reporting the same thing, a session or login dip, import fatals across orgs) is invisible in this packet; say so before blaming one client's setup.")
        else: out.append("(none)")
    if errs_note: out.append("\n## BUILD WARNINGS\n" + "\n".join("- " + n for n in errs_note))
    out.append("\n## LEAK CHECK\nAsserted by this script: no thread, meeting header, calendar event or fleet row after T. Not asserted: free text inside meetings.md / folder.md / state.md (state rows may be later than T and are labelled by the builder).")
    (d / a.out).write_text("\n".join(out) + "\n"); print(f"wrote {d/a.out} ({len(rows)} threads, {len(by)} conversations)")

if __name__ == "__main__": main()
