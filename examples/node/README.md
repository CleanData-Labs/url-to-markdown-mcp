# Node.js examples

Needs Node.js 18+ and an Apify API token.

```bash
npm install
export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
node page-to-markdown.mjs
```

| Script | What it does | Cost |
|---|---|---|
| `page-to-markdown.mjs` | Convert a web page to Markdown and write it to ./output. | $0.002 per converted page. |
| `rag-chunks.mjs` | Crawl a small docs section and save RAG-ready chunks as JSONL. | $0.002 per converted page; capped at 10 pages here (max $0.02). |

Every script sets `maxTotalChargeUsd`, so a run stops before it can cost more than the cap. Files are written to `./output/` (git-ignored).
