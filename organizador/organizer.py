"""Planning and moving. `plan()` has no side effects; `apply()` does the moves."""

from __future__ import annotations

import logging
import shutil
import time
from dataclasses import dataclass
from pathlib import Path

from .categories import Categories

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class Move:
    src: Path
    dest_dir: Path

    @property
    def dest(self) -> Path:
        return self.dest_dir / self.src.name


def plan(folder: Path, categories: Categories, *, recursive: bool = False) -> list[Move]:
    """What would move, without touching anything."""
    folder = Path(folder)
    managed = {folder / name for name in categories.folder_names}
    files = folder.rglob("*") if recursive else folder.iterdir()

    moves: list[Move] = []
    for entry in sorted(files):
        if not entry.is_file():
            continue
        if any(parent in managed for parent in entry.parents):
            dest_dir = folder / categories.folder_for(entry.name)
            if entry.parent == dest_dir:
                continue  # already in the right place
        moves.append(Move(entry, folder / categories.folder_for(entry.name)))
    return moves


def apply(moves: list[Move], *, dry_run: bool = False, retries: int = 5) -> int:
    done = 0
    for mv in moves:
        if dry_run:
            log.info("[dry-run] %s -> %s/", mv.src.name, mv.dest_dir.name)
            done += 1
        elif _move_one(mv, retries):
            done += 1
    return done


def _move_one(mv: Move, retries: int) -> bool:
    if mv.src.parent == mv.dest_dir:
        return False
    mv.dest_dir.mkdir(parents=True, exist_ok=True)
    target = _unique(mv.dest)
    for attempt in range(1, retries + 1):
        try:
            shutil.move(str(mv.src), str(target))
            log.info("%s -> %s/", mv.src.name, mv.dest_dir.name)
            return True
        except PermissionError:
            log.warning("%s in use, retry %d/%d", mv.src.name, attempt, retries)
            time.sleep(1)
        except FileNotFoundError:
            log.warning("%s vanished before it could be moved", mv.src.name)
            return False
        except OSError as exc:
            log.error("could not move %s: %s", mv.src.name, exc)
            return False
    log.error("gave up on %s after %d tries", mv.src.name, retries)
    return False


def _unique(path: Path) -> Path:
    """file.pdf -> 'file (1).pdf' if the destination is taken."""
    if not path.exists():
        return path
    stem, suffix, i = path.stem, path.suffix, 1
    while path.with_name(f"{stem} ({i}){suffix}").exists():
        i += 1
    return path.with_name(f"{stem} ({i}){suffix}")
