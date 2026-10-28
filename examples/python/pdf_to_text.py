"""Read the first pages of a PDF as Markdown and print the beginning.

Usage:
    pip install -r requirements.txt
    export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
    python pdf_to_text.py

Cost: 1 PDF = 1 page charge = $0.002.
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
        "https://arxiv.org/pdf/1706.03762"
    ],
    "maxPdfPages": 5
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
    for item in items:
        if item.get("error"):
            print("Not converted (free):", item["error"])
            continue
        print(f"{item.get('title')}  [{item.get('fetchedWith')}, ~{item.get('approxTokens')} tokens]\n")
        print(item["markdown"][:1500])


if __name__ == "__main__":
    main()
