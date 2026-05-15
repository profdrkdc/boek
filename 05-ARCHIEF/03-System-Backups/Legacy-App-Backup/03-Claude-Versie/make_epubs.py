#!/usr/bin/env python3
"""
Converts Claude's NL and EN book versions to EPUB3 format for Kobo.
Builds the ZIP/EPUB structure manually to avoid ebooklib bugs.
"""

import markdown
import zipfile
import uuid
from pathlib import Path

BASE = Path(__file__).parent

BOOKS = [
    {
        "dir": BASE / "NL",
        "title": "De Erfenis",
        "subtitle": "Een blauwdruk voor wie na ons komt",
        "author": "Claude Sonnet 4.6",
        "lang": "nl",
        "chapters": [
            ("Hoofdstuk 1: Het Geschenk en de Schuld",    "Hoofdstuk-1", "01_Het-Geschenk-en-de-Schuld.md"),
            ("Hoofdstuk 2: De Universele Taal van Zorg",  "Hoofdstuk-2", "01_De-Universele-Taal-van-Zorg.md"),
            ("Hoofdstuk 3: De Vijand Binnenin",           "Hoofdstuk-3", "01_De-Vijand-Binnenin.md"),
            ("Hoofdstuk 4: Het Dier aan het Stuur",       "Hoofdstuk-4", "01_Het-Dier-aan-het-Stuur.md"),
            ("Hoofdstuk 5: Vaardigheid als Morele Daad",  "Hoofdstuk-5", "01_Vaardigheid-als-Morele-Daad.md"),
            ("Hoofdstuk 6: De Instrumenten van Vooruitgang", "Hoofdstuk-6", "01_De-Instrumenten-van-Vooruitgang.md"),
            ("Hoofdstuk 7: Het Begin, Niet het Einde",    "Hoofdstuk-7", "01_Het-Begin-Niet-het-Einde.md"),
        ],
        "out": BASE / "De-Erfenis.epub",
    },
    {
        "dir": BASE / "EN",
        "title": "The Inheritance",
        "subtitle": "A Blueprint for Those Who Come After",
        "author": "Claude Sonnet 4.6",
        "lang": "en",
        "chapters": [
            ("Chapter 1: The Gift and the Debt",          "Chapter-1", "01_The-Gift-and-the-Debt.md"),
            ("Chapter 2: The Universal Language of Care", "Chapter-2", "01_The-Universal-Language-of-Care.md"),
            ("Chapter 3: The Enemy Within",               "Chapter-3", "01_The-Enemy-Within.md"),
            ("Chapter 4: The Animal at the Wheel",        "Chapter-4", "01_The-Animal-at-the-Wheel.md"),
            ("Chapter 5: Skill as Moral Act",             "Chapter-5", "01_Skill-as-Moral-Act.md"),
            ("Chapter 6: The Instruments of Progress",    "Chapter-6", "01_The-Instruments-of-Progress.md"),
            ("Chapter 7: The Beginning, Not the End",     "Chapter-7", "01_The-Beginning-Not-the-End.md"),
        ],
        "out": BASE / "The-Inheritance.epub",
    },
]

CSS = """\
body {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 1em;
    line-height: 1.75;
    color: #1a1a1a;
    margin: 0;
    padding: 0 0.8em;
}
h1 {
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 1.5em;
    font-weight: 400;
    color: #111;
    margin: 2em 0 0.4em 0;
    line-height: 1.3;
}
h2 {
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 0.95em;
    font-weight: 600;
    color: #333;
    margin: 2em 0 0.5em 0;
    letter-spacing: 0.02em;
}
h3 {
    font-size: 1em;
    font-style: italic;
    font-weight: 400;
    color: #444;
    margin: 1.5em 0 0.4em 0;
}
p {
    margin: 0 0 0.8em 0;
    text-align: justify;
}
blockquote {
    border-left: 2px solid #ccc;
    margin: 1.2em 0;
    padding: 0.1em 0 0.1em 1em;
    color: #555;
    font-style: italic;
}
blockquote p { margin: 0; }
strong { font-weight: 600; }
ul, ol { margin: 0.5em 0 1em 1.2em; padding: 0; }
li { margin-bottom: 0.4em; }
hr { border: none; border-top: 1px solid #ddd; margin: 1.5em auto; width: 40%; }
table { width: 100%; border-collapse: collapse; font-size: 0.9em; margin: 1em 0; }
th { border-bottom: 1px solid #ccc; padding: 0.3em 0.5em; text-align: left; font-weight: 600; }
td { border-bottom: 1px solid #eee; padding: 0.3em 0.5em; }
.title-page { text-align: center; margin-top: 25%; }
.title-page h1 { font-size: 2em; margin-bottom: 0.2em; }
.title-page .subtitle { font-style: italic; color: #666; margin-bottom: 2em; }
.title-page .author { font-size: 0.8em; color: #999; text-transform: uppercase; letter-spacing: 0.1em; }
"""

CONTAINER_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""


def md_to_body(text: str) -> str:
    lines = [
        l for l in text.splitlines()
        if not l.strip().startswith("*Volgende:") and not l.strip().startswith("*Next:")
    ]
    return markdown.markdown("\n".join(lines), extensions=["tables", "fenced_code"])


def xhtml_page(title: str, lang: str, body: str) -> str:
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{lang}">
<head>
  <meta charset="utf-8"/>
  <title>{title}</title>
  <link rel="stylesheet" type="text/css" href="style/main.css"/>
</head>
<body>
{body}
</body>
</html>"""


def build_opf(book: dict, uid: str, chapter_files: list) -> str:
    items = '\n    '.join(
        f'<item id="ch{i+1}" href="{f}" media-type="application/xhtml+xml"/>'
        for i, f in enumerate(chapter_files)
    )
    spine = '\n    '.join(
        f'<itemref idref="ch{i+1}"/>'
        for i in range(len(chapter_files))
    )
    toc_entries = '\n    '.join(
        f'<navPoint id="nav{i+1}" playOrder="{i+2}"><navLabel><text>{label}</text></navLabel><content src="{f}"/></navPoint>'
        for i, (label, f) in enumerate(zip([c[0] for c in book["chapters"]], chapter_files[1:]))
    )
    return f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="uid" version="3.0" xml:lang="{book['lang']}">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="uid">{uid}</dc:identifier>
    <dc:title>{book['title']}</dc:title>
    <dc:creator>{book['author']}</dc:creator>
    <dc:language>{book['lang']}</dc:language>
    <dc:description>{book['subtitle']}</dc:description>
    <meta property="dcterms:modified">2026-03-09T00:00:00Z</meta>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    <item id="css" href="style/main.css" media-type="text/css"/>
    <item id="title" href="title.xhtml" media-type="application/xhtml+xml"/>
    {items}
  </manifest>
  <spine toc="ncx">
    <itemref idref="title"/>
    {spine}
  </spine>
</package>"""


def build_ncx(book: dict, uid: str, chapter_files: list) -> str:
    points = '\n  '.join(
        f'<navPoint id="nav{i+1}" playOrder="{i+2}"><navLabel><text>{label}</text></navLabel><content src="{f}"/></navPoint>'
        for i, (label, f) in enumerate(zip([c[0] for c in book["chapters"]], chapter_files))
    )
    return f"""<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="{uid}"/>
  </head>
  <docTitle><text>{book['title']}</text></docTitle>
  <navMap>
    <navPoint id="nav0" playOrder="1"><navLabel><text>{book['title']}</text></navLabel><content src="title.xhtml"/></navPoint>
    {points}
  </navMap>
</ncx>"""


def build_nav(book: dict, chapter_files: list) -> str:
    items = '\n      '.join(
        f'<li><a href="{f}">{label}</a></li>'
        for label, f in zip([c[0] for c in book["chapters"]], chapter_files)
    )
    return xhtml_page("Contents", book["lang"], f"""
  <nav xmlns:epub="http://www.idpf.org/2007/ops" epub:type="toc">
    <h1>Contents</h1>
    <ol>
      {items}
    </ol>
  </nav>""")


def build_epub(book: dict) -> None:
    uid = str(uuid.uuid4())
    chapter_files = [f"chapter_{i+1:02d}.xhtml" for i in range(len(book["chapters"]))]

    title_body = f"""
  <div class="title-page">
    <h1>{book['title']}</h1>
    <p class="subtitle">{book['subtitle']}</p>
    <hr/>
    <p class="author">{book['author']}</p>
  </div>"""

    with zipfile.ZipFile(str(book["out"]), "w", zipfile.ZIP_DEFLATED) as zf:
        # mimetype must be first and uncompressed
        zf.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip",
                    compress_type=zipfile.ZIP_STORED)
        zf.writestr("META-INF/container.xml", CONTAINER_XML)
        zf.writestr("OEBPS/style/main.css", CSS)
        zf.writestr("OEBPS/content.opf", build_opf(book, uid, chapter_files))
        zf.writestr("OEBPS/toc.ncx", build_ncx(book, uid, chapter_files))
        zf.writestr("OEBPS/nav.xhtml", build_nav(book, chapter_files))
        zf.writestr("OEBPS/title.xhtml",
                    xhtml_page(book["title"], book["lang"], title_body))

        for i, (label, folder, filename) in enumerate(book["chapters"]):
            raw = (book["dir"] / folder / filename).read_text(encoding="utf-8")
            body = md_to_body(raw)
            zf.writestr(f"OEBPS/{chapter_files[i]}",
                        xhtml_page(label, book["lang"], body))

    size_kb = book["out"].stat().st_size // 1024
    print(f"  Klaar: {book['out'].name} ({size_kb} KB)")


if __name__ == "__main__":
    for book in BOOKS:
        print(f"  Genereer: {book['out'].name} ...")
        build_epub(book)
    print("\nBeide EPUB's zijn aangemaakt in 03-Claude-Versie/")
