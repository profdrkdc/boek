#!/usr/bin/env python3
"""
Converts Claude's NL and EN book versions to nicely formatted PDFs.
"""

import markdown
from weasyprint import HTML, CSS
from pathlib import Path

BASE = Path(__file__).parent

# Boek-definities: (map, bestandsvolgorde, uitvoernaam, taal)
BOOKS = [
    {
        "dir": BASE / "NL",
        "title": "De Erfenis",
        "subtitle": "Een blauwdruk voor wie na ons komt",
        "author": "Claude Sonnet 4.6",
        "lang": "nl",
        "chapters": [
            ("Hoofdstuk-1", "01_Het-Geschenk-en-de-Schuld.md"),
            ("Hoofdstuk-2", "01_De-Universele-Taal-van-Zorg.md"),
            ("Hoofdstuk-3", "01_De-Vijand-Binnenin.md"),
            ("Hoofdstuk-4", "01_Het-Dier-aan-het-Stuur.md"),
            ("Hoofdstuk-5", "01_Vaardigheid-als-Morele-Daad.md"),
            ("Hoofdstuk-6", "01_De-Instrumenten-van-Vooruitgang.md"),
            ("Hoofdstuk-7", "01_Het-Begin-Niet-het-Einde.md"),
        ],
        "out": BASE / "De-Erfenis.pdf",
    },
    {
        "dir": BASE / "EN",
        "title": "The Inheritance",
        "subtitle": "A Blueprint for Those Who Come After",
        "author": "Claude Sonnet 4.6",
        "lang": "en",
        "chapters": [
            ("Chapter-1", "01_The-Gift-and-the-Debt.md"),
            ("Chapter-2", "01_The-Universal-Language-of-Care.md"),
            ("Chapter-3", "01_The-Enemy-Within.md"),
            ("Chapter-4", "01_The-Animal-at-the-Wheel.md"),
            ("Chapter-5", "01_Skill-as-Moral-Act.md"),
            ("Chapter-6", "01_The-Instruments-of-Progress.md"),
            ("Chapter-7", "01_The-Beginning-Not-the-End.md"),
        ],
        "out": BASE / "The-Inheritance.pdf",
    },
]

CSS_STYLES = CSS(string="""
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;600&display=swap');

    @page {
        size: A5;
        margin: 2.5cm 2.2cm 2.8cm 2.2cm;
        @bottom-center {
            content: counter(page);
            font-family: 'Inter', sans-serif;
            font-size: 9pt;
            color: #aaa;
        }
    }

    @page :first {
        @bottom-center { content: none; }
    }

    body {
        font-family: 'EB Garamond', Georgia, serif;
        font-size: 11.5pt;
        line-height: 1.75;
        color: #1a1a1a;
        background: white;
    }

    /* Titelpagina */
    .title-page {
        page-break-after: always;
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 85vh;
        text-align: center;
        padding-top: 30%;
    }

    .title-page h1 {
        font-family: 'Inter', 'Helvetica Neue', sans-serif;
        font-size: 28pt;
        font-weight: 300;
        letter-spacing: -0.5pt;
        margin: 0 0 0.3em 0;
        color: #111;
        border: none;
    }

    .title-page .subtitle {
        font-family: 'EB Garamond', Georgia, serif;
        font-size: 12pt;
        color: #666;
        font-style: italic;
        margin: 0 0 3em 0;
    }

    .title-page .author {
        font-family: 'Inter', sans-serif;
        font-size: 9pt;
        color: #aaa;
        letter-spacing: 2pt;
        text-transform: uppercase;
    }

    .title-page .rule {
        width: 40px;
        border: none;
        border-top: 1px solid #ddd;
        margin: 2em auto;
    }

    /* Hoofdstukken */
    .chapter {
        page-break-before: always;
    }

    h1 {
        font-family: 'Inter', 'Helvetica Neue', sans-serif;
        font-size: 18pt;
        font-weight: 400;
        color: #111;
        margin: 0 0 0.5em 0;
        padding-top: 1.5em;
        border-bottom: none;
        line-height: 1.3;
    }

    h2 {
        font-family: 'Inter', 'Helvetica Neue', sans-serif;
        font-size: 11pt;
        font-weight: 600;
        color: #333;
        margin: 2em 0 0.5em 0;
        letter-spacing: 0.3pt;
    }

    h3 {
        font-family: 'EB Garamond', Georgia, serif;
        font-size: 11.5pt;
        font-weight: 400;
        font-style: italic;
        color: #444;
        margin: 1.5em 0 0.4em 0;
    }

    p {
        margin: 0 0 0.9em 0;
        text-align: justify;
        hyphens: auto;
    }

    blockquote {
        border-left: 2px solid #ddd;
        margin: 1.5em 0 1.5em 0;
        padding: 0.2em 0 0.2em 1.2em;
        color: #555;
        font-style: italic;
    }

    blockquote p {
        margin: 0;
    }

    strong {
        font-weight: 600;
        color: #111;
    }

    em {
        font-style: italic;
    }

    ul, ol {
        margin: 0.5em 0 1em 1.2em;
        padding: 0;
    }

    li {
        margin-bottom: 0.4em;
    }

    hr {
        border: none;
        border-top: 1px solid #e0e0e0;
        margin: 2em auto;
        width: 60px;
    }

    a {
        color: inherit;
        text-decoration: none;
    }

    .chapter-nav {
        display: none;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        font-size: 10pt;
        margin: 1em 0;
    }

    th {
        font-family: 'Inter', sans-serif;
        font-size: 9pt;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5pt;
        border-bottom: 1px solid #ccc;
        padding: 0.4em 0.6em;
        text-align: left;
    }

    td {
        border-bottom: 1px solid #eee;
        padding: 0.4em 0.6em;
        vertical-align: top;
    }
""")


def md_to_html(text: str) -> str:
    return markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "nl2br"],
    )


def build_pdf(book: dict) -> None:
    parts = []

    # Titelpagina
    parts.append(f"""
    <div class="title-page">
        <h1>{book['title']}</h1>
        <p class="subtitle">{book['subtitle']}</p>
        <hr class="rule">
        <p class="author">{book['author']}</p>
    </div>
    """)

    # Hoofdstukken
    for folder, filename in book["chapters"]:
        path = book["dir"] / folder / filename
        raw = path.read_text(encoding="utf-8")
        # Strip de "Volgende: ..." navigatieregel onderaan
        lines = raw.splitlines()
        lines = [l for l in lines if not l.strip().startswith("*Volgende:") and not l.strip().startswith("*Next:")]
        raw = "\n".join(lines)
        html_body = md_to_html(raw)
        parts.append(f'<div class="chapter">{html_body}</div>')

    full_html = f"""<!DOCTYPE html>
<html lang="{book['lang']}">
<head>
  <meta charset="UTF-8">
  <title>{book['title']}</title>
</head>
<body>
{''.join(parts)}
</body>
</html>"""

    print(f"  Genereer: {book['out'].name} ...")
    HTML(string=full_html, base_url=str(book["dir"])).write_pdf(
        str(book["out"]),
        stylesheets=[CSS_STYLES],
        presentational_hints=True,
    )
    size_kb = book["out"].stat().st_size // 1024
    print(f"  Klaar: {book['out']} ({size_kb} KB)")


if __name__ == "__main__":
    for book in BOOKS:
        build_pdf(book)
    print("\nBeide PDF's zijn aangemaakt in 03-Claude-Versie/")
