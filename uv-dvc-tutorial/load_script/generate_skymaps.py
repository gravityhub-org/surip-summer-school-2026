#!/usr/bin/env python3
"""Download LIGO skymaps for DVC tracking.

Tries GWOSC API first (as in GWOSC tutorials), falls back to LIGO DCC
when skymap_fits is missing from the API.

Run from repo root:
    uv run python load_script/generate_skymaps.py
"""

from pathlib import Path

import requests

EVENTS = {
    "GW150914": "https://dcc.ligo.org/LIGO-P1800381/public/GW150914_skymap.fits.gz",
    "GW170817": "https://dcc.ligo.org/LIGO-P1800381/public/GW170817_skymap.fits.gz",
    "GW170814": "https://dcc.ligo.org/LIGO-P1800381/public/GW170814_skymap.fits.gz",
}
OUT = Path(__file__).resolve().parents[1] / "data" / "skymaps"

OUT.mkdir(parents=True, exist_ok=True)

for event, dcc_url in EVENTS.items():
    out_path = OUT / f"{event}_skymap.fits.gz"
    if out_path.exists():
        print(f"  [cache] {event}")
        continue

    skymap_url = None
    print(f"  [fetch] {event} from GWOSC API …")
    api = f"https://gwosc.org/eventapi/json/event/{event}/"
    r = requests.get(api, timeout=30)
    r.raise_for_status()
    events = r.json().get("events", {})
    for version_key, ev in events.items():
        skymap_url = ev.get("skymap_fits")
        if skymap_url:
            break

    if not skymap_url:
        print(f"  GWOSC API has no skymap_fits for {event}, using LIGO DCC")
        skymap_url = dcc_url

    print(f"  Downloading: {skymap_url}")
    r = requests.get(skymap_url, timeout=120, stream=True)
    r.raise_for_status()
    with open(out_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"         saved → {out_path} ({out_path.stat().st_size // 1024} KB)")
