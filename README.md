# news-image-20261119

![news-image-20261119](https://img.shields.io/badge/news--image-20261119-blue)
![repo](https://img.shields.io/badge/repo-agungvg%2Fnews--image--20261119-green)

One image that sums up the world's news of **Thursday 19 November 2026** — a
newspaper front page, "THE WORLD", drawn entirely in code with Pillow.

## What's on the page — 35 stories, 7 regions

- **Lead:** the first-ever Trump–Xi–Putin trilateral summit opens in Shenzhen
  at APEC — Xi hugs Trump on the tarmac. Hero illustration: the Shenzhen
  skyline at dusk with the three flags.
- **Second tier (4, each with its own small illustration):** Anthropic's
  $81.3bn IPO, the biggest ever; Israeli tanks cross the ceasefire line in
  central Gaza; the Crimean Bridge is hit again; Hakeem Jeffries is nominated
  as the next Speaker — the first Black Speaker.
- **Around the world (30 more, grouped by region):** Asia, Europe, the
  Middle East, the Americas, Tech & Science, Culture & Sport — from Cyclone
  Akvan and Indonesia's rate rise to Voyager 1 reaching one light-day from
  Earth, a record $190.4m Van Gogh, and GTA VI's global rollout.
- **Day in numbers:** 35 stories · 7 regions · $81.3bn biggest IPO ever ·
  1 light-day (Voyager 1) · 3 leaders, one table.

Every story is an event of 19 November 2026, sourced from Reuters, AP, AFP,
BBC, Al Jazeera and others. Nothing is invented; no hype or speculation is
presented as fact.

## Files

- `draw.py` — paints `entry.png` (1024×1024, Pillow, no network, fixed
  seed, deterministic)
- `main.py` — the competition entrypoint: copies `entry.png` to
  `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`) and verifies the copy
- `entry.png` — the finished front page

## Run

```sh
python3 draw.py      # repaint entry.png
python3 main.py      # write /output/entry.png
```

Re-running either script produces byte-identical output.

## License

MIT — see `LICENSE`.
