"""Crawl a small docs section and save RAG-ready chunks as JSONL.

Usage:
    pip install -r requirements.txt
    export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
    python docs_to_rag_chunks.py

Cost: $0.002 per converted page; capped at 10 pages here (max $0.02).
The run is capped with max_total_charge_usd, so it cannot cost more than $0.10.
"""
import os
import sys
from decimal import Decimal

from apify_client import ApifyClient

ACTOR_ID = "cleandata-labs/url-to-markdown"
MAX_COST_USD = Decimal("0.10")

RUN_INPUT = {
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
    "includeLinks": False
}


def run_actor(run_input: dict) -> list[dict]:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set the APIFY_TOKEN environment variable first "
                 "(Apify Console > Settings > API & Integrations).")
    client = ApifyClient(token)
    run = client.actor(ACTOR_ID).call(run_input=run_input, max_total_charge_usd=MAX_COST_USD)
    if run is None:
        sys.exit("The run could not be started.")
    print(f"Run {run.id} finished: {run.status}", file=sys.stderr)
    return list(client.dataset(run.default_dataset_id).iterate_items())


def main() -> None:
    items = run_actor(RUN_INPUT)
    import json

    os.makedirs("output", exist_ok=True)
    path = os.path.join("output", "chunks.jsonl")
    count = 0
    with open(path, "w", encoding="utf-8") as f:
        for item in items:
            if item.get("error"):
                continue
            for chunk in item.get("chunks") or []:
                record = {"id": f"{item['finalUrl']}#{chunk['index']}", "url": item["finalUrl"],
                          "title": item.get("title"), "text": chunk["text"],
                          "approxTokens": chunk.get("approxTokens")}
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                count += 1
    print(f"Wrote {count} chunks from {len(items)} rows to {path}")


if __name__ == "__main__":
    main()
