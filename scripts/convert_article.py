# scripts/convert_article.py
# Converts a markdown file to HTML using front matter.
# Requires: pip install markdown pyyaml

import sys, re, pathlib
import markdown
import yaml

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

    # simple wrapper; swap to a template later if you like
    html = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<link rel="stylesheet" href="/stylesheet.css">
</head><body><main>
{html_body}
</main></body></html>"""

    out_file = ROOT / output_path
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")
    print(f"✅ Wrote {out_file.relative_to(ROOT)}")

if __name__ == "__main__":
    main()