# Build tools

`hurricane.html` is generated. Make changes in `template.html` (and `data/`), then rebuild:

```bash
cd tools
python3 build.py        # writes ../hurricane.html
```

Only Python 3's standard library is needed.

## Files

| File | Purpose |
|---|---|
| `template.html` | The app's HTML, CSS and JS, with placeholders for the data |
| `build.py` | Inlines `data/*.json` into the template and writes `../hurricane.html` |
| `config.py` | Storm list, source URLs and paths shared by all scripts |
| `extract_storms.py` | NOAA HURDAT2 best track → `data/storms.json` |
| `extract_forecasts.py` | NHC official forecasts (ATCF a-decks) → `data/ofcl.json` |
| `extract_cone_radii.py` | NHC's cone radii per season (via the Internet Archive) → `data/cone_radii.json` |
| `data/world.topo.json` | Highcharts Map Collection world map |

Downloads go to `raw/`, which is git-ignored. Each script downloads what it needs if the file isn't already there.

## Adding a storm

1. Add its ATCF id (for example `AL142016` for Matthew) to `STORM_IDS` in `config.py`. Storms from 2004 onward have wind-radii data, which the app needs.
2. Run the extractors, then rebuild:

   ```bash
   python3 extract_storms.py
   python3 extract_forecasts.py
   python3 extract_cone_radii.py
   python3 build.py
   ```

3. Open `../hurricane.html` to check it, then commit and push. GitHub Pages updates within a minute or two.

## Updating to a newer HURDAT2 release

NOAA publishes a new HURDAT2 file each spring. Set `HURDAT2_FILE` in `config.py` to the new name from https://www.nhc.noaa.gov/data/hurdat/, run `extract_storms.py`, then run `build.py`.
