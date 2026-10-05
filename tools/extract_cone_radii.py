"""Read NHC's published Atlantic cone radii for each season into data/cone_radii.json.

The table on https://www.nhc.noaa.gov/aboutcone.shtml changes every year, so each season's
values are read from the Internet Archive copy live in mid-August of that year. The oldest
archived copy is from 2007, so 2005 storms end up using the 2007 table.
"""
import html
import json
import re

from config import DATA, RAW, STORM_IDS, WAYBACK, download

LEADS = (12, 24, 36, 48, 60, 72, 96, 120)


def atlantic_radii(page):
    text = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", page)))
    seg = text[text.find("Forecast Period"):][:700]
    cols = 3 if "Central North Pacific Basin (nautical miles)" in seg[:400] else 2
    body = seg[seg.rfind("(nautical miles)", 0, 400) + len("(nautical miles)"):]
    nums = [int(x) for x in re.findall(r"\b\d+\b", body)]
    radii, k = {}, 0
    while k + cols < len(nums) + 1 and nums[k] in LEADS:
        radii[nums[k]] = nums[k + 1]          # first value after the lead time is the Atlantic basin
        k += cols + 1
    return radii


def main():
    years = sorted({int(s[4:]) for s in STORM_IDS})
    out = {}
    for y in years:
        page = download(WAYBACK.format(year=y), RAW / "cone" / f"{y}.html").read_text(errors="ignore")
        out[str(y)] = atlantic_radii(page)
        print(y, out[str(y)])
    (DATA / "cone_radii.json").write_text(json.dumps(out))


if __name__ == "__main__":
    main()
