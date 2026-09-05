#!/usr/bin/env python3
"""Run a read-only SELECT against supercatprod via the configured Postgres MCP
endpoint and write the rows to disk as JSON.

Exists because the Postgres MCP is a remote HTTP server (VPN-only, no local
DSN), so psycopg2 cannot reach the database directly. Once DATABASE_URL is
available this module can be bypassed -- build_dataset.py accepts either source.

The endpoint speaks the HTTP+SSE MCP transport: GET /sse yields an `endpoint`
event carrying a session-scoped POST URL; JSON-RPC requests go to that URL and
their responses arrive back on the SSE stream.

Usage:
    python3 mcp_sql.py --sql-file query.sql --out rows.json
    python3 mcp_sql.py --sql "SELECT 1" --out rows.json
"""
from __future__ import annotations

import argparse
import json
import os
import queue
import sys
import threading
import urllib.parse
import urllib.request

MCP_CONFIG = os.path.expanduser("~/.cursor/mcp.json")
SERVER_KEY = "supercat-postgres-vpn"
READ_TIMEOUT = 900


def _eval_repr(text: str):
    """The server renders rows as Python reprs, which include datetime.date(...)
    and Decimal(...) calls that ast.literal_eval rejects. Evaluate in a namespace
    restricted to those constructors -- no builtins, so nothing else can run."""
    import datetime
    from decimal import Decimal

    namespace = {
        "datetime": datetime,
        "Decimal": Decimal,
        "date": datetime.date,
        "time": datetime.time,
        "timedelta": datetime.timedelta,
        "UUID": __import__("uuid").UUID,
        "None": None,
    }
    return eval(text, {"__builtins__": {}}, namespace)  # noqa: S307 - restricted namespace


def endpoint_url() -> str:
    with open(MCP_CONFIG, "r", encoding="utf-8") as fh:
        cfg = json.load(fh)
    servers = cfg.get("mcpServers") or cfg.get("servers") or {}
    entry = servers.get(SERVER_KEY)
    if not entry or "url" not in entry:
        raise SystemExit(f"No url for MCP server {SERVER_KEY!r} in {MCP_CONFIG}")
    return entry["url"]


class SseSession:
    def __init__(self, sse_url: str):
        self.sse_url = sse_url
        self.post_url: str | None = None
        self._messages: "queue.Queue[dict]" = queue.Queue()
        self._endpoint_ready = threading.Event()
        self._error: BaseException | None = None
        self._next_id = 0
        self._thread = threading.Thread(target=self._pump, daemon=True)

    def _pump(self) -> None:
        """Read the SSE stream forever, dispatching endpoint and message events."""
        try:
            req = urllib.request.Request(self.sse_url, headers={"Accept": "text/event-stream"})
            with urllib.request.urlopen(req, timeout=READ_TIMEOUT) as resp:
                event, data_lines = None, []
                for raw in resp:
                    line = raw.decode("utf-8", "replace").rstrip("\r\n")
                    if line == "":
                        if data_lines:
                            self._dispatch(event, "\n".join(data_lines))
                        event, data_lines = None, []
                        continue
                    if line.startswith("event:"):
                        event = line[6:].strip()
                    elif line.startswith("data:"):
                        data_lines.append(line[5:].strip())
        except BaseException as exc:  # surfaced to the caller via _error
            self._error = exc
            self._endpoint_ready.set()

    def _dispatch(self, event: str | None, data: str) -> None:
        if event == "endpoint":
            base = urllib.parse.urlparse(self.sse_url)
            self.post_url = urllib.parse.urljoin(f"{base.scheme}://{base.netloc}", data)
            self._endpoint_ready.set()
            return
        try:
            self._messages.put(json.loads(data))
        except json.JSONDecodeError:
            pass

    def open(self) -> None:
        self._thread.start()
        if not self._endpoint_ready.wait(timeout=60):
            raise SystemExit("Timed out waiting for MCP endpoint event")
        if self._error:
            raise SystemExit(f"SSE stream failed: {self._error!r}")

    def _await_id(self, want: int) -> dict:
        while True:
            try:
                msg = self._messages.get(timeout=READ_TIMEOUT)
            except queue.Empty:
                raise SystemExit(f"Timed out waiting for JSON-RPC response id={want}")
            if msg.get("id") == want:
                return msg

    def _rpc(self, method: str, params: dict, notify: bool = False):
        payload = {"jsonrpc": "2.0", "method": method, "params": params}
        if not notify:
            self._next_id += 1
            payload["id"] = self._next_id
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.post_url, data=body, headers={"Content-Type": "application/json"}, method="POST"
        )
        with urllib.request.urlopen(req, timeout=READ_TIMEOUT) as resp:
            resp.read()
        if notify:
            return None
        msg = self._await_id(self._next_id)
        if "error" in msg:
            raise SystemExit(f"MCP error on {method}: {json.dumps(msg['error'])[:600]}")
        return msg.get("result", {})

    def initialize(self) -> None:
        self._rpc(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "sales-portal-dataset-builder", "version": "1.0"},
            },
        )
        self._rpc("notifications/initialized", {}, notify=True)

    def execute_sql(self, sql: str):
        result = self._rpc("tools/call", {"name": "execute_sql", "arguments": {"sql": sql}})
        if result.get("isError"):
            raise SystemExit(f"SQL error: {json.dumps(result)[:1000]}")
        sc = result.get("structuredContent")
        if isinstance(sc, dict) and "result" in sc:
            return sc["result"]
        if sc is not None:
            return sc
        texts = [c.get("text", "") for c in result.get("content", []) if c.get("type") == "text"]
        joined = "\n".join(texts).strip()
        if joined.startswith("Error:") or joined.startswith("ERROR:"):
            raise SystemExit(f"SQL error: {joined[:800]}")
        try:
            return json.loads(joined)
        except json.JSONDecodeError:
            return _eval_repr(joined)


def connect() -> SseSession:
    sess = SseSession(endpoint_url())
    sess.open()
    sess.initialize()
    return sess


def run(sql: str):
    return connect().execute_sql(sql)


def main() -> None:
    ap = argparse.ArgumentParser()
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--sql")
    src.add_argument("--sql-file")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    sql = args.sql if args.sql else open(args.sql_file, "r", encoding="utf-8").read()
    rows = run(sql)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(rows, fh, default=str)
    n = len(rows) if isinstance(rows, list) else 1
    print(f"wrote {n} row(s) -> {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
