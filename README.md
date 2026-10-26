# seo-optimizer

An AI agent skill that audits and improves a website's on-page SEO, based on Google's [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide).

Give your agent a page, a template, or a whole site, and it will check indexability, titles, meta descriptions, URLs, duplicate content, links, images, and content quality. It then reports what to fix, in priority order. It also knows what **not** to flag, so you don't waste time on SEO myths.

> Not affiliated with or endorsed by Google. This skill is a paraphrased, practical summary of [public guidance](https://developers.google.com/search/docs/fundamentals/seo-starter-guide). It cannot guarantee rankings, and neither can anyone else :D

## Features

- **Indexability first.** Checks for accidental `noindex`, blocked CSS/JS, and whether the page renders for crawlers like it does for users.
- **Guided review** of titles, meta descriptions, descriptive URLs, canonical/redirect handling, link text, `nofollow` on untrusted and user-generated links, image alt text, video pages, and intrusive ads.
- **Myth filter.** A reference list of things Google says aren't worth chasing (meta keywords, word count, heading order, TLD, E-E-A-T as a ranking factor, and more).
- **Bundled audit script** (`scripts/seo_audit.py`): standard library only, no dependencies.
- **Consistent report format** with sections: Fix first, Worth doing, Optional, and Checked and fine.
- **Fixes in the right place.** Edits go in shared layouts and templates, not page by page.

## Repository structure

```
seo-optimizer/
├── SKILL.md                          # Skill instructions and workflow
├── references/
│   └── myths-and-priorities.md       # What not to focus on + priority order
└── scripts/
    └── seo_audit.py                  # Lightweight HTML auditor
```

## Installation

### Claude.ai
Download `seo-optimizer.skill` and upload it under **Settings → Capabilities → Skills**, or click **Save skill** when the file is shown in a chat. Menu names can change, so check Anthropic's current docs if you can't find it.

### Claude Code
Copy the folder into your skills directory:

```bash
# Personal (all projects)
cp -r seo-optimizer ~/.claude/skills/

# Or per project
cp -r seo-optimizer .claude/skills/
```

### Other agents
Any agent that supports `SKILL.md`-style skills should work. Point it at the `seo-optimizer/` folder.

## Usage

Once installed, the skill triggers when you talk about SEO, even without the word itself. For example:

- "Why isn't my site showing up on Google?"
- "Review the meta tags in `index.html`."
- "Improve the SEO of my product pages."
- "Write alt text for the images in this template."
- "Audit this repo for search visibility problems."

### Running the audit script directly

```bash
# One file
python scripts/seo_audit.py path/to/page.html

# Every .html file in a folder, as JSON
python scripts/seo_audit.py path/to/site/ --format json

# A live page (requires network access)
python scripts/seo_audit.py https://example.com/page
```

Example output:

```
== page.html
  [HIGH] Missing or empty <title>
      -> Add a unique, concise title that accurately describes the page.
  [MEDIUM] Image without alt attribute: a.jpg
      -> Add descriptive alt text (alt="" only if purely decorative).
  [LOW] Generic link text 'click here' -> /x
      -> Use anchor text that says what the linked page contains.
```

Severity levels are `high`, `medium`, `low`, and `info`.

## What the script checks (and what it doesn't)

| Checks | Deliberately ignores |
|---|---|
| Missing or empty `<title>` | Number and order of headings |
| Missing meta description | Meta keywords tag |
| `noindex` in robots meta | Content length / word count |
| Images with no or generic `alt` | Keywords in domain or URL |
| Generic link text ("click here") | TLD choice |
| Opaque ID-style URL segments | Duplicate content "penalties" |
| Missing canonical (info only) | E-E-A-T |

The script is a starting point and reads static HTML only. Template files (Razor, Jinja, JSX, etc.) and JavaScript-rendered content should be reviewed by hand using the checklist in `SKILL.md`. The 70-character title warning is a heuristic, not a rule from Google's guide.

## Limitations

- It can't check rankings, traffic, or whether a page is actually indexed. Use [Google Search Console](https://search.google.com/search-console) and the `site:` search operator for that.
- SEO changes can take hours to months to show up. Wait a few weeks before judging results.
- It does not cover structured data, international SEO, site migrations, or Core Web Vitals in depth.

## Contributing

Issues and pull requests are welcome. Good contributions include:

- New checks that are backed by official Google guidance (please link the source).
- Parsers for template languages.
- Test fixtures with real-world HTML.

## Credits

Based on Google Search Central's *Search Engine Optimization (SEO) Starter Guide*. Read the original for full detail.

## License

Add your license here (for example, MIT) and include a `LICENSE` file.
