# The World — 27 November 2026

[![make.fun](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/yudhisutawan77/news-image-27nov/rank.svg)](https://make.fun/bounty/news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/yudhisutawan77/news-image-27nov/reward.svg)](https://make.fun/bounty/news-image-20261127)

A one-page newspaper front page summing up the world's news of
**Friday 27 November 2026**, drawn with PIL at build time and shipped as
`entry.png` (1024×1024, ~110 KB).

## The day's stories

- **Iranian drones kill two Italians in Kuwait** — Italy and Kuwait blame
  Iran for the strike on an air-defence station, where two Rheinmetall
  technicians died and two more people were hurt; Tehran denies any role.
  (BBC, Reuters, NYT, 27 Nov)
- **Israel kills 10 in Gaza as Hamas weighs reply** — ten people killed in
  Israeli strikes; Hamas weighs its response to the latest escalation.
  (Reuters, 27 Nov)
- **Tanker capsizes off Ibiza; one dead, oil spill feared** — a diesel
  tanker carrying up to 7,000 tonnes capsizes; Spain races to stop the
  spill. (BBC, 27 Nov)
- **UK net migration falls to lowest since 1997** — lowest in nearly three
  decades outside the pandemic years. (NYT, 27 Nov)
- **Gukesh, Sindarov draw marathon Game 3** — nothing separates the two
  after three games of the World Chess Championship match.
  (India Today / The Hindu, 27 Nov)
- **Depardieu to stand trial for alleged rape** — a French court rules the
  actor must face trial over an alleged rape in 2018. (BBC, 27 Nov)
- Also today: Ebola in Congo passes 12,000 cases; Nepal declares 4,000
  landslide missing dead; Trump seeks a probe into GDP figures.

## How it runs

`main.py` (Python 3.13, standard library only) copies the bundled
`entry.png` to the output path: `ENTRY_OUT` (file or directory) →
`MAKEFUN_OUTPUT_DIR` → `/output/entry.png` → `./entry.png` (last resort
only). No network, deterministic — two runs write byte-identical files.

`draw.py` is the build-time renderer (PIL) that drew `entry.png`; it is
not needed at grade time.

## Entry

- Competition: [Sum up 27 November's world news in one image](https://make.fun/bounty/news-image-20261127)
- License: MIT (see `LICENSE`)
