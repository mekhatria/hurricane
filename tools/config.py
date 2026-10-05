"""Shared settings for the data scripts."""
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
DATA = TOOLS / "data"          # committed: the extracted JSON that build.py embeds
RAW = TOOLS / "raw"            # not committed: downloaded source files (re-fetched on demand)

# Storms shown in the app (ATCF ids). Order here is the order in the embedded data.
STORM_IDS = [
    "AL122005", "AL182005", "AL252005", "AL092008", "AL182012", "AL092017", "AL112017", "AL152017",
    "AL062018", "AL142018", "AL052019", "AL132020", "AL092021", "AL092022", "AL102023", "AL022024",
    "AL092024", "AL142024", "AL052025", "AL132025",
]

# NOAA HURDAT2 Atlantic best-track release (see https://www.nhc.noaa.gov/data/hurdat/).
HURDAT2_FILE = "hurdat2-1851-2025-092326.txt"
HURDAT2_URL = "https://www.nhc.noaa.gov/data/hurdat/" + HURDAT2_FILE

# NHC ATCF a-deck archive (official forecasts are the OFCL lines).
ADECK_URL = "https://ftp.nhc.noaa.gov/atcf/archive/{year}/a{sid}.dat.gz"

# NHC cone definition page, read through the Internet Archive for each season.
CONE_PAGE = "https://www.nhc.noaa.gov/aboutcone.shtml"
WAYBACK = "https://web.archive.org/web/{year}0815000000/" + CONE_PAGE

# Highcharts Map Collection world map (TopoJSON).
WORLD_MAP_URL = "https://code.highcharts.com/mapdata/custom/world.topo.json"


def download(url, dest):
    """Fetch url to dest unless it already exists."""
    import urllib.request
    dest = Path(dest)
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    print("downloading", url)
    req = urllib.request.Request(url, headers={"User-Agent": "hurricane-demo-tools"})
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        f.write(r.read())
    return dest
