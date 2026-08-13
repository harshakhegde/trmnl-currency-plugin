#!/usr/bin/env python3
"""Fetches USD->INR and EUR->INR exchange rates and writes current.json
for TRMNL to poll. Run periodically via GitHub Actions (or cron)."""
import json
import urllib.request
from datetime import date, datetime
from pathlib import Path

HERE = Path(__file__).parent
API = "https://api.frankfurter.dev/v1/latest?base={base}&symbols=INR"


def fetch_rate(base: str) -> tuple[float, str]:
    req = urllib.request.Request(
        API.format(base=base), headers={"User-Agent": "trmnl-currency-plugin"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    return data["rates"]["INR"], data["date"]


def load_previous() -> dict:
    out = HERE / "current.json"
    if out.exists():
        return json.loads(out.read_text())
    return {}


def main():
    previous = load_previous()

    usd_inr, usd_date = fetch_rate("USD")
    eur_inr, eur_date = fetch_rate("EUR")

    result = {
        "usd_inr": round(usd_inr, 2),
        "eur_inr": round(eur_inr, 2),
        "usd_inr_prev": previous.get("usd_inr"),
        "eur_inr_prev": previous.get("eur_inr"),
        "rate_date": max(usd_date, eur_date),
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "today": date.today().isoformat(),
    }

    out = HERE / "current.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(out.read_text())


if __name__ == "__main__":
    main()
