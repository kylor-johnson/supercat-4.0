#!/usr/bin/env python3
"""Screenshot the client-review v2 artifact across views and scopes.

Also fails loudly on any console error, so a broken render can't slip into a
client session.
"""
from __future__ import annotations

import pathlib
import sys

from playwright.sync_api import sync_playwright

APP = pathlib.Path(__file__).resolve().parents[4] / "design-system" / "app"
HTML = APP / "sales-portal-client-review-v2.html"
OUT = pathlib.Path("/tmp/spshots-v2")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page(viewport={"width": 1440, "height": 960}, device_scale_factor=2)
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(HTML.as_uri())
        page.wait_for_timeout(1200)

        for name, nav in [
            ("1-dashboard", "dashboard"),
            ("2-intelligence", "intelligence"),
            ("3-customers", "customers"),
            ("4-orders", "orders"),
            ("5-invoices", "invoices"),
            ("6-reports", "reports"),
            ("7-settings", "settings"),
        ]:
            page.click(f'[data-view="{nav}"]')
            page.wait_for_timeout(500)
            page.screenshot(path=str(OUT / f"{name}.png"), full_page=False)

        page.click('[data-view="reports"]')
        page.select_option("#groupby", "territory")
        page.wait_for_timeout(400)
        page.screenshot(path=str(OUT / "8-reports-territory.png"))

        opts = page.eval_on_selector_all(
            "#territory option", "els => els.map(e => e.value).filter(Boolean)"
        )
        page.select_option("#territory", opts[0])
        page.wait_for_timeout(450)
        page.click('[data-view="intelligence"]')
        page.wait_for_timeout(500)
        page.screenshot(path=str(OUT / "9-intelligence-territory.png"))

        page.select_option("#territory", "none")
        page.wait_for_timeout(450)
        page.click('[data-view="orders"]')
        page.wait_for_timeout(400)
        page.screenshot(path=str(OUT / "10-orders-unassigned.png"))

        b.close()

    print("console:", "clean" if not errors else errors[:5])
    if errors:
        sys.exit(1)
    print("shots ->", OUT)


if __name__ == "__main__":
    main()
