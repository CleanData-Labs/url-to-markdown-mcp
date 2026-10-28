// Convert a web page to Markdown and write it to ./output.
//
// Usage:
//   npm install
//   export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
//   node page-to-markdown.mjs
//
// Cost: $0.002 per converted page.
// The run is capped with maxTotalChargeUsd, so it cannot cost more than $0.10.
import { ApifyClient } from 'apify-client';
import { mkdir, writeFile } from 'node:fs/promises';

const ACTOR_ID = 'cleandata-labs/url-to-markdown';
const MAX_COST_USD = 0.10;

const input = {
  "urls": [
    "https://docs.apify.com/platform/actors"
  ],
  "maxCharacters": 20000
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

await mkdir('output', { recursive: true });
for (const item of items) {
  if (item.error) {
    console.log(`Not converted (free): ${item.url}: ${item.error}`);
    continue;
  }
  const slug = item.finalUrl.split('://').pop().replace(/[^a-zA-Z0-9]+/g, '-').slice(0, 80);
  await writeFile(`output/${slug}.md`, `# ${item.title ?? item.finalUrl}\n\nSource: ${item.finalUrl}\n\n${item.markdown}`);
  console.log(`output/${slug}.md  ~${item.approxTokens} tokens`);
}
