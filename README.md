# THE WORLD IN ONE DAY — Saturday 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Iyannn11/news-image-20261121-05/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Iyannn11/news-image-20261121-05/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A broadsheet front page for **Saturday 21 November 2026** — 35 stories
across 7 regions, built for the
[make.fun news-image-20261121 bounty](https://make.fun/bounty/news-image-20261121).

## What's on the page

- **3 hero stories:** COP31 stalls into day two of overtime in Antalya,
  five Houthi missiles shot down over Saudi Arabia, and the 6.7 quake
  that shook central Peru.
- **10 illustrated cards:** Zelensky on the Crimean Bridge, Iran's drone
  claim, Iran's uranium red lines, Trump's data-centre tax, China–Japan
  over Taiwan, the Air Niugini diversion to Davao, the Australia–China
  AI dialogue, Bitcoin below $59,000, Russell fastest in Las Vegas FP3,
  and Rahul's century in Wellington.
- **22 more stories** in the "ALSO ON SATURDAY" list, each with its
  source outlet.
- **THE DAY IN UTC** timeline strip with six verified times, a real
  world map with numbered pins 1–13, and a DATE CHECK box naming the
  stories deliberately left out because they happened on other days
  (the Wall Street correction was Friday 20 Nov; the Texas execution
  was Thursday 19 Nov).

## Files

- `entry.png` — the 1024×1024 front page (rendered by `render.py`)
- `render.py` — Python + PIL renderer; all story data is inline
- `main.ts` — copies `entry.png` to `/output/entry.png`

## Build

```sh
python3 render.py   # writes entry.png (deterministic)
```
