"""
fertility.py - Reference tokenizer fertility measurement

This is the original measurement script used as the baseline for the audit.
It demonstrates the standard methodology for computing tokenization metrics.

Usage:
    python fertility.py --corpus <path> --tokenizer <name> --output <csv>

The script computes:
- Tokens per word
- Tokens per grapheme
- Tokens per UTF-8 byte
- Tokens per sentence

This reference implementation is used to validate corrected versions.
"""

import argparse
import csv
from pathlib import Path
from typing import List, Tuple, Dict
import unicodedata


def tokenize_gpt2(text: str) -> List[int]:
    """Tokenize with GPT-2 (via tiktoken)."""
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return enc.encode(text)
    except ImportError:
        raise ImportError("tiktoken not installed. Install with: pip install tiktoken")


def tokenize_mbert(text: str) -> List[int]:
    """Tokenize with mBERT (via transformers)."""
    try:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
        return tokenizer.encode(text, add_special_tokens=False)
    except ImportError:
        raise ImportError("transformers not installed. Install with: pip install transformers")


def count_graphemes(text: str) -> int:
    """Count grapheme clusters (approximate using NFC normalization)."""
    # For most purposes, character count after NFC normalization approximates graphemes
    return len(unicodedata.normalize("NFC", text))


def count_bytes(text: str) -> int:
    """Count UTF-8 encoded bytes."""
    return len(text.encode("utf-8"))


def count_words(text: str) -> int:
    """Count words using split() (corrected from split(" "))."""
    return len(text.split())


def compute_metrics(text: str, tokens: List[int]) -> Dict:
    """Compute all fertility metrics for a text."""
    num_tokens = len(tokens)
    num_words = count_words(text)
    num_graphemes = count_graphemes(text)
    num_bytes = count_bytes(text)
    
    return {
        "tokens": num_tokens,
        "words": num_words,
        "graphemes": num_graphemes,
        "bytes": num_bytes,
        "tokens_per_word": num_tokens / num_words if num_words > 0 else 0,
        "tokens_per_grapheme": num_tokens / num_graphemes if num_graphemes > 0 else 0,
        "tokens_per_byte": num_tokens / num_bytes if num_bytes > 0 else 0,
    }


def process_corpus(filepath: str, tokenizer: str = "gpt2") -> Tuple[Dict, List[Dict]]:
    """Process a corpus file and compute aggregate metrics."""
    
    if tokenizer == "gpt2":
        tokenize_fn = tokenize_gpt2
    elif tokenizer == "mbert":
        tokenize_fn = tokenize_mbert
    else:
        raise ValueError(f"Unknown tokenizer: {tokenizer}")
    
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    aggregate = {
        "total_tokens": 0,
        "total_words": 0,
        "total_graphemes": 0,
        "total_bytes": 0,
        "num_sentences": 0,
    }
    
    sentence_metrics = []
    
    for line_num, line in enumerate(lines):
        line = line.rstrip("\n")
        if not line:
            continue
        
        try:
            tokens = tokenize_fn(line)
            metrics = compute_metrics(line, tokens)
            
            # Accumulate
            aggregate["total_tokens"] += metrics["tokens"]
            aggregate["total_words"] += metrics["words"]
            aggregate["total_graphemes"] += metrics["graphemes"]
            aggregate["total_bytes"] += metrics["bytes"]
            aggregate["num_sentences"] += 1
            
            # Store sentence-level
            sentence_metrics.append({
                "line": line_num,
                **metrics,
            })
        except Exception as e:
            print(f"Error processing line {line_num}: {e}")
            continue
    
    # Compute final metrics
    if aggregate["num_sentences"] > 0:
        aggregate["tokens_per_word"] = aggregate["total_tokens"] / aggregate["total_words"] if aggregate["total_words"] > 0 else 0
        aggregate["tokens_per_grapheme"] = aggregate["total_tokens"] / aggregate["total_graphemes"]
        aggregate["tokens_per_byte"] = aggregate["total_tokens"] / aggregate["total_bytes"]
        aggregate["tokens_per_sentence"] = aggregate["total_tokens"] / aggregate["num_sentences"]
    
    return aggregate, sentence_metrics


def main():
    parser = argparse.ArgumentParser(description="Measure tokenizer fertility on a corpus")
    parser.add_argument("--corpus", required=True, help="Path to corpus file")
    parser.add_argument("--tokenizer", default="gpt2", choices=["gpt2", "mbert"], help="Tokenizer to use")
    parser.add_argument("--output", default="fertility_report.csv", help="Output CSV file")
    
    args = parser.parse_args()
    
    print(f"Processing {args.corpus} with {args.tokenizer}...")
    
    aggregate, sentence_metrics = process_corpus(args.corpus, args.tokenizer)
    
    print("\n=== Aggregate Metrics ===")
    for key, value in aggregate.items():
        if isinstance(value, float):
            print(f"{key}: {value:.4f}")
        else:
            print(f"{key}: {value}")
    
    # Save sentence-level metrics
    with open(args.output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=sentence_metrics[0].keys())
        writer.writeheader()
        writer.writerows(sentence_metrics)
    
    print(f"\nSentence-level metrics saved to {args.output}")


if __name__ == "__main__":
    main()
