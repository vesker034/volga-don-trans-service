# -*- coding: utf-8 -*-
"""Обновляет логотип ВДТ на всех HTML-страницах в design/."""
import pathlib

base = pathlib.Path(__file__).resolve().parent.parent

HEADER_OLD = """      <a href="index.html" class="logo">
        <div class="logo__mark">ВДТС</div>
        <div class="logo__sub">Волга-Дон-Транссервис</div>
      </a>"""

HEADER_NEW = """      <a href="index.html" class="logo" aria-label="ВДТ — на главную">
        <svg class="logo__svg logo__svg--dark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 148 52" width="96" height="34" aria-hidden="true">
          <text x="0" y="38" font-family="Manrope, system-ui, sans-serif" font-size="40" font-weight="800" letter-spacing="-1.6" fill="#0D1B2A">ВДТ</text>
          <rect x="0" y="46" width="44" height="2.5" fill="#0F4C81" rx="1"/>
        </svg>
        <svg class="logo__svg logo__svg--light" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 148 52" width="96" height="34" aria-hidden="true">
          <text x="0" y="38" font-family="Manrope, system-ui, sans-serif" font-size="40" font-weight="800" letter-spacing="-1.6" fill="#FFFFFF">ВДТ</text>
          <rect x="0" y="46" width="44" height="2.5" fill="#A8C4DC" rx="1"/>
        </svg>
      </a>"""

FOOTER_OLD = """          <div class="logo__mark">ВДТС</div>"""

FOOTER_NEW = """          <svg class="logo__svg logo__svg--footer" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 148 52" width="88" height="31" aria-hidden="true">
            <text x="0" y="38" font-family="Manrope, system-ui, sans-serif" font-size="40" font-weight="800" letter-spacing="-1.6" fill="#FFFFFF">ВДТ</text>
            <rect x="0" y="46" width="44" height="2.5" fill="#A8C4DC" rx="1"/>
          </svg>"""

INTER = (
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700'
    '&display=swap" rel="stylesheet">'
)
MANROPE = (
    '<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@800'
    '&display=swap" rel="stylesheet">'
)

skip = {"index.html"}
files = [p for p in base.glob("*.html") if p.name not in skip]

for path in files:
    text = path.read_text(encoding="utf-8")
    orig = text

    if HEADER_OLD in text:
        text = text.replace(HEADER_OLD, HEADER_NEW)
    if FOOTER_OLD in text:
        text = text.replace(FOOTER_OLD, FOOTER_NEW)
    if INTER in text:
        text = text.replace(INTER, MANROPE)
    elif MANROPE not in text:
        text = text.replace(
            '<link rel="stylesheet" href="css/styles.css">',
            MANROPE + '\n  <link rel="stylesheet" href="css/styles.css">',
        )

    if text != orig:
        path.write_text(text, encoding="utf-8")
        print("updated:", path.name)
    else:
        print("skipped:", path.name)
