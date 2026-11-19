#!/usr/bin/env python3
"""Ship the finished front page for Thursday 19 November 2026.

The picture is already painted and lives next to this script as
entry.png: a 1024x1024 newspaper front page for Thursday 19 November
2026, drawn by draw.py (a lead story on the first Trump-Xi-Putin
trilateral in Shenzhen, four second-tier stories with small flat
illustrations, a 30-story "Around the world" list grouped by region,
and a "Day in numbers" strip — 35 stories in all).

This script only moves that file into the folder the grader points
at and checks the copy landed whole. It touches no network, reads
no clock, and uses no randomness, so every run writes the same bytes.
"""

import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
NAME = "entry.png"


def destination() -> Path:
    """Where the image goes: the grader's folder, or /output by default."""
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = Path(folder)
    path.mkdir(parents=True, exist_ok=True)
    return path / NAME


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    target = destination()
    shutil.copyfile(SOURCE, target)
    if sha256_of(SOURCE) != sha256_of(target):
        raise SystemExit(f"copy failed: {target} does not match {SOURCE}")
    print(f"wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
