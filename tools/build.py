"""Build ../hurricane.html from template.html and the JSON files in data/.

The template has four placeholders that get the data inlined, so the published page
is a single self-contained file (apart from the Highcharts CDN scripts).
"""
from config import DATA, TOOLS, WORLD_MAP_URL, download

PLACEHOLDERS = {
    "__MAPDATA__": "world.topo.json",
    "__STORMS__": "storms.json",
    "__OFCL__": "ofcl.json",
    "__CONE__": "cone_radii.json",
}


def main():
    download(WORLD_MAP_URL, DATA / "world.topo.json")
    page = (TOOLS / "template.html").read_text()
    for key, name in PLACEHOLDERS.items():
        if key not in page:
            raise SystemExit(f"placeholder {key} missing from template.html")
        page = page.replace(key, (DATA / name).read_text().strip())
    out = TOOLS.parent / "hurricane.html"
    out.write_text(page)
    print(f"wrote {out} ({len(page.encode()) // 1024} KB)")


if __name__ == "__main__":
    main()
