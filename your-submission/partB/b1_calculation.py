"""
Part B Question 1: Capacity calculation from corrected tokenizer metrics.

Calculates capacity implications based on the corrected tokens-per-sentence metric.
"""

import json
from pathlib import Path


def calculate_capacity_distribution():
    """Calculate capacity distribution across languages."""
    
    # Corrected metrics from Part A (tokens per aligned sentence)
    metrics = {
        "gpt2": {
            "english": 25.82,
            "hindi": 192.41,
            "kannada": 350.82,
            "tamil": 398.36,
            "telugu": 336.65,
        },
        "mbert": {
            "english": 27.51,
            "hindi": 48.89,
            "kannada": 61.01,
            "tamil": 58.12,
            "telugu": 59.03,
        }
    }
    
    results = {
        "question": "Q1: What is the corrected capacity distribution?",
        "methodology": "tokens_per_sentence",
        "tokenizers": {}
    }
    
    for tokenizer, langs in metrics.items():
        total_tokens = sum(langs.values())
        results["tokenizers"][tokenizer] = {
            "by_language": langs,
            "total_tokens": total_tokens,
            "percentage_by_language": {
                lang: (tokens / total_tokens * 100)
                for lang, tokens in langs.items()
            }
        }
    
    return results


def main():
    results = calculate_capacity_distribution()
    
    output_file = Path(__file__).parent / "b1_calculation.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print("Question 1: Capacity Distribution")
    print("=" * 60)
    
    for tokenizer, data in results["tokenizers"].items():
        print(f"\n{tokenizer.upper()}:")
        print(f"  Total tokens: {data['total_tokens']:.0f}")
        for lang, pct in data["percentage_by_language"].items():
            tokens = data["by_language"][lang]
            print(f"    {lang.capitalize()}: {pct:.1f}% ({tokens:.0f} tokens)")
    
    print(f"\nResults saved to {output_file}")


if __name__ == "__main__":
    main()
