#!/usr/bin/env python3
"""Reproducible tokenizer audit with both legacy and corrected metrics."""
from __future__ import annotations

import argparse
import csv
import json
import unicodedata
from pathlib import Path

import regex


def load_tokenizer(spec: str):
    if spec == "gpt2":
        import tiktoken
        return tiktoken.get_encoding("gpt2").encode
    if spec.startswith("hf:"):
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(spec[3:])
        return lambda text: tokenizer.encode(text, add_special_tokens=False)
    raise ValueError(f"Unsupported tokenizer {spec!r}; use gpt2 or hf:<repository>")


def lines(path: Path) -> list[str]:
    return [unicodedata.normalize("NFC", line.strip()) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def units(text: str) -> dict[str, int]:
    return {
        "whitespace_word": len(text.split()),
        "grapheme": len(regex.findall(r"\X", text)),
        "utf8_byte": len(text.encode("utf-8")),
        "sentence": 1,
    }


def corrected(corpus: list[str], encode) -> dict[str, float]:
    totals = {key: 0 for key in ("token", "whitespace_word", "grapheme", "utf8_byte", "sentence")}
    for text in corpus:
        totals["token"] += len(encode(text))
        for key, value in units(text).items():
            totals[key] += value
    return {key: totals["token"] / value for key, value in totals.items() if key != "token"}


def legacy(corpus: list[str], encode) -> dict[str, float]:
    # Exact logic of starter_kit/fertility.py after its reader has stripped lines.
    fert, tok_char = [], []
    for text in corpus:
        text = text.lower()
        tokens = len(encode(text))
        fert.append(tokens / len(text.split(" ")))
        tok_char.append(tokens / len(text))
    return {"legacy_tok_per_space_split_word": sum(fert) / len(fert), "legacy_tok_per_codepoint": sum(tok_char) / len(tok_char)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--languages", nargs="+", default=["eng", "hin", "kan", "tam", "tel"])
    parser.add_argument("--tokenizer", action="append", required=True, help="repeatable: gpt2 or hf:repo")
    parser.add_argument("--out", type=Path, default=Path("results.csv"))
    args = parser.parse_args()
    corpora = {lang: lines(args.data / f"{lang}.txt") for lang in args.languages}
    counts = {lang: len(corpus) for lang, corpus in corpora.items()}
    if len(set(counts.values())) != 1:
        raise SystemExit(f"Expected parallel files with equal line counts, got {counts}")
    rows = []
    for spec in args.tokenizer:
        encode = load_tokenizer(spec)
        for lang, corpus in corpora.items():
            metric = corrected(corpus, encode)
            for name, value in legacy(corpus, encode).items():
                rows.append({"tokenizer": spec, "language": lang, "metric": name, "tokens_per_unit": value})
            for name, value in metric.items():
                rows.append({"tokenizer": spec, "language": lang, "metric": f"tok_per_{name}", "tokens_per_unit": value})
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["tokenizer", "language", "metric", "tokens_per_unit"])
        writer.writeheader(); writer.writerows(rows)
    print(json.dumps({"sentences_per_language": next(iter(counts.values())), "rows": len(rows), "out": str(args.out)}, indent=2))


if __name__ == "__main__":
    main()
