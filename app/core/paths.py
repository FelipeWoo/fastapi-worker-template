from __future__ import annotations

from pathlib import Path


def find_project_root(marker: str = "Makefile") -> Path:
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / marker).is_file():
            return parent.resolve()
    raise FileNotFoundError(f"{marker} not found in any parent directory.")


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path
