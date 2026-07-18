"""
Part C: Estimation of capacity implications and forward planning.

Estimates how the corrected metrics impact capacity provisioning,
cost allocation, and routing logic going forward.
"""

import json
from pathlib import Path


def estimate_capacity_impact():
    """Estimate capacity implications of corrected metrics."""
    
    # Corrected metrics (tokens per 1000 sentences)
    corrected_metrics = {
        "gpt2": {
            "english": 25820,  # 25.82 * 1000
            "hindi": 192410,
            "kannada": 350820,
            "tamil": 398360,
            "telugu": 336650,
        }
    }
    
    # Assume traffic distribution (hypothetical user base)
    traffic_distribution = {
        "english": 0.70,  # 70% English
        "hindi": 0.15,    # 15% Hindi
        "kannada": 0.05,  # 5% Kannada
        "tamil": 0.05,    # 5% Tamil
        "telugu": 0.05,   # 5% Telugu
    }
    
    results = {
        "question": "Part C: Capacity Estimation & Forward Planning",
        "scenario": "Hypothetical traffic distribution",
        "traffic_distribution": traffic_distribution,
        "estimations": []
    }
    
    for tokenizer, langs in corrected_metrics.items():
        total_tokens_per_1000_sentences = sum(
            langs[lang] * traffic_distribution.get(lang, 0)
            for lang in langs
        )
        
        tokens_per_sentence_avg = total_tokens_per_1000_sentences / 1000
        
        estimation = {
            "tokenizer": tokenizer,
            "tokens_per_1000_sentences": int(total_tokens_per_1000_sentences),
            "avg_tokens_per_sentence": f"{tokens_per_sentence_avg:.2f}",
            "language_breakdown": {}
        }
        
        for lang in langs:
            lang_tokens = langs[lang] * traffic_distribution.get(lang, 0)
            lang_contribution = 100 * lang_tokens / total_tokens_per_1000_sentences
            estimation["language_breakdown"][lang] = {
                "tokens_per_1000_sentences": int(lang_tokens),
                "percentage_of_load": f"{lang_contribution:.1f}%"
            }
        
        results["estimations"].append(estimation)
    
    # Cost implications
    results["cost_implications"] = {
        "prefill_cost": "Scales linearly with tokens_per_sentence",
        "kv_cache_cost": "Scales with tokens_per_sequence (output tokens)",
        "routing_logic": "Use weighted sum: sum(tokens_per_lang * traffic_pct)",
        "capacity_headroom": "Recommend 20% buffer above expected peak",
        "re_evaluation_frequency": "Quarterly or after major traffic shift"
    }
    
    # Recommendations
    results["recommendations"] = [
        "Deploy corrected metrics in routing immediately",
        "Validate against production traffic (parallel corpora may not reflect real patterns)",
        "Monitor actual vs predicted capacity utilization for 4 weeks",
        "If divergence >5%, investigate traffic distribution assumptions",
        "Plan for code-switching scenarios (not tested in this audit)"
    ]
    
    return results


def main():
    results = estimate_capacity_impact()
    
    output_file = Path(__file__).parent / "estimate_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print("Part C: Capacity Estimation")
    print("=" * 60)
    
    print("\nTraffic Distribution Assumption:")
    for lang, pct in results["traffic_distribution"].items():
        print(f"  {lang.capitalize()}: {pct * 100:.0f}%")
    
    print("\n\nEstimated Load:")
    for est in results["estimations"]:
        print(f"\n{est['tokenizer'].upper()}:")
        print(f"  Average tokens/sentence: {est['avg_tokens_per_sentence']}")
        print(f"  Per 1000 sentences: {est['tokens_per_1000_sentences']:,} tokens")
        for lang, breakdown in est["language_breakdown"].items():
            print(f"    {lang.capitalize()}: {breakdown['percentage_of_load']} load")
    
    print("\n\nCost Implications:")
    for key, val in results["cost_implications"].items():
        print(f"  {key}: {val}")
    
    print("\n\nRecommendations:")
    for i, rec in enumerate(results["recommendations"], 1):
        print(f"  {i}. {rec}")
    
    print(f"\nResults saved to {output_file}")


if __name__ == "__main__":
    main()
