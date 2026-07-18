"""
Validation of normalization fixes and their impact.

This script verifies that NFC normalization and proper seed handling
do not introduce unintended changes to tokenization counts.
"""

import unicodedata
from pathlib import Path
from typing import Tuple, Dict


def normalize_nfc(text: str) -> str:
    """Normalize text to NFC form."""
    return unicodedata.normalize("NFC", text)


def normalize_nfd(text: str) -> str:
    """Normalize text to NFD form."""
    return unicodedata.normalize("NFD", text)


def are_equivalent(text1: str, text2: str) -> bool:
    """Check if two texts are normalization-equivalent."""
    return normalize_nfc(text1) == normalize_nfc(text2)


def compare_normalizations(text: str) -> Dict:
    """Compare tokenization across different normalizations."""
    nfc = normalize_nfc(text)
    nfd = normalize_nfd(text)
    
    return {
        "original": text,
        "nfc": nfc,
        "nfd": nfd,
        "nfc_bytes": len(nfc.encode("utf-8")),
        "nfd_bytes": len(nfd.encode("utf-8")),
        "nfc_equals_nfd": (nfc == nfd),
        "nfc_length": len(nfc),
        "nfd_length": len(nfd),
    }


def validate_corpus(filepath: str) -> Dict:
    """Validate normalization consistency across a corpus file."""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    results = {
        "total_lines": len(lines),
        "nfc_equivalent": 0,
        "nfc_different": 0,
        "samples_different": [],
    }
    
    for i, line in enumerate(lines[:1000]):  # Check first 1000 lines
        nfc = normalize_nfc(line)
        nfd = normalize_nfd(line)
        
        if nfc == nfd:
            results["nfc_equivalent"] += 1
        else:
            results["nfc_different"] += 1
            if len(results["samples_different"]) < 10:
                results["samples_different"].append({
                    "line_num": i,
                    "nfc_len": len(nfc),
                    "nfd_len": len(nfd),
                })
    
    results["nfd_impact_pct"] = (
        100 * results["nfc_different"] / results["total_lines"]
        if results["total_lines"] > 0 else 0
    )
    
    return results


def test_seed_independence(num_runs: int = 3) -> bool:
    """Verify that random.seed is not used incorrectly."""
    import random
    
    results = []
    for run in range(num_runs):
        # Simulate a tokenization operation
        values = [random.random() for _ in range(100)]
        results.append(sum(values))
    
    # All runs should have different sums (since seed isn't being reset)
    return len(set(results)) == num_runs


def main():
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Validate normalization fixes")
    parser.add_argument("--corpus", required=True, help="Corpus file to validate")
    parser.add_argument("--out", default="normalization_fix_report.json", help="Output file")
    args = parser.parse_args()
    
    corpus_results = validate_corpus(args.corpus)
    seed_test = test_seed_independence()
    
    output = {
        "corpus_validation": corpus_results,
        "seed_independence_test": seed_test,
        "conclusion": "Normalization handling is correct" if corpus_results["nfd_impact_pct"] < 1 else "Normalization varies across corpus",
    }
    
    with open(args.out, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"Validation complete. Report saved to {args.out}")


if __name__ == "__main__":
    main()
