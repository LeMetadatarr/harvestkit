# Dataset products

`harvestkit` is a resumable bulk-dataset harvesting engine. The repository does
not ship upstream scrapers; it provides the skeleton that source-specific
scraper clients use to produce JSONL datasets. The engine handles pagination,
checkpointing, deduplication, throttling and resumption, so each concrete
scraper only has to fetch a page and map raw records to flat rows.

## What this repo produces

A `harvestkit` run appends one JSON object per line to a `{name}.jsonl` file.
Each row is the output of the scraper's `map_row()` method, typically a flat
dictionary of primitive fields. A companion `{name}_checkpoint.json` stores the
cursor and total row count so the run can resume after interruption. The repo
also includes `harvestkit.publish`, which pushes the JSONL file to Hugging Face
Datasets.

## Dataset format

Files are line-delimited JSON (JSONL). UTF-8 encoding. One row per upstream
record.

Core files written to the output directory:

| File | Purpose |
| ---- | ------- |
| `{name}.jsonl` | Dataset rows, one JSON object per line. |
| `{name}_checkpoint.json` | Resume cursor and row total. |

The row schema is defined by each `Source` subclass. A minimal row might look
like this:

```json
{"id": "12345", "title": "Example Show", "year": 2020}
```

When `harvestkit.publish` reads a JSONL file, it coerces types for consistency:

- Fields ending in `_year` are cast to integer when possible.
- Fields ending in `_id` (plus a fixed set such as `soundcloud_id`,
  `bandcamp_id`, `mb_id`, `wikidata_id`) are cast to string.
- Mixed string/integer columns become strings.
- Columns that are lists in some rows and scalars in others become lists of
  strings.

## How to generate it

Subclass `PaginatedJSONSource` (or `Source` for non-standard pagination),
implement `map_row()`, register the class, and run it.

```python
from pathlib import Path
from harvestkit import PaginatedJSONSource, register, run_cli

@register
class TVMazeShows(PaginatedJSONSource):
    name = "tvmaze_shows"
    id_field = "id"
    base = "https://api.tvmaze.com/shows"
    results_key = ""
    page_size = 250

    def map_row(self, record):
        return {
            "id": record["id"],
            "name": record["name"],
            "language": record.get("language"),
            "premiered": record.get("premiered"),
        }

if __name__ == "__main__":
    run_cli(TVMazeShows)
```

Run from the command line:

```bash
python -m my_client tvmaze_shows --limit 1000 --output ./datasets
```

Or dispatch through `harvestkit` after importing the scraper module:

```bash
python -m harvestkit tvmaze_shows --output ./datasets
```

Publish the resulting JSONL to Hugging Face:

```python
from harvestkit import publish

publish("tvmaze_shows", collection="media-metadata", org="LeData")
```

## Worth publishing on Hugging Face?

Yes. `harvestkit` is the pipeline layer for the LeMetadatarr project, and its
JSONL output is designed to be pushed to Hugging Face Datasets. The publisher
creates a dataset card, resolves repo IDs from named collections, and casts
rows to a consistent Arrow schema. Datasets produced by downstream harvestkit
scrapers are published under the `LeData` namespace as part of themed
collections such as `media-metadata`.

## ML tasks served

- Entity linking and catalog reconciliation across media databases.
- Metadata enrichment for recommendation systems.
- Retrieval and RAG corpora for media questions.
- Dataset construction for training domain-specific scrapers and parsers.
