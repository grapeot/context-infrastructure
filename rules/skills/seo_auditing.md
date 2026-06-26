## 元数据

- **类型**: Workflow
- **分类**: Utilities
- **适用场景**: Audit technical SEO — meta tags, structured data, Open Graph, sitemaps, robots.txt, performance, and accessibility signals.
- **上游来源**: [seo-auditing](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/seo-auditing)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# SEO Auditing

Check and fix technical SEO issues in a web project.

## Audit Checklist

### 1. Meta Tags

Every page must have:

```html
<head>
  <title>Page Title — Site Name</title>
  <meta name="description" content="155 chars max, compelling summary" />
  <link rel="canonical" href="https://example.com/page" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
</head>
```

Check for:
- [ ] Unique `<title>` per page (50-60 chars)
- [ ] Unique `<meta description>` per page (120-155 chars)
- [ ] Canonical URL set (avoids duplicate content)
- [ ] No `noindex` on pages that should be indexed

### 2. Open Graph & Social

```html
<meta property="og:title" content="Page Title" />
<meta property="og:description" content="Description for social sharing" />
<meta property="og:image" content="https://example.com/og-image.png" />
<meta property="og:url" content="https://example.com/page" />
<meta property="og:type" content="website" />
<meta name="twitter:card" content="summary_large_image" />
```

- OG image should be 1200x630px
- Test with https://developers.facebook.com/tools/debug/ and https://cards-dev.twitter.com/validator

### 3. Structured Data (JSON-LD)

Add schema markup for rich search results:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "author": { "@type": "Person", "name": "Author Name" },
  "datePublished": "2026-04-10",
  "image": "https://example.com/image.jpg"
}
</script>
```

Common types: `Article`, `Product`, `FAQPage`, `Organization`, `BreadcrumbList`

Test with: https://search.google.com/test/rich-results

### 4. Sitemap

`/sitemap.xml` should:
- List all indexable pages
- Include `<lastmod>` dates
- Exclude pages with `noindex`
- Be under 50MB / 50,000 URLs per file
- Be referenced in `robots.txt`

### 5. Robots.txt

`/robots.txt` should:
```
User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/
Sitemap: https://example.com/sitemap.xml
```

- Not block CSS/JS files (search engines need them to render)
- Not block pages you want indexed

### 6. Performance (Core Web Vitals)

| Metric | Good | Needs Work |
|--------|------|------------|
| LCP (Largest Contentful Paint) | < 2.5s | > 4.0s |
| INP (Interaction to Next Paint) | < 200ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | > 0.25 |

Key fixes:
- Compress and lazy-load images
- Preload critical fonts and CSS
- Avoid layout shifts from dynamic content
- Use `next/image` or equivalent for automatic optimization

### 7. Crawlability

- [ ] All important pages are reachable from internal links
- [ ] No orphan pages (pages with zero internal links)
- [ ] No redirect chains (A→B→C should be A→C)
- [ ] 404 pages return proper HTTP 404 status
- [ ] No broken internal links

### 8. Accessibility (SEO Signals)

- [ ] All images have `alt` text
- [ ] Heading hierarchy is correct (one `h1`, then `h2`, `h3` etc.)
- [ ] Links have descriptive text (not "click here")
- [ ] Language attribute set: `<html lang="en">`

## Quick Automated Check

```bash
# Check robots.txt
curl -s https://example.com/robots.txt

# Check sitemap
curl -s https://example.com/sitemap.xml | head -20

# Check meta tags
curl -s https://example.com | grep -E '<title>|<meta name="description"|<link rel="canonical"'

# Check HTTP status codes
curl -o /dev/null -s -w "%{http_code}" https://example.com/page
```

## Tips

- Run Lighthouse in Chrome DevTools → check SEO score
- Google Search Console is the source of truth for indexing issues
- Mobile-friendliness is a ranking factor — test on mobile viewports
- Page speed directly affects rankings — optimize Core Web Vitals
