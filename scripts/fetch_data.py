#!/usr/bin/env python3
"""
Fetch recent eBird observations for Burrowing Owls and Roseate Spoonbills
within 10 miles of Koreshan State Park, Estero FL, and save to data/observations.json.

Called by GitHub Actions twice daily.
Requires environment variable: EBIRD_API_KEY
"""

import os
import sys
import json
import requests
from datetime import datetime, timezone

# ── Configuration ────────────────────────────────────────────────
API_KEY = os.environ.get("EBIRD_API_KEY", "").strip()
if not API_KEY:
    print("ERROR: EBIRD_API_KEY environment variable is not set.", file=sys.stderr)
    sys.exit(1)

CENTER_LAT = 26.4317      # Koreshan State Park, Estero FL
CENTER_LNG = -81.8187
DIST_KM    = 32           # 20 miles ≈ 32.19 km
BACK_DAYS  = 3            # Look back this many days (eBird max is 30)
MAX_RESULTS = 10000       # eBird hard max

# species code → display info
SPECIES = {
    "burowl": {
        "name":  "Burrowing Owl",
        "color": "#8B4513",
    },
    "rosspo1": {
        "name":  "Roseate Spoonbill",
        "color": "#FF69B4",
    },
    "limpki": {
        "name":  "Limpkin",
        "color": "#D2691E",
    },
}

BASE_URL = "https://api.ebird.org/v2/data/obs/geo/recent"
HEADERS  = {"X-eBirdApiToken": API_KEY}

# ── Fetch ────────────────────────────────────────────────────────
all_observations: list[dict] = []

for code, info in SPECIES.items():
    url    = f"{BASE_URL}/{code}"
    params = {
        "lat":               CENTER_LAT,
        "lng":               CENTER_LNG,
        "dist":              DIST_KM,
        "back":              BACK_DAYS,
        "maxResults":        MAX_RESULTS,
        "includeProvisional": "true",
    }

    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
        resp.raise_for_status()
        obs_list: list[dict] = resp.json()

    except requests.exceptions.HTTPError as exc:
        status = exc.response.status_code if exc.response else "?"
        print(f"  ✗ HTTP {status} for {info['name']}: {exc}", file=sys.stderr)
        continue
    except requests.exceptions.RequestException as exc:
        print(f"  ✗ Request error for {info['name']}: {exc}", file=sys.stderr)
        continue

    # Attach display metadata
    for obs in obs_list:
        obs["displayName"] = info["name"]
        obs["markerColor"] = info["color"]

    all_observations.extend(obs_list)
    print(f"  ✓ {info['name']}: {len(obs_list)} observation(s) found")

# ── Write JSON ───────────────────────────────────────────────────
output = {
    "lastUpdated":  datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "centerLat":    CENTER_LAT,
    "centerLng":    CENTER_LNG,
    "distKm":       DIST_KM,
    "backDays":     BACK_DAYS,
    "observations": all_observations,
}

os.makedirs("data", exist_ok=True)
output_path = os.path.join("data", "observations.json")

with open(output_path, "w", encoding="utf-8") as fh:
    json.dump(output, fh, indent=2, ensure_ascii=False)

print(f"\n  ✓ Wrote {len(all_observations)} total observation(s) → {output_path}")