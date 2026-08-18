# TRMNL Currency Plugin

Shows USD→₹ and EUR→₹ exchange rates on a TRMNL device, as a Private Plugin
polling a JSON feed. Templates target **TRMNL X** (portrait, 4-bit grayscale)
using the framework's `lg:`/`portrait:` responsive prefixes and larger v3
typography tiers, while remaining backward-compatible with OG.

- `generate_rates.py` fetches rates from the [Frankfurter API](https://frankfurter.dev/) (ECB data, no key required) and writes `current.json`.
- `.github/workflows/update-rates.yml` runs the script daily and commits the result.
- `template.liquid` / `template--half-vertical.liquid` render the data on the device.

## Setup on TRMNL

1. Push this repo to GitHub (e.g. `harshakhegde/trmnl-currency-plugin`) and enable
   GitHub Actions so `update-rates.yml` starts committing fresh `current.json` files.
2. In the TRMNL dashboard, go to **Plugins → Private Plugin → Add New**.
3. Set **Strategy** to `Polling`.
4. Set **Polling URL** to the raw GitHub URL for `current.json`, e.g.:
   `https://raw.githubusercontent.com/<user>/trmnl-currency-plugin/main/current.json`
5. Set **Polling headers** if the repo is private (a `Authorization: token <PAT>`
   header), otherwise leave blank for a public repo.
6. Paste `template.liquid` into the **Markup** editor (and `template--half-vertical.liquid`
   into the half-vertical layout variant if you use mixed layouts).
7. Save and add the plugin to a playlist.

## Local testing

```bash
python3 generate_rates.py
```

This overwrites `current.json` with the latest rates.
