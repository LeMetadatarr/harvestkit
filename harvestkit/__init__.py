"""harvestkit — resumable bulk-dataset harvesting engine.

Checkpoint/dedup/paginate/throttle skeleton for source-specific scraper
clients, plus a HuggingFace dataset publisher. See :mod:`harvestkit.engine`
for the full API description.
"""

from harvestkit.engine import (
    PaginatedHTMLSource,
    PaginatedJSONSource,
    PartitionedJSONSource,
    Source,
    Throttle,
    all_sources,
    deep_get,
    get_source,
    register,
    run_cli,
)
from harvestkit.publish import publish

__all__ = [
    "Source",
    "PaginatedJSONSource",
    "PartitionedJSONSource",
    "PaginatedHTMLSource",
    "register",
    "get_source",
    "all_sources",
    "run_cli",
    "deep_get",
    "Throttle",
    "publish",
]

__version__ = "0.1.0a1"
