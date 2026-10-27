# -*- coding: utf-8 -*-
"""Собирает HTML со встроенным CSS для импорта в Figma (Yolbridge и др.).

Важно: data-theme меняем ТОЛЬКО у <html>, CSS-селекторы [data-theme="dark"]
не трогаем — иначе светлая тема получает тёмные токены.
"""

from pathlib import Path
import re

BASE = Path(__file__).resolve().parent.parent
CSS = (BASE / "css" / "styles.css").read_text(encoding="utf-8")
OUT = BASE / "figma-import"
OUT.mkdir(exist_ok=True)

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

THEME_BOOT_LIGHT = """<script>
(function () {
  document.documentElement.setAttribute('data-theme', 'light');
  try { localStorage.setItem('vdts_theme', 'light'); localStorage.setItem('cookies_accepted', '1'); } catch (e) {}
  var b = document.getElementById('cookieBanner');
  if (b) b.hidden = true;
  document.addEventListener('DOMContentLoaded', function () {
    document.body.classList.remove('has-cookie-banner');
  });
})();
</script>"""

THEME_BOOT_DARK = """<script>
(function () {
  document.documentElement.setAttribute('data-theme', 'dark');
  try { localStorage.setItem('vdts_theme', 'dark'); localStorage.setItem('cookies_accepted', '1'); } catch (e) {}
  var b = document.getElementById('cookieBanner');
  if (b) b.hidden = true;
  document.addEventListener('DOMContentLoaded', function () {
    document.body.classList.remove('has-cookie-banner');
  });
})();
</script>"""


def bundle_page(slug: str, src_name: str, theme: str) -> Path:
    src_path = BASE / src_name
    html = src_path.read_text(encoding="utf-8")

    # Встраиваем CSS как есть — селекторы [data-theme="dark"] не меняем
    html = html.replace(
        '<link rel="stylesheet" href="css/styles.css">',
        f"<style>\n{CSS}\n</style>",
    )

    # Меняем ТОЛЬКО атрибут у тега <html>
    html = re.sub(
        r'(<html\b[^>]*\bdata-theme=")(light|dark)(")',
        rf"\g<1>{theme}\g<3>",
        html,
        count=1,
        flags=re.IGNORECASE,
    )

    boot = THEME_BOOT_LIGHT if theme == "light" else THEME_BOOT_DARK
    if "<body>" in html and "data-theme', '" not in html.split("<body>", 1)[1][:400]:
        html = html.replace("<body>", f"<body>\n  {boot}", 1)
    else:
        # Уже был boot от прошлой сборки — заменим на правильный
        html = re.sub(
            r"<body>\s*<script>[\s\S]*?</script>",
            f"<body>\n  {boot}",
            html,
            count=1,
        )

    out_path = OUT / f"{slug}-{theme}.html"
    out_path.write_text(html, encoding="utf-8")
    return out_path


def main() -> None:
    for slug, src in PAGES:
        for theme in ("light", "dark"):
            path = bundle_page(slug, src, theme)
            print(f"OK: {path.name}")

    # Быстрая проверка: в light-файле CSS-селектор dark должен остаться dark
    sample = (OUT / "glavnaya-light.html").read_text(encoding="utf-8")
    assert 'data-theme="light"' in sample[:200], "html attr light missing"
    assert '[data-theme="dark"]' in sample, "CSS dark selector was corrupted"
    assert '[data-theme="light"] {' not in sample, "dark tokens wrongly bound to light"
    print("Check passed: light files keep [data-theme=dark] CSS selectors")
    print(f"Done: {OUT}")


if __name__ == "__main__":
    main()
