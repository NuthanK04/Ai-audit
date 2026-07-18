#!/usr/bin/env python3
"""Download a small, parallel FLORES-200 dev evaluation slice.

The script intentionally downloads data rather than committing a copy: the
source archive is large and its checksum/version should be recorded by a
submission run.  The selected languages are parallel by sentence index.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import tarfile
import urllib.request
from pathlib import Path

FLORES_URL = "https://dl.fbaipublicfiles.com/nllb/flores200_dataset.tar.gz"
LANGS = {"eng": "eng_Latn", "hin": "hin_Deva", "kan": "kan_Knda", "tam": "tam_Taml", "tel": "tel_Telu"}


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "fertility-audit/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("data/flores_dev"))
    parser.add_argument("--limit", type=int, default=997, help="first N dev sentences; 997 is the complete dev split")
    parser.add_argument("--url", default=FLORES_URL)
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be positive")

    args.out.mkdir(parents=True, exist_ok=True)
    blob = download(args.url)
    corpora = {}
    with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as archive:
        for short, code in LANGS.items():
            suffix = f"/dev/{code}.dev"
            matches = [member for member in archive.getmembers() if member.name.endswith(suffix)]
            if len(matches) != 1:
                raise RuntimeError(f"Archive does not contain exactly one {suffix!r}; found {[x.name for x in matches]}")
            member = matches[0]
            handle = archive.extractfile(member)
            assert handle is not None
            lines = handle.read().decode("utf-8").splitlines()[: args.limit]
            if len(lines) != args.limit:
                raise RuntimeError(f"{code}: expected {args.limit} lines, got {len(lines)}")
            corpora[short] = lines
    if len({len(lines) for lines in corpora.values()}) != 1:
        raise RuntimeError("parallelism check failed: language files have different line counts")
    for short, lines in corpora.items():
        (args.out / f"{short}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (args.out / "SOURCE.txt").write_text(f"FLORES-200 dev\nurl: {args.url}\nsha256: {hashlib.sha256(blob).hexdigest()}\n", encoding="utf-8")
    print(f"wrote {len(next(iter(corpora.values())))} parallel sentences for {', '.join(corpora)} to {args.out}")


if __name__ == "__main__":
    main()
