"""
Demonstration of whitespace splitting bug and correction.

The legacy split(" ") approach mishandles repeated whitespace,
counting empty strings as tokens and understating true fertility.
This script demonstrates the bug and validates the fix.
"""

import argparse
from pathlib import Path


def legacy_count_words(text: str) -> int:
    """Legacy approach using split(' ') - BUGGY."""
    return len(text.split(" "))


def corrected_count_words(text: str) -> int:
    """Corrected approach using split() without argument."""
    return len(text.split())


def analyze_file(filepath: str) -> dict:
    """Compare legacy vs corrected word counting."""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    results = {
        "total_lines": len(lines),
        "samples": [],
        "aggregate_legacy": 0,
        "aggregate_corrected": 0,
        "divergence_pct": 0.0,
    }
    
    for i, line in enumerate(lines[:100]):  # Sample first 100 lines
        line = line.rstrip("\n")
        legacy = legacy_count_words(line)
        corrected = corrected_count_words(line)
        
        if legacy != corrected:
            results["samples"].append({
                "line_num": i,
                "text": line,
                "legacy_words": legacy,
                "corrected_words": corrected,
                "difference": corrected - legacy,
            })
        
        results["aggregate_legacy"] += legacy
        results["aggregate_corrected"] += corrected
    
    if results["aggregate_legacy"] > 0:
        results["divergence_pct"] = (
            100 * (results["aggregate_legacy"] - results["aggregate_corrected"]) 
            / results["aggregate_legacy"]
        )
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Demonstrate split() vs split(' ') bug")
    parser.add_argument("--file", required=True, help="Text file to analyze")
    parser.add_argument("--out", default="split_fix_report.json", help="Output file")
    args = parser.parse_args()
    
    import json
    
    results = analyze_file(args.file)
    
    with open(args.out, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"Analysis complete. Report saved to {args.out}")
    print(f"Divergence: {results['divergence_pct']:.2f}%")
    print(f"Sample mismatches found: {len(results['samples'])}")


if __name__ == "__main__":
    main()
