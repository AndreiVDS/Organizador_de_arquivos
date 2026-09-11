"""Command-line interface.

    organizar ~/Downloads                 # sort once
    organizar ~/Downloads --dry-run       # show the plan, move nothing
    organizar ~/Downloads --watch         # sort, then keep sorting new files
    organizar . --only imagem,video       # just those categories
    organizar . --categories my.json      # custom mapping
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from .categories import DEFAULT, Categories
from .organizer import apply, plan
from .watcher import watch


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="organizar", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("folder", type=Path, help="folder to organise")
    p.add_argument("--watch", action="store_true", help="keep organising new files after the first pass")
    p.add_argument("--dry-run", action="store_true", help="print what would move, change nothing")
    p.add_argument("--recursive", action="store_true", help="also sort files already in subfolders")
    p.add_argument("--only", help="comma-separated category ids (default: all): " + ",".join(DEFAULT))
    p.add_argument("--categories", type=Path, help="JSON file overriding the extension→folder map")
    p.add_argument("-v", "--verbose", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(levelname)s %(message)s")

    folder: Path = args.folder.expanduser()
    if not folder.is_dir():
        logging.error("not a folder: %s", folder)
        return 2

    only = {c.strip() for c in args.only.split(",")} if args.only else None
    try:
        categories = (
            Categories.from_json(args.categories, only) if args.categories
            else Categories.build(DEFAULT, only)
        )
    except (OSError, ValueError, KeyError) as exc:
        logging.error("bad categories file: %s", exc)
        return 2

    moves = plan(folder, categories, recursive=args.recursive)
    moved = apply(moves, dry_run=args.dry_run)
    logging.info("%s %d file(s)", "would move" if args.dry_run else "moved", moved)

    if args.watch and not args.dry_run:
        watch(folder, categories)
    return 0


if __name__ == "__main__":
    sys.exit(main())
