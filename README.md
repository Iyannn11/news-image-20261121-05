[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Iyannn11/news-image-20261121-05/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Iyannn11/news-image-20261121-05/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# Saturday 21 November 2026 — The World in One Day

One image that sums up the world's news of Saturday 21 November 2026:
**35 dated stories across 7 regions**, every one numbered, dated and sourced.

A broadsheet front page in the style of the Top 1 entry for this bounty,
redrawn cleaner: a stronger masthead and deck, a facts strip with bigger
numerals, uniform card geometry, a more accurate world map with numbered
dots, crisper original illustrations, and a DATE CHECK box that names what
was deliberately left out — including the Wall Street correction, which was
Friday 20 November's trading session, not Saturday's news.

## Layout

- Masthead + deck naming the three biggest stories
- Facts strip: Day 13 of COP31 · 5 missiles · 6.7 quake · 146 safe ·
  $58,174 bitcoin · 124\* Rahul
- Region bars: Europe 5 · Asia 10 · Middle East 6 · Africa 1 ·
  Americas 8 · Oceania 3 · Global 2
- 3 big story cards (COP31, Saudi missiles, Peru quake) + 10 smaller cards
- "Where it happened" world map with numbered dots for stories 1–13
- "Also on Saturday 21 November 2026": 22 more stories, one line each
- DATE CHECK: what was left out on purpose, and why

## Files

- `entry.png` — the front page, 1024×1024, rendered by `render.py`
- `render.py` — draws the page with Pillow (stdlib + PIL at build time only)
- `main.ts` — copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (or `/output`),
  with a 1 MiB size guard
- `SOURCES.md` — every story with its source

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Entry for the [news-image-20261121 bounty on make.fun](https://make.fun/bounty/news-image-20261121).
