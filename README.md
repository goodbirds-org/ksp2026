# 🦉 Koreshan State Park and Vicinity — Selected Birds

A live, auto-updating web map tracking recent **Burrowing Owl** and **Roseate Spoonbill**
sightings within 10 miles of Koreshan State Park in Estero, Florida — powered by the
[eBird API](https://documenter.getpostman.com/view/664302/S1ENwy59) and hosted on GitHub Pages.

---

## 🗺️ Live Map

**[View the Map →](https://your-github-username.github.io/your-repo-name/)**

> Replace the link above with your actual GitHub Pages URL after setup.

---

## 🐦 Target Species

| Marker | Species | eBird Code | Notes |
|--------|---------|-----------|-------|
| 🟤 Brown | [Burrowing Owl](https://ebird.org/species/burowl) | `burowl` | Year-round resident; nests in open grasslands and suburban lawns across SW Florida |
| 🩷 Pink | [Roseate Spoonbill](https://ebird.org/species/rosspo1) | `rosspo1` | Wading bird with unmistakable spatula-shaped bill; frequents estuaries and mangroves |

---

## 📍 Search Area

| Parameter | Value |
|-----------|-------|
| **Center** | Koreshan State Park, Estero, FL (26.4317°N, 81.8187°W) |
| **Radius** | 10 miles (≈ 16 km) |
| **Lookback window** | Past 2 days |
| **Data source** | [eBird](https://ebird.org) / Cornell Lab of Ornithology |

The map displays three reference rings at **1 mile**, **5 miles**, and **10 miles**
from the park entrance.

---

## 🔄 Auto-Update Schedule

Data is refreshed automatically via **GitHub Actions** twice daily:

| Run | Eastern Time | UTC |
|-----|-------------|-----|
| Morning | ~4:00 AM ET | 09:00 UTC |
| Afternoon | ~1:00 PM ET | 18:00 UTC |

> ⏰ Times may shift by one hour between EST (Nov–Mar) and EDT (Mar–Nov)
> due to Daylight Saving Time. See the [workflow file](.github/workflows/update-data.yml)
> to adjust cron times for your preference.

The workflow:
1. Queries the eBird API for each target species
2. Saves results to [`data/observations.json`](data/observations.json)
3. Commits the updated file back to this repository
4. GitHub Pages serves the new data automatically — no server required

---

## 🗂️ Repository Structure