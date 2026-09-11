# File Organizer

[![CI](https://github.com/AndreiVDS/Organizador_de_arquivos/actions/workflows/ci.yml/badge.svg)](https://github.com/AndreiVDS/Organizador_de_arquivos/actions/workflows/ci.yml)
![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![tests](https://img.shields.io/badge/tests-11_passing-6e9f18)
![license](https://img.shields.io/badge/license-MIT-blue)

A command-line tool that **sorts a folder's files into category subfolders** — run it once
over a mess, or leave it running to tidy new files as they land.

## Use

```bash
organizar ~/Downloads                  # sort once
organizar ~/Downloads --dry-run        # print the plan, move nothing
organizar ~/Downloads --watch          # sort, then keep sorting new files (Ctrl+C to stop)
organizar . --only imagem,video        # restrict to some categories
organizar . --recursive                # also sweep files already in subfolders
organizar . --categories my.json       # custom extension → folder map
```

Files go into `Imagens/`, `Vídeos/`, `PDF/`, `Códigos/`, `Planilhas/`, … and anything
unrecognised into `outros/`. Name clashes are never overwritten (`report.pdf` →
`report (1).pdf`). A file being written by another process is retried a few times.

### Custom categories

```json
{
  "livros":  { "folder": "Livros",  "extensions": [".epub", ".mobi", ".pdf"] },
  "imagens": { "folder": "Fotos",   "extensions": [".jpg", ".png", ".heic"] }
}
```

## Design

```
organizador/
  categories.py   the extension → folder map (built-in or from JSON), with --only filtering
  organizer.py    plan(folder) -> [Move]  (no side effects)  ·  apply(moves, dry_run=…)
  watcher.py      watchdog handler that runs the same logic on new files
  cli.py          argparse front-end
organizar.py      entry point (also the PyInstaller target)
```

`plan()` and `apply()` are separate on purpose: `--dry-run` is just `apply(..., dry_run=True)`,
and the tests drive `plan`/`apply` against a temp directory with no mocking.

## Install / develop

```bash
pip install -e .            # gives you the `organizar` command
python organizar.py --help  # or run it directly

pip install -e ".[dev]" && pytest   # 11 tests
```

Build a standalone executable with `pyinstaller organizar.spec` (output in `dist/`).
