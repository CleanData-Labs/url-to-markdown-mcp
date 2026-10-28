// Crawl a small docs section and save RAG-ready chunks as JSONL.
//
// Usage:
//   npm install
//   export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
//   node rag-chunks.mjs
//
// Cost: $0.002 per converted page; capped at 10 pages here (max $0.02).
// The run is capped with maxTotalChargeUsd, so it cannot cost more than $0.10.
import { ApifyClient } from 'apify-client';
import { mkdir, writeFile } from 'node:fs/promises';

const ACTOR_ID = 'cleandata-labs/url-to-markdown';
const MAX_COST_USD = 0.10;

const input = {
  "urls": [
    "https://crawlee.dev/python/docs/quick-start"
  ],
  "maxCrawlDepth": 1,
  "maxPagesPerStartUrl": 10,
  "includeUrlGlobs": [
    "https://crawlee.dev/python/docs/*"
  ],
  "chunkSizeTokens": 800,
  "chunkOverlapTokens": 80,
  "includeLinks": false
};

const token = process.env.APIFY_TOKEN;
if (!token) {
  console.error('Set the APIFY_TOKEN environment variable first (Apify Console > Settings > API & Integrations).');
  process.exit(1);
}

const client = new ApifyClient({ token });
const run = await client.actor(ACTOR_ID).call(input, { maxTotalChargeUsd: MAX_COST_USD });
console.error(`Run ${run.id} finished: ${run.status}`);
const { items } = await client.dataset(run.defaultDatasetId).listItems();

const lines = [];
for (const item of items.filter((i) => !i.error)) {
  for (const chunk of item.chunks ?? []) {
    lines.push(JSON.stringify({ id: `${item.finalUrl}#${chunk.index}`, url: item.finalUrl, title: item.title, text: chunk.text }));
  }
}
await mkdir('output', { recursive: true });
await writeFile('output/chunks.jsonl', lines.join('\n') + '\n');
console.log(`Wrote ${lines.length} chunks to output/chunks.jsonl`);
