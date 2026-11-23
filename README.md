[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/akbare12/news-22-b14-utc-timeline/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/akbare12/news-22-b14-utc-timeline/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# THE WORLD TODAY — Sunday 22 November 2026 (UTC Timeline)

One image summing up Sunday 22 November 2026, built as a 24-hour UTC
timeline: the day's milestones down a spine — 01:00 Hong Kong polls open,
03:00 COP31 objections close, 06:00 COP31 session, ~16:00 COP31 collapses,
17:00 Alcaraz wins, 18:13 Democrats reach 258, 23:00 wires read — with the
three hero scenes embedded at their hours and the small cards slotted by
time. 36 stories, 7 regions, canonical numbers, a numbered world map, and a
red DATE CHECK box (wires read to 23:00 UTC, LEFT OUT with dates, NOT YET).

## The day's three heroes

1. **COP31 collapses: NO DEAL** (Antalya) — talks end with no agreement
   after 44 hours overtime, the first climate-summit failure since 2009.
2. **186 drones rain on Ukraine overnight** — 161 shot down or jammed; a
   five-storey block in Dymer collapses, 1 dead, 14 unaccounted for.
3. **Iran claims 2 US Patriot radars hit in Bahrain** (CLAIM) — Tehran says
   its missiles struck al-Riffa and Awali; Bahrain denies a military attack.

## How it is built

`draw.py` (Pillow) draws `entry.png` (1024×1024). `main.py` is a
stdlib-only copy program: it copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` and verifies the PNG header (1024×1024)
and sha256. It never writes next to `main.py`.

Scenes are drawn illustrations, not photographs.
