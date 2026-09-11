"""Keep organising files that show up after the first pass."""

from __future__ import annotations

import logging
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .categories import Categories
from .organizer import Move, apply

log = logging.getLogger(__name__)


class _Handler(FileSystemEventHandler):
    def __init__(self, folder: Path, categories: Categories, dry_run: bool):
        self.folder = folder
        self.categories = categories
        self.dry_run = dry_run

    def _sort(self, path_str: str) -> None:
        src = Path(path_str)
        if not src.is_file():
            return
        if any(parent.name in self.categories.folder_names for parent in src.parents):
            return  # already inside a managed folder
        dest = self.folder / self.categories.folder_for(src.name)
        apply([Move(src, dest)], dry_run=self.dry_run)

    def on_created(self, event):
        if not event.is_directory:
            self._sort(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self._sort(event.dest_path)


def watch(folder: Path, categories: Categories, *, dry_run: bool = False) -> None:
    handler = _Handler(folder, categories, dry_run)
    observer = Observer()
    observer.schedule(handler, str(folder), recursive=False)
    observer.start()
    log.info("watching %s — Ctrl+C to stop", folder)
    try:
        while observer.is_alive():
            observer.join(1)
    except KeyboardInterrupt:
        log.info("stopping")
    finally:
        observer.stop()
        observer.join()
