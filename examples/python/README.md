# Python examples

Needs Python 3.10+ and an Apify API token.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
python page_to_markdown.py
```

| Script | What it does | Cost |
|---|---|---|
| `page_to_markdown.py` | Convert one or more web pages to Markdown files in ./output. | $0.002 per converted page (2 pages = $0.004). |
| `docs_to_rag_chunks.py` | Crawl a small docs section and save RAG-ready chunks as JSONL. | $0.002 per converted page; capped at 10 pages here (max $0.02). |
| `pdf_to_text.py` | Read the first pages of a PDF as Markdown and print the beginning. | 1 PDF = 1 page charge = $0.002. |

Every script sets `max_total_charge_usd`, so a run stops before it can cost more than the cap. Files are written to `./output/` (git-ignored).
