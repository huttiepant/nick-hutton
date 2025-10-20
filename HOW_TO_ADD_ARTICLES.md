# How to Add New Articles to Your Blog

This guide shows you how to easily write new articles in Markdown and convert them to HTML for your website.

## Quick Start (3 Simple Steps)

### 1. Install Python dependency (one-time setup)
```bash
pip install markdown
```

### 2. Write your article in Markdown
Create a new `.md` file (like `my_new_article.md`) and write your content. See `example_article.md` for reference.

**Markdown is simple:**
- `# Title` → Creates an h2 heading (main title)
- `## Subtitle` → Creates an h3 heading (section title)
- `### Smaller heading` → Creates an h4 heading
- Just write paragraphs normally (no tags needed!)
- `**bold**` → **bold text**
- `*italic*` → *italic text*
- `[link text](url)` → creates a link

### 3. Convert to HTML
```bash
python3 convert_article.py your_article.md -o "Category/Essays/Article title.html"
```

## Examples

### Example 1: Add a Product Management essay
```bash
# Write your article
nano my_pm_thoughts.md

# Convert it
python3 convert_article.py my_pm_thoughts.md -o "product-management/essays/my-pm-thoughts.html"
```

### Example 2: Add an About essay
```bash
python3 convert_article.py my_story.md -o "about/essays/my-story.html"
```

### Example 3: Specify a custom page title
```bash
python3 convert_article.py article.md -o "education/essays/new-essay.html" -t "Custom Page Title"
```

## Your Categories

Based on your current site structure:
- `about/essays/`
- `education/essays/`
- `product-management/essays/`
- `products/essays/`

## Tips

1. **Keep your Markdown files**: Store them in a `drafts/` folder so you can edit them later
2. **Preview**: The script will tell you where it created the HTML file
3. **Stylesheet path**: The script automatically calculates the correct path to `stylesheet.css`
4. **Title**: If you don't specify `-t`, it uses your first heading as the page title

## Markdown Cheat Sheet

```markdown
# Main Title (h2)

## Section Title (h3)

### Subsection (h4)

Regular paragraph text.

**bold text**
*italic text*

Lists need a blank line before them:

- Bullet point
- Another point

Numbered lists too:

1. Numbered item
2. Another item

[Link text](https://example.com)
```

## Next Steps

1. Try converting the example: `python3 convert_article.py example_article.md -o "test.html"`
2. Write your next article in Markdown
3. Convert it and publish!

Way easier than writing HTML by hand! 🎉
