"""Dispatch a registered scraper by name.

    python -m harvestkit <name> [--output DIR] [--delay S] [--limit N]
    python -m harvestkit --list

harvestkit itself registers no :class:`~harvestkit.engine.Source` subclasses —
client code imports its own scraper modules (which call
:func:`~harvestkit.engine.register` on import) before invoking this CLI, so
whatever is registered in-process at call time is what ``--list``/dispatch see.
"""
from __future__ import annotations

import sys

from harvestkit.engine import all_sources, get_source, run_cli


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    if not argv or argv[0] in ("--list", "-l", "list"):
        for name in sorted(all_sources()):
            print(name)
        return 0

    name, rest = argv[0], argv[1:]
    try:
        source_cls = get_source(name)
    except KeyError:
        print(f"unknown scraper: {name!r}. Use --list to see available ones.",
              file=sys.stderr)
        return 2
    return run_cli(source_cls, rest)


if __name__ == "__main__":
    raise SystemExit(main())
