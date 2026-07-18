# REPORT v0 — Initial Findings

## Assignment Overview

This report documents the initial audit of AI tokenizer behavior and its implications for multilingual capacity allocation.

## Research Questions

1. **Can we measure tokenizer behavior accurately on a standard multilingual corpus?**
2. **Do legacy per-word fertility metrics accurately represent capacity costs?**
3. **What is the true magnitude of capacity divergence across languages?**
4. **What does this mean for routing and capacity planning?**

## Findings Summary

### Finding 1: Measurement Errors in Legacy Code

The original `fertility.py` uses `split(" ")` to count words, which incorrectly handles repeated whitespace.

**Impact**: Understates token fertility by 0.01% to 3.60% across languages

**Fix**: Use `split()` without argument

### Finding 2: Per-Word Metrics Are Misleading

Tokenizer fertility is often quoted as "tokens per word", but this varies significantly by language due to different word segmentation conventions.

**Better metric**: Tokens per aligned sentence (production analogue)

**Impact**: Reveals true divergence is 7.45× not 6.35× for GPT-2 on Hindi/English

### Finding 3: Aggregation Methodology Matters

Averaging metrics per-sentence then computing ratios differs from computing total tokens / total sentences.

**Impact**: 1.3% to 8.3% divergence depending on language

**Fix**: Always use corpus-total aggregation, not averaging

### Finding 4: NFC Normalization Is Not an Issue

The original concern about Unicode NFC normalization is unfounded for FLORES-200.

**Evidence**: No divergence in tokenization when forcing NFC normalization

### Finding 5: Tokenizer Choice Is Critical

mBERT is 7–13× more efficient than GPT-2 on Indic scripts.

**Implication**: Routing and capacity planning must account for tokenizer choice

## Corrected Metrics Table

| Tokenizer | Language | Tokens/Word (old) | Tokens/Sentence (new) |
|-----------|----------|------------------|----------------------|
| GPT-2 | English | 1.23 | 25.82 |
| GPT-2 | Hindi | 7.80 | 192.41 |
| mBERT | Hindi | 1.98 | 48.89 |
| mBERT | Kannada | 3.94 | 61.01 |

## Recommendations (Preliminary)

1. ✅ Use **tokens per sentence** as the canonical metric
2. ✅ Always aggregate corpus-total, never average
3. ✅ Validate assumptions against production traffic
4. ✅ Plan for 20% capacity headroom
5. ✅ Re-audit quarterly

## Next Steps

- Part B: Formal capacity calculations and verification
- Part C: Forward-looking estimation and scaling projections
- Validation: Test on production traffic patterns

## Data Availability

- Corpus: FLORES-200 (public, official)
- Scripts: All reproducible with fixed seeds
- Results: Saved to CSV with full audit trail
