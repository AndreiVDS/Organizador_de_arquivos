# File Organizer

A desktop utility that **sorts a folder's files into category subfolders** — run it once
over an existing mess, or leave it running to tidy new files as they land.

## What it does

- Pick a folder through a native dialog (Tkinter).
- Files are moved into subfolders by extension:
  `Arquivos de Códigos`, `texto e xml`, `Arquivos Compactados`, `pdf`, `audio`, `imagens`,
  `videos`, `Documentos do word`, `Planilhas`, `Arquivos de apresentação`,
  `Arquivos do Windows`, and `outros` for everything else.
- Unknown extensions are logged to `outros/extensoes.txt`.
- **Watch mode**: uses `watchdog` to keep organising files that appear later, in the background.
- Move is retried on transient `PermissionError` (file still in use).

## Stack

`Python 3` · `watchdog` · `tkinter` · `shutil` / `os` · packaged for Windows with **PyInstaller**

## Running

```bash
pip install watchdog
python main2.py
```

A prebuilt Windows executable is under `dist/Organizador.exe`; rebuild with `pyinstaller main2.spec`.

## Note

`build/` and `dist/` are committed for convenience but are generated artifacts — add them to
`.gitignore` if you fork this.
