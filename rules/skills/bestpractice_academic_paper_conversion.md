# Skill: Download and Convert Academic Papers

Best practices for downloading academic papers from arXiv and converting them to machine-readable markdown format.

## When to Use

- Building a paper corpus for a research project
- Need to read paper content programmatically (LLM analysis, hypothesis generation, etc.)
- Creating a local knowledge base from a researcher's publication list

## Workflow Overview

1. **Build a paper index** (`index.json`) with metadata
2. **Find arXiv IDs** for papers that don't have them
3. **Download and convert** to markdown (HTML preferred, PDF fallback)
4. **Quality check** — verify correct paper downloaded, check for duplicates

## Step 1: Build the Paper Index

Start from the researcher's lab website publication page (most reliable) or Google Scholar. Create `index.json` with structured entries:

```json
{
  "id": "P01",
  "title": "Full paper title",
  "authors": "Author1, Author2, ...",
  "journal": "Journal Name Volume, Pages",
  "year": 2024,
  "arxiv_id": "2401.12345",
  "role": "first_author",
  "status": "pending"
}
```

### Source priority for publication lists
1. **Lab/group website** — curated, grouped by year, often has arXiv links
2. **Google Scholar** — complete but may include papers where researcher is minor contributor
3. **Semantic Scholar API** — programmatic access, good metadata

### Pitfall: Google Scholar anti-scraping
Google Scholar blocks automated scraping. Workarounds:
- Ask the user to paste the page content directly
- Use the browser extension if available
- Use Semantic Scholar API as fallback

## Step 2: Find arXiv IDs

For papers without known arXiv IDs, search using Tavily:

```bash
cd adhoc_jobs/tavily_skill && .venv/bin/python -m tavily_skill search 'arXiv preprint "<exact paper title>"' \
  --max-results 6 --answer advanced --stdout
```

### Key practices
- Use the **exact paper title** in quotes — most reliable signal
- Add `--answer advanced` to get Tavily's aggregated answer which often contains the arXiv ID
- Do NOT use `--include-domain arxiv.org` — it over-restricts and misses results
- Extract arXiv IDs with regex from both the answer and individual result URLs/content

### Pitfall: Duplicate arXiv IDs
After bulk searching, **always check for duplicate arXiv IDs** across papers:
```python
from collections import Counter
ids = [p['arxiv_id'] for p in papers if p.get('arxiv_id')]
dups = {k: v for k, v in Counter(ids).items() if v > 1}
```
Common causes of duplicates:
- Search returns a related paper instead of the target (e.g., same material system, similar title)
- A Nature Materials "News & Views" commentary gets matched to the original research paper's arXiv
- Two papers in the same series get the same ID due to fuzzy matching

### Pitfall: Wrong paper matched
After finding an arXiv ID, consider verifying for critical papers:
- Check the arXiv abstract page to confirm title and authors match
- For HTML-available papers, the first few lines of extracted content reveal the actual title

## Step 3: Download and Convert

### Strategy: HTML first, PDF fallback

**Check HTML availability:**
```bash
curl -sI "https://arxiv.org/html/{arxiv_id}" | head -1
# HTTP/2 200 = HTML available
# HTTP/2 404 = PDF only
```

**HTML path (preferred):** Use Tavily extract for clean markdown:
```bash
cd adhoc_jobs/tavily_skill && .venv/bin/python -m tavily_skill extract "https://arxiv.org/html/{arxiv_id}" \
  --format markdown --stdout
```
Advantages: cleaner text, better equation rendering, proper section structure.

**PDF path (fallback):** Download PDF then convert with markitdown:
```bash
curl -L -o raw/{id}_{arxiv_id}.pdf "https://arxiv.org/pdf/{arxiv_id}"
```
```python
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert('path/to/paper.pdf')
```

### File organization
```
contexts/papers/
├── index.json              # Paper metadata index
├── P01_1809.07437.md       # Converted markdown (with YAML frontmatter)
├── P02_2105.06429.md
├── ...
└── raw/                    # Original PDFs (gitignored)
    ├── P01_1809.07437.pdf
    └── ...
```

### Naming convention
- `{paper_id}_{arxiv_id}.md` — e.g., `P01_1809.07437.md`
- Paper IDs use zero-padded two-digit numbers: P01, P02, ..., P49

### YAML frontmatter
Every markdown file starts with:
```yaml
---
title: "Paper Title"
arxiv_id: "2401.12345"
authors: "Author1, Author2, ..."
publication: "Journal Volume, Pages (Year)"
year: 2024
---
```

## Step 4: Quality Checks

1. **File size check**: MD files should be >500 bytes (a few KB minimum for real papers)
2. **Duplicate ID check**: Run after bulk arXiv ID search
3. **Title verification**: For papers downloaded via arXiv ID search, spot-check that the downloaded content matches the expected paper
4. **Content-header match**: After conversion, verify that the first few lines of the markdown body match the expected paper title. In practice, ~8% of auto-searched arXiv IDs were wrong, leading to completely unrelated papers being downloaded.
5. **Rate limiting**: Add 1-second delay between arXiv downloads to be respectful

### Critical: Wrong arXiv ID failure mode

The most dangerous failure is downloading the correct file for a wrong arXiv ID — the PDF downloads successfully, converts to markdown without errors, and has a reasonable file size. The only way to catch this is by reading the content. In a batch workflow, the paper-reading agents serve as the last quality gate. When an agent reports a content mismatch, immediately:
- Remove the wrong file
- Set `arxiv_id: null` and `status: "wrong_arxiv_id"` in index.json
- Do NOT retry with a different search — the paper may genuinely lack an arXiv preprint

## Batch Processing Scripts

The project includes two helper scripts in `scripts/`:
- `search_arxiv_ids.py` — Bulk search for missing arXiv IDs via Tavily
- `download_papers.py` — Bulk download and convert papers with arXiv IDs

Both read/write `contexts/papers/index.json` and support `--only-missing` flag.

## Papers Without arXiv Preprints

Some papers won't have arXiv versions:
- Journal-specific commentaries (Nature Materials "News & Views", etc.)
- Very old papers predating arXiv adoption in the field
- Some conference proceedings

Mark these with `"status": "skip_no_preprint"` in index.json. If full text is still needed, check:
- Publisher open access (some journals have delayed OA)
- Author's institutional repository
- DOI-based access through the user's institution

## Lessons Learned

1. **arXiv HTML is only available for newer papers** — roughly post-2023 submissions. Older papers are PDF-only.
2. **markitdown works well for physics papers** — equations come through as LaTeX, figures are referenced, and section structure is preserved.
3. **Tavily extract for HTML is very clean** — better than downloading raw HTML and parsing yourself.
4. **The biggest time sink is arXiv ID discovery**, not download/conversion. Invest in good search queries upfront.
5. **Always verify after bulk operations** — duplicate IDs and wrong-paper matches are the most common failure modes.
