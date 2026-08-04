# harvestkit

Resumable bulk-dataset harvesting engine — checkpoint, dedup, paginate,
throttle — for [LeMetadatarr](https://github.com/LeMetadatarr) source
clients. Extracted from [metadatarr](https://github.com/TigreGotico/metadatarr)'s
scraper engine into its own standalone package.

Every harvester walks the same skeleton: resume from a saved cursor, fetch a
page, map raw records to flat rows, dedup by an id field, append to JSONL,
checkpoint, throttle, repeat. `harvestkit` captures that skeleton once so a
concrete scraper only has to answer two questions:

- `Source.initial_cursor()` — where a fresh run starts.
- `Source.fetch(cursor)` — given a cursor, return `(rows, next_cursor)`; a
  `next_cursor` of `None` means the harvest is complete.

## Install

```bash
pip install harvestkit
# or, for the HuggingFace publisher:
pip install "harvestkit[hf]"
# or, for Cloudflare-guarded sources:
pip install "harvestkit[stealth]"
```

## Usage

Most JSON REST catalogues need nothing more than `PaginatedJSONSource`: set
`base`/`results_key`/`page_size` and implement `map_row`. HTML catalogues use
`PaginatedHTMLSource`. Anything stranger overrides `Source.fetch` directly and
still gets resume/dedup/checkpoint for free.

```python
from harvestkit import PaginatedJSONSource, register, run_cli

@register
class TVMazeShows(PaginatedJSONSource):
    name = "tvmaze_shows"
    id_field = "id"
    base = "https://api.tvmaze.com/shows"
    results_key = ""  # top-level list
    page_size = 250

    def map_row(self, record):
        return {"id": record["id"], "name": record["name"]}

if __name__ == "__main__":
    run_cli(TVMazeShows)
```

Run it:

```bash
python -m my_client tvmaze_shows --limit 1000
```

Or, once a client module has imported and registered its `Source` subclasses,
dispatch by name through harvestkit's own CLI:

```bash
python -m harvestkit --list
python -m harvestkit tvmaze_shows
```

harvestkit itself registers no sources — it's a library. `--list` prints
nothing until a client has imported its scrapers into the process.

## Publishing to HuggingFace

```python
from harvestkit import publish

publish("tvmaze_shows", collection="media-metadata", org="LeData")
```

`collection` is looked up in `harvestkit.publish.COLLECTIONS` (a plain dict
mapping collection keys to HF repo-id prefixes) to build
`{org}/{prefix}-{name}`. Pass `repo_id=...` to override entirely.

## Checkpoint location

Datasets and checkpoints default to `~/.cache/metadatarr/scrapers` — kept
as-is for back-compat with existing metadatarr-era datasets on disk. Override
with `Source.run(output_dir=...)` or `--output`.

## License

Apache-2.0.
