"""Convert one or more web pages to Markdown files in ./output.

Usage:
    pip install -r requirements.txt
    export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
    python page_to_markdown.py

Cost: $0.002 per converted page (2 pages = $0.004).
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
        "https://docs.apify.com/platform/actors",
        "https://en.wikipedia.org/wiki/Markdown"
    ],
    "outputFormats": [
        "markdown"
    ],
    "maxCharacters": 20000
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
    import re

    os.makedirs("output", exist_ok=True)
    for item in items:
        if item.get("error"):
            print(f"Not converted (free): {item.get('url')}: {item['error']}")
            continue
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", item["finalUrl"].split("://", 1)[-1]).strip("-")[:80]
        path = os.path.join("output", f"{slug}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# {item.get('title') or item['finalUrl']}\n\nSource: {item['finalUrl']}\n\n")
            f.write(item["markdown"])
        print(f"{path}  ~{item.get('approxTokens')} tokens")


if __name__ == "__main__":
    main()
