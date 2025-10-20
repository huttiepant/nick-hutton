#!/usr/bin/env python3
"""
Simple Markdown to HTML converter for your blog.
Converts Markdown articles to HTML matching your site's style.
"""

import argparse
import os
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    print("Error: 'markdown' package not found.")
    print("Install it with: pip install markdown")
    sys.exit(1)


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en-UK">
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-169187972-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'UA-169187972-1');
</script>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <link rel="stylesheet" href="{stylesheet_path}" />
        <title>{title}</title>
    </head>
    <body>
        <div id>
            <div id="content">
{content}
            </div>
        </div>
    </body>
</html>"""


def calculate_stylesheet_path(output_path):
    """Calculate relative path to stylesheet.css from the output HTML file."""
    output_path = Path(output_path).resolve()
    workspace = Path.cwd()
    stylesheet = workspace / "stylesheet.css"
    
    try:
        relative = os.path.relpath(stylesheet, output_path.parent)
        return relative
    except ValueError:
        # If on different drives on Windows, use absolute path
        return str(stylesheet)


def convert_markdown_to_html(markdown_file, output_file, title=None):
    """Convert a Markdown file to HTML using the site template."""
    
    # Read the Markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert Markdown to HTML
    md = markdown.Markdown(extensions=['extra'])
    html_content = md.convert(md_content)
    
    # If no title provided, try to extract from first h1 or h2 in the markdown
    if not title:
        lines = md_content.split('\n')
        for line in lines:
            if line.startswith('# '):
                title = line.replace('# ', '').strip()
                break
            elif line.startswith('## '):
                title = line.replace('## ', '').strip()
                break
        if not title:
            title = "Invariably Unstructured"
    
    # Calculate relative path to stylesheet
    stylesheet_path = calculate_stylesheet_path(output_file)
    
    # Indent the HTML content for proper formatting
    indented_content = '\n'.join('                ' + line if line.strip() else '' 
                                  for line in html_content.split('\n'))
    
    # Generate final HTML
    final_html = HTML_TEMPLATE.format(
        stylesheet_path=stylesheet_path,
        title=title,
        content=indented_content
    )
    
    # Ensure output directory exists
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"✓ Converted: {markdown_file}")
    print(f"✓ Output: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown articles to HTML for your blog',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert a markdown file to HTML
  python convert_article.py my_article.md -o "Product management/Essays/My new article.html"
  
  # Specify a custom title
  python convert_article.py my_article.md -o "About/Essays/New essay.html" -t "My Custom Title"
        """
    )
    
    parser.add_argument('input', help='Input Markdown file')
    parser.add_argument('-o', '--output', required=True, help='Output HTML file path')
    parser.add_argument('-t', '--title', help='Page title (default: extracted from first heading)')
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)
    
    convert_markdown_to_html(args.input, args.output, args.title)


if __name__ == '__main__':
    main()
