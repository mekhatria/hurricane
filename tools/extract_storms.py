"""Extract the selected storms from NOAA HURDAT2 into data/storms.json.

Each fix: [timeUTC, lat, lon, status, windKt, pressureMb, recordId,
           r34[NE,SE,SW,NW], r50[...], r64[...], rmwNm]   (radii in n mi, -999 = missing)
"""
import json

from config import DATA, RAW, STORM_IDS, HURDAT2_FILE, HURDAT2_URL, download


def main():
    path = download(HURDAT2_URL, RAW / HURDAT2_FILE)
    lines = path.read_text().splitlines()
    storms, i = {}, 0
    while i < len(lines):
        head = [x.strip() for x in lines[i].split(",")]
        sid, n = head[0], int(head[2])
        if sid in STORM_IDS:
            pts = []
            for ln in lines[i + 1:i + 1 + n]:
                f = [x.strip() for x in ln.split(",")]
                lat = float(f[4][:-1]) * (1 if f[4][-1] == "N" else -1)
                lon = float(f[5][:-1]) * (1 if f[5][-1] == "E" else -1)
                ints = [int(x) for x in f[6:21]]
                rad = ints[2:14]
                iso = f"{f[0][:4]}-{f[0][4:6]}-{f[0][6:]}T{f[1][:2]}:{f[1][2:]}Z"
                pts.append([iso, lat, lon, f[3], ints[0], ints[1], f[2], rad[0:4], rad[4:8], rad[8:12], ints[14]])
            storms[sid] = {"id": sid, "name": head[1].title(), "year": int(sid[4:]), "pts": pts}
        i += n + 1

    missing = [s for s in STORM_IDS if s not in storms]
    if missing:
        raise SystemExit(f"not found in {HURDAT2_FILE}: {missing}")
    out = [storms[s] for s in STORM_IDS]
    for s in out:
        print(f"{s['name']:>10} {s['year']}  {len(s['pts'])} fixes  peak {max(p[4] for p in s['pts'])} kt")
    (DATA / "storms.json").write_text(json.dumps(out, separators=(",", ":")))


if __name__ == "__main__":
    main()
