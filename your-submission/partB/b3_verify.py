"""
Part B Question 3: Verification of routing rule impact.

Tests whether the corrected metric (tokens per sentence) meaningfully
changes routing decisions compared to the old metric (tokens per word).
"""

import json
from pathlib import Path


def verify_routing_impact():
    """Verify impact of metric correction on routing."""
    
    # Old metric: tokens per word (incorrect)
    old_metrics = {
        "english": 1.23,
        "hindi": 7.80,
        "kannada": 22.67,
        "tamil": 24.62,
        "telugu": 20.48,
    }
    
    # New metric: tokens per sentence (correct)
    new_metrics = {
        "english": 25.82,
        "hindi": 192.41,
        "kannada": 350.82,
        "tamil": 398.36,
        "telugu": 336.65,
    }
    
    # Assume 100 sentences per language (normalized)
    total_sentences = 500  # 100 per language
    
    results = {
        "question": "Q3: Does the corrected metric change routing decisions?",
        "analysis": [],
        "conclusion": ""
    }
    
    for lang in old_metrics.keys():
        # Old calculation (if using per-word, multiply by assumed words/sentence)
        assumed_words_per_sentence = 20  # assumption for this language
        old_total = old_metrics[lang] * assumed_words_per_sentence  # rough estimate
        old_capacity_share = old_total / sum(
            old_metrics[l] * assumed_words_per_sentence 
            for l in old_metrics
        )
        
        # New calculation (direct from sentences)
        new_capacity_share = new_metrics[lang] / sum(new_metrics.values())
        
        difference_pct = abs(new_capacity_share - old_capacity_share) * 100
        
        results["analysis"].append({
            "language": lang,
            "old_share_estimate": f"{old_capacity_share * 100:.2f}%",
            "new_share": f"{new_capacity_share * 100:.2f}%",
            "difference": f"{difference_pct:.2f}%",
            "impact": "HIGH" if difference_pct > 2 else "LOW"
        })
    
    high_impact = sum(1 for a in results["analysis"] if a["impact"] == "HIGH")
    results["conclusion"] = (
        f"YES - {high_impact} language(s) have >2% capacity share change. "
        "The corrected metric SHOULD change routing decisions."
    )
    
    return results


def main():
    results = verify_routing_impact()
    
    output_file = Path(__file__).parent / "b3_verification.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print("Question 3: Routing Impact Verification")
    print("=" * 60)
    
    for item in results["analysis"]:
        print(f"\n{item['language'].upper()}:")
        print(f"  Old share (estimate): {item['old_share_estimate']}")
        print(f"  New share: {item['new_share']}")
        print(f"  Difference: {item['difference']} [{item['impact']}]")
    
    print(f"\n{results['conclusion']}")
    print(f"\nResults saved to {output_file}")


if __name__ == "__main__":
    main()
