# Dream House

House plans and South Indian modern exterior/interior studies.

## Run locally

Requires Python 3; no packages or build step are needed.

```sh
python3 -m http.server 8000 --directory public
```

Open http://localhost:8000/floor-plan/.

The site includes ground-floor, first-floor and roof plans, five exterior views,
and sixteen interior views. Each page has one Download button that downloads
`dream-house.zip`. Extract it to get a `dream-house` folder containing five SVG
plans and all twenty-one current gallery images.

## Update drawings and download bundle

```sh
python3 scripts/floor-plan/upper_options.py
python3 scripts/floor-plan/build_download.py
```

`upper_options.py` also regenerates ground-floor and plot drawings. Rebuild the
ZIP after updating drawings or gallery assets. HTML pages are edited directly.

## Files

- `public/floor-plan/`: standalone website, current images, SVG plans and ZIP.
- `scripts/floor-plan/`: Python drawing generators and download bundler.
- `design/`: image-generation prompts for the current design studies.

The drawings are concept plans, not construction documents. AI-rendered details
can vary from the plans; structural design and measured elevations remain to be
developed. The roof drawing and first-floor rear-center coverage currently have
a discrepancy; the latest rendered rear terrace is open to sky.
