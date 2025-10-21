# scripts/convert_article.py
# Converts a markdown file to HTML using front matter.
# Requires: pip install markdown pyyaml

import sys, re, pathlib, os, textwrap
import markdown
import yaml
from html import escape

ROOT = pathlib.Path(__file__).resolve().parents[1]

def parse_front_matter(text: str):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise SystemExit("Missing front matter block at top of file (--- ... ---).")
    fm = yaml.safe_load(m.group(1)) or {}
    body = m.group(2)
    return fm, body

def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python scripts/convert_article.py content/drafts/your-file.md")

    md_path = ROOT / sys.argv[1]
    if not md_path.exists():
        raise SystemExit(f"Markdown file not found: {md_path}")

    raw = md_path.read_text(encoding="utf-8")
    fm, md_body = parse_front_matter(raw)

    title = fm.get("title", md_path.stem)
    output_path = fm.get("output_path")
    if not output_path:
        raise SystemExit(
            "Front matter must include an 'output_path', e.g.\n"
            "---\n"
            "title: My Post\n"
            "output_path: about/essays/my-post.html\n"
            "---"
        )

    html_body = markdown.markdown(md_body, extensions=["extra", "toc"])

    out_file = ROOT / output_path
    out_file.parent.mkdir(parents=True, exist_ok=True)

    lang = fm.get("lang", "en-UK")
    stylesheet_href = os.path.relpath(ROOT / "stylesheet.css", out_file.parent)
    home_href = os.path.relpath(ROOT / "index.html", out_file.parent)

    analytics_snippet = """<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-169187972-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-169187972-1');
</script>"""

    body_with_indent = textwrap.indent(html_body.strip(), "                ")

    html = f"""<!DOCTYPE html>
<html lang="{lang}">
    <head>
        {analytics_snippet}
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="stylesheet" href="{stylesheet_href}" />
        <title>{escape(title)}</title>
    </head>
    <body>
        <div id>
            <div id="content">
                <p><a href="{home_href}">← Home</a></p>
{body_with_indent}
            </div>
        </div>
    </body>
</html>"""

    out_file.write_text(html, encoding="utf-8")
    print(f"✅ Wrote {out_file.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
