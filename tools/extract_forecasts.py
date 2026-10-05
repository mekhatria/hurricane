"""Extract NHC official forecasts (OFCL) from the ATCF a-deck archive into data/ofcl.json.

Output per storm: [[synopticTimeUTC, [[tauHours, lat, lon, maxWindKt], ...]], ...]
"""
import gzip
import json

from config import DATA, RAW, STORM_IDS, ADECK_URL, download

TAUS = {0, 12, 24, 36, 48, 60, 72, 96, 120}


def latlon(v):
    n = int(v[:-1]) / 10.0
    return n if v[-1] in "NE" else -n


def main():
    out = {}
    for sid in STORM_IDS:
        path = download(ADECK_URL.format(year=sid[4:], sid=sid.lower()), RAW / "adeck" / f"a{sid.lower()}.dat.gz")
        fc = {}
        for line in gzip.open(path, "rt", errors="ignore"):
            f = [x.strip() for x in line.split(",")]
            if len(f) < 9 or f[4] != "OFCL" or not f[6] or not f[7]:
                continue
            tau = int(f[5])
            if tau not in TAUS:
                continue
            lat, lon = latlon(f[6]), latlon(f[7])
            if lat == 0 and lon == 0:
                continue
            wind = int(f[8]) if f[8].lstrip("-").isdigit() else 0
            # One line per wind-radii threshold; keeping the last per (time, tau) dedupes them.
            fc.setdefault(f[2], {})[tau] = [tau, round(lat, 1), round(lon, 1), wind]
        advisories = []
        for init in sorted(fc):
            pts = [fc[init][k] for k in sorted(fc[init])]
            if len(pts) >= 2 and pts[0][0] == 0:
                advisories.append([f"{init[:4]}-{init[4:6]}-{init[6:8]}T{init[8:10]}:00Z", pts])
        out[sid] = advisories
        print(f"{sid}  {len(advisories)} forecasts")
    (DATA / "ofcl.json").write_text(json.dumps(out, separators=(",", ":")))


if __name__ == "__main__":
    main()
