"""
Additional tokenizer experiments for comparative analysis.

This script runs supplementary experiments beyond the core audit:
- Edge case handling (special characters, URLs, mixed scripts)
- Compression ratio analysis
- Token distribution patterns
"""

import argparse
import json
import csv
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple

try:
    import tiktoken
except ImportError:
    tiktoken = None

try:
    from transformers import AutoTokenizer
except ImportError:
    AutoTokenizer = None


def analyze_edge_cases(text: str, tokenizer_name: str) -> Dict:
    """Analyze tokenizer behavior on edge cases."""
    cases = {
        "urls": "Visit https://example.com for more info",
        "special_chars": "Hello!!! @#$% &*()",
        "mixed_script": "Hello नमस्ते 你好",
        "repeated_spaces": "hello    world",
        "tabs_newlines": "line1\n\tline2",
        "unicode_emoji": "Hello 👋 World 🌍",
        "code_snippet": "def foo(): return x + y",
    }
    
    results = {}
    for case_name, case_text in cases.items():
        try:
            if tokenizer_name == "gpt2" and tiktoken:
                enc = tiktoken.get_encoding("cl100k_base")
                tokens = enc.encode(case_text)
            elif tokenizer_name.startswith("hf:") and AutoTokenizer:
                model_name = tokenizer_name.replace("hf:", "")
                tok = AutoTokenizer.from_pretrained(model_name)
                tokens = tok.encode(case_text)
            else:
                tokens = []
            
            results[case_name] = {
                "text": case_text,
                "token_count": len(tokens),
                "tokens_per_char": len(tokens) / len(case_text) if case_text else 0,
            }
        except Exception as e:
            results[case_name] = {"error": str(e)}
    
    return results


def analyze_distribution(text: str, tokenizer_name: str) -> Dict:
    """Analyze token distribution patterns."""
    try:
        if tokenizer_name == "gpt2" and tiktoken:
            enc = tiktoken.get_encoding("cl100k_base")
            tokens = enc.encode(text)
        elif tokenizer_name.startswith("hf:") and AutoTokenizer:
            model_name = tokenizer_name.replace("hf:", "")
            tok = AutoTokenizer.from_pretrained(model_name)
            tokens = tok.encode(text)
        else:
            tokens = []
        
        token_counter = Counter(tokens)
        
        return {
            "total_tokens": len(tokens),
            "unique_tokens": len(token_counter),
            "most_common_top10": dict(token_counter.most_common(10)),
            "avg_token_id": sum(tokens) / len(tokens) if tokens else 0,
        }
    except Exception as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Run additional tokenizer experiments")
    parser.add_argument("--tokenizer", default="gpt2", help="Tokenizer to use (gpt2 or hf:<model>)")
    parser.add_argument("--out", default="experiments_results.json", help="Output file")
    args = parser.parse_args()
    
    results = {
        "edge_cases": analyze_edge_cases("test sample", args.tokenizer),
        "metadata": {
            "tokenizer": args.tokenizer,
            "note": "Supplementary experiments for tokenizer analysis"
        }
    }
    
    with open(args.out, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"Experiments complete. Results saved to {args.out}")


if __name__ == "__main__":
    main()
