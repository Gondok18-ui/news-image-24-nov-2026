[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Gondok18-ui/news-image-24-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard)
[![reward](https://make.fun/badge/news-image-20261124/Gondok18-ui/news-image-24-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261124)

# The Daily Meridian — the world of Tuesday, 24 November 2026, on one page

An original broadsheet newspaper front page, drawn entirely in code, that
sums up the world news of Tuesday 24 November 2026 in a single 1024×1024
image.

## Repository layout

- **`entry.png`** — the judged image itself: the finished front page,
  1024×1024, held in the repository.
- **`generate.py`** — the generator that drew `entry.png` (Python 3,
  Pillow only). It was run during development to produce the image and
  is kept here for provenance and reproduction; running it again
  regenerates the same PNG byte for byte.
- **`main.ts`** — the program the make.fun harness runs. It uses only
  the Node 22 standard library: it resolves the output directory
  (`$MAKEFUN_OUTPUT_DIR`, defaulting to `/output`), creates it if
  needed, and copies `entry.png` into it.

## What the page shows

- **Masthead** — *The Daily Meridian*, with the date line
  "Tuesday, 24 November 2026" on a navy date bar marked LATE FINAL
  EDITION and a black "Also Today" ticker carrying the day's one-line
  stories: Germany receiving Ukraine's Delta battlefield system, the
  Solomon Islands ending its China security pact, Spain's amnesty for
  Puigdemont, Sanofi buying Insmed for $41B, and the United States
  losing its measles elimination status.
- **Lead story** — "Huang Returns to Nvidia as Shares Soar 31%":
  Nvidia's board reinstates its founder Jensen Huang as chief executive
  and chair less than two weeks after his resignation, reportedly after
  pressure from President Trump — and Wall Street answers with the
  biggest one-day rally of the AI era, the S&P 500 up 4.73% and the
  Nasdaq up 6.51%. The story carries a drawn illustration of the day's
  rising NVDA chart.
- **Three panels** — Russia's warning of a "preventive nuclear attack"
  as Medvedev says Ukraine and NATO crossed a line and NATO vows to
  defend space; a factory fire in Banten province, Indonesia, killing
  at least 26 people with dozens more missing; and US states suing Elon
  Musk's firms over alleged Grok-generated child sexual-abuse images.
- **Four briefs** — Zelensky confirming seven drones sank the Russian
  corvette Merkury at Benghazi; Qatar seeking to revive US–Iran talks
  while Netanyahu urges strikes; seven nations backing limits on
  Russian tourist and sports visas; and the US losing its measles
  elimination status after 25 years.

## How the program works

`generate.py` (Python 3, Pillow only) composes the page from flat
vector shapes and typeset text: a double-ruled page frame, a serif
masthead, a navy date bar, a black ticker strip, the lead story with
its drawn market-chart illustration, three ruled story columns and a
row of briefs. All headlines and body copy are written for this entry,
and the drawing is fully deterministic — no randomness, no clock, no
network — so two runs write byte-identical files.

Run it:

```sh
python3 generate.py            # writes entry.png beside the program
```

Under the make.fun harness, `main.ts` (Node 22, standard library
only) copies the held `entry.png` to `/output/entry.png`. The image
is a whole PNG, exactly 1024×1024 pixels and well under the 1 MiB
limit.
