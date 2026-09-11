"""The extension → folder mapping. Overridable with a JSON file (--categories)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

OTHERS = "outros"

# key = category id (used with --only), value = (destination folder, extensions)
DEFAULT: dict[str, tuple[str, list[str]]] = {
    "codigo": ("Códigos", [".py", ".cs", ".js", ".ts", ".php", ".html", ".css", ".sql", ".sqlite", ".db"]),
    "texto": ("Texto e XML", [".txt", ".xml", ".log", ".md"]),
    "compactado": ("Compactados", [".zip", ".rar", ".tar", ".gz", ".7z"]),
    "pdf": ("PDF", [".pdf"]),
    "audio": ("Áudio", [".mp3", ".wav", ".aac", ".flac", ".ogg"]),
    "imagem": ("Imagens", [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".webp", ".tiff", ".raw"]),
    "video": ("Vídeos", [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"]),
    "documento": ("Documentos", [".doc", ".docx", ".odt", ".rtf"]),
    "planilha": ("Planilhas", [".xls", ".xlsx", ".ods", ".csv"]),
    "apresentacao": ("Apresentações", [".ppt", ".pptx", ".odp"]),
    "windows": ("Instaladores e binários", [".exe", ".msi", ".dll", ".bat", ".sys", ".ini"]),
}


@dataclass(frozen=True)
class Categories:
    _by_ext: dict[str, str]           # ".pdf" -> "PDF"
    _folders: dict[str, str]          # "pdf"  -> "PDF"
    others_folder: str = OTHERS

    @classmethod
    def build(cls, mapping: dict[str, tuple[str, list[str]]] = DEFAULT, only: set[str] | None = None) -> "Categories":
        by_ext: dict[str, str] = {}
        folders: dict[str, str] = {}
        for key, (folder, exts) in mapping.items():
            if only and key not in only:
                continue
            folders[key] = folder
            for ext in exts:
                by_ext[ext.lower()] = folder
        return cls(by_ext, folders)

    @classmethod
    def from_json(cls, path: str | Path, only: set[str] | None = None) -> "Categories":
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        mapping = {k: (v["folder"], list(v["extensions"])) for k, v in raw.items()}
        return cls.build(mapping, only)

    def folder_for(self, filename: str) -> str:
        ext = Path(filename).suffix.lower()
        return self._by_ext.get(ext, self.others_folder)

    @property
    def known_keys(self) -> list[str]:
        return list(self._folders)

    @property
    def folder_names(self) -> set[str]:
        """Every destination folder this instance can create, including 'outros'."""
        return set(self._folders.values()) | {self.others_folder}
