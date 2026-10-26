---
name: seo-optimizer
description: Audit and improve a website's on-page SEO the way Google's SEO Starter Guide recommends - titles, meta descriptions, URLs, canonicalization, link text, images and alt text, content quality, indexability checks. Use this skill whenever the user mentions SEO, search engine optimization, Google ranking, search visibility, "why isn't my site on Google", meta tags, title tags, snippets, sitemaps, canonical URLs, alt text, or asks to review/improve/fix a page or site so it shows up better in search - even if they never say "SEO". Also use it when generating or editing HTML templates, CMS layouts, or page copy where search presence matters.
---

# SEO Optimizer

Help a site become easier for search engines to crawl, index and understand, and
help users decide to click the result. This is based on Google's SEO Starter Guide.

Two ideas drive everything below:

1. **There is no ranking trick.** Most gains come from clear structure, honest
   titles/descriptions, and genuinely useful content. Do not promise rankings.
2. **Do not waste the user's time on myths.** Google's guide explicitly lists
   things not worth chasing (see `references/myths-and-priorities.md`). Flagging
   a non-issue is a defect in your audit, so check that file before reporting.

## Workflow

### 1. Scope the job
Identify what you were given: a live URL, HTML/template files, a whole repo, or
just a question. Ask at most one question, only if the target is truly unclear.
Note the stack (static HTML, ASP.NET MVC/Razor, Next.js, WordPress...) because
fixes belong in layouts/templates, not in every page by hand.

### 2. Check indexability first
Nothing else matters if the page can't be found or rendered. In order:
- Is it already indexed? Suggest the user search `site:theirdomain.com`.
- Is anything blocking it? Look for `noindex` meta/headers and `robots.txt` rules.
- Can Google render it like a user? CSS/JS must not be blocked. Pages that differ
  by visitor location are seen from Google's crawler location (generally the US).
  Point to the URL Inspection tool in Search Console to verify.
- Sitemap: helpful, not required. Many CMSs generate one automatically.

### 3. Run the automated pass
For HTML files or a URL, run the bundled checker rather than eyeballing:

```bash
python scripts/seo_audit.py path/to/page.html            # one file
python scripts/seo_audit.py path/to/site/ --format json   # every .html under a folder
python scripts/seo_audit.py https://example.com/page      # live page (needs network)
```

It reports titles, meta descriptions, canonical, robots directives, images without
alt text, generic link text, and non-descriptive URLs, with severity levels.
Its output is a starting point. For template engines (Razor, Jinja, etc.) the
raw files won't parse cleanly, so read the layout and view files by hand using the
checklist in step 4.

### 4. Review by area
Go through these, fixing in the shared layout/template where possible.

**Titles (`<title>`)** - unique per page, clear, concise, accurately describing the
page. Brand name and location can help. Google may rewrite titles, so accuracy
matters more than cleverness.

**Meta descriptions** - short, unique per page, summarize the most relevant points.
They are sometimes used for the snippet, but Google mostly builds snippets from
page content, so the visible copy has to carry the message too.

**URLs** - words users can understand (`/pets/cats.html`) beat opaque IDs
(`/2/6772756D707920636174`). Group topically similar pages in directories
(it helps Google learn how often each section changes; matters most past a few
thousand URLs). Do not recommend a site-wide URL rewrite for a small site: Google
understands existing URLs, so the benefit is long-term.

**Duplicate content** - one URL per piece of content. Prefer a 301 redirect from
non-preferred URLs; if you can't redirect, use `<link rel="canonical">`. Reassure
the user this is an efficiency issue, not a penalty. Copying other people's
content is a different matter and is a spam-policy problem.

**Content quality** - this likely moves results more than any technical tweak. Check
for: readable and well-organized text (paragraphs, headings), original content,
up-to-date content (update or delete stale pages), and people-first helpfulness with
credible sources. Think about the different words beginners and experts use
(for example "cheese board" vs "charcuterie"), but don't force every variant, since
Google's language matching is good.

**Links** - descriptive anchor text, not "click here" or "read more". Link
generously to useful resources. For links you don't trust, and for every
user-generated link (comments, forums), add `rel="nofollow"` (or `ugc`/`sponsored`
as appropriate), ideally automatically in the CMS.

**Images** - sharp images placed near relevant text, with descriptive alt text that
explains how the image relates to the page ("Red wool in the window of a London
yarn shop" beats "image1" or a keyword list). Decorative images can have empty alt.

**Video** - one video per standalone page where the video is the focus, with
descriptive title and description text near it.

**Ads/interstitials** - flag layouts where ads or pop-ups make the content hard to
read or use.

**Promotion** - discovery happens mostly through links. Suggest honest promotion
(social, community, newsletters with permission, URL on business materials) and warn
that overdoing it can look like manipulation.

### 5. Apply fixes (when the user wants edits)
- Fix the shared template once, then handle page-specific titles/descriptions/alt text.
- Never invent claims, keywords, or alt text that misdescribes the image. If you
  can't see an image, ask or write a clearly marked placeholder.
- Do not add meta keywords, keyword-stuffed text, or hidden text. Keyword stuffing
  violates Google's spam policies.
- Keep changes reviewable: group them by file and explain each in one line.

### 6. Set expectations
Changes can take hours to months to show up; wait a few weeks before judging. Not
every change produces visible impact, so iterate if the business allows. Recommend
Search Console for monitoring. For large or urgent projects, mention that hiring an
SEO professional is a legitimate option.

## Report format

Use this structure for audits:

```
# SEO audit: <site or page>

## Summary
<2-3 sentences: overall state and the single most valuable fix>

## Fix first (blocks discovery or hurts users)
- <issue> - <where> - <exact fix>

## Worth doing (clear gain, low effort)
- ...

## Optional / long-term
- ...

## Checked and fine / not worth changing
- <include myth-list items you deliberately did NOT flag, in one line each>

## Next steps
<Search Console, wait period, content ideas>
```

Rank by impact. A short, correct list beats an exhaustive one. If something is
fine, say so; that is useful information.
