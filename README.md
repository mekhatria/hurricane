# Hurricane Track Playback

**Live demo: https://mekhatria.github.io/hurricane/**

Replay 20 real Atlantic hurricanes (Katrina 2005 through Melissa 2025) on an interactive map, and compare what actually happened with what the National Hurricane Center forecast at the time.

## Features

- **Real storm data**: position, maximum wind, pressure, landfalls and wind-field size every 6 hours, from NOAA's best-track record. Positions in between follow a smooth spline through the official fixes.
- **Satellite-style storm**: an enhanced-infrared look (the default) or a visible-light look. Each category has its own structure, with 3 variations, and the storm turns counterclockwise. It is drawn at true geographic scale from the measured 34-kt wind radius, so it resizes correctly as you zoom.
- **NHC forecasts as issued**: every official advisory forecast, shown from the time it was published, with the cone rebuilt from that season's published cone radii. Dotted lines show how far each forecast point was from where the storm actually went, and the table lists each storm's average day-3 miss.
- **Controls**: play, pause and scrub through time, change speed, and switch the wind field, cone and forecast details on or off. Light, dark and auto themes are available.
- **Compare storms**: a sortable table (Highcharts Grid Lite). Click a row to load that storm.
- **Deep links**: for example `#AL122005@120` opens Katrina at hour 120.

## Data sources

- **Best track**: [NOAA NHC HURDAT2](https://www.nhc.noaa.gov/data/#hurdat), Atlantic, 1851–2025 release.
- **Official forecasts (OFCL)**: [NHC ATCF a-deck archive](https://ftp.nhc.noaa.gov/atcf/archive/).
- **Cone radii**: NHC's [cone definition page](https://www.nhc.noaa.gov/aboutcone.shtml) for each season, via the Internet Archive. The 2005 storms use the earliest archived table, from 2007.

The cloud imagery is a procedural rendering, not real satellite imagery. The cone is rebuilt from NHC's inputs using NHC's method, so it may differ slightly in shape from NHC's own graphics.

## Built with

- [Highcharts Maps](https://www.highcharts.com/products/maps/)
- [Highcharts Grid Lite](https://www.highcharts.com/products/grid/)

Both libraries load from the jsDelivr CDN. Everything else, including the map and all storm data, is inside `hurricane.html`.

Highcharts is free for personal, school and non-profit use. Commercial use requires a [license](https://shop.highcharts.com/).
