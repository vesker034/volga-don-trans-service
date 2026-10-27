# -*- coding: utf-8 -*-
"""PNG всех страниц (light/dark) для ручной вставки в Figma — без MCP."""

import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "figma-import" / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)

PORT = 8080
HOST = f"http://localhost:{PORT}"

PAGES = [
    ("glavnaya", "index.html"),
    ("uslugi", "uslugi.html"),
    ("o-kompanii", "o-kompanii.html"),
    ("kak-rabotaem", "kak-rabotaem.html"),
    ("opyt", "opyt.html"),
    ("faq", "faq.html"),
    ("kontakty", "kontakty.html"),
    ("politika-pdn", "politika-pdn.html"),
    ("politika-cookies", "politika-cookies.html"),
]


def capture(page, slug: str, src: str, theme: str) -> None:
    page.goto(f"{HOST}/{src}", wait_until="networkidle")
    page.evaluate(
        """(theme) => {
          document.documentElement.setAttribute('data-theme', theme);
          localStorage.setItem('vdts_theme', theme);
          localStorage.setItem('cookies_accepted', '1');
          const b = document.getElementById('cookieBanner');
          if (b) b.hidden = true;
          document.body.classList.remove('has-cookie-banner');
        }""",
        theme,
    )
    page.wait_for_timeout(600)
    height = page.evaluate("() => document.documentElement.scrollHeight")
    page.set_viewport_size({"width": 1440, "height": min(height, 16000)})
    filename = OUT / f"{slug}-{theme}-1440.png"
    page.screenshot(path=str(filename), full_page=True)
    print(f"OK: {filename.name}")


def main() -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Установите: pip install playwright && playwright install chromium")
        sys.exit(1)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        for slug, src in PAGES:
            for theme in ("light", "dark"):
                capture(page, slug, src, theme)
        browser.close()

    print(f"\nГотово: {OUT}")


if __name__ == "__main__":
    main()
