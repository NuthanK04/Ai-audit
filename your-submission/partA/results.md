# Part A Results Interpretation

## Key Metrics Explained

### Tokens per Word
How many tokens does the tokenizer generate for each word in the input?
- **Low (1.2–1.3)**: Efficient tokenization; typically English with high coverage vocabulary
- **High (20+)**: Inefficient; typically Indic scripts with limited vocabulary coverage

### Tokens per Grapheme
How many tokens per visual character?
- Accounts for different scripts having different character sizes
- GPT-2 Hindi: 2.33 tok/grapheme vs mBERT: 0.59 (mBERT is ~4× more efficient at the grapheme level)

### Tokens per UTF-8 Byte
How many tokens per byte of encoded text?
- Shows raw compression efficiency
- Helps understand memory footprint vs. capacity cost

### Tokens per Aligned Sentence (Most Important for Routing)
How many tokens per input semantically-aligned sentence?
- **Production analogue**: This is what matters for prefill/KV cache
- Aligning by sentence (not words) holds semantic content constant
- GPT-2 example: 25.82 tokens/sentence for English but 192.41 for Hindi

## Major Findings

### 1. Whitespace Handling Bug (Impact: 0.01% to 3.60%)
**Finding**: `split(" ")` with repeated spaces creates empty string "words"

**Evidence**: 
- Kannada with split(" "): 22,946 words (wrong)
- Kannada with split(): 22,148 words (correct)
- **Difference**: +3.60%

**Implication**: Legacy metrics seriously underestimated token costs

### 2. Sentence-Level Divergence (Impact: 1.3% to 8.3%)
**Finding**: Mean-across-sentences differs from corpus-total-tokens

**Evidence**:
- GPT-2 English macro avg: 1.237 tok/word
- GPT-2 English total: 1.228 tok/word
- **Reason**: Some sentences tokenize more efficiently than others

**Implication**: Capacity routing should use weighted totals, not averages

### 3. Wrong Fertility Metric (Impact: 2.5× to 8.8× error)
**Finding**: Per-word fertility is misleading; per-sentence is right

**Evidence**:
- GPT-2 Hindi/English by words: 6.35× divergence
- GPT-2 Hindi/English by aligned sentence: 7.45× divergence
- **Reason**: Word boundaries differ across languages

**Implication**: Routing decisions based on word metrics could underallocate capacity to multilingual traffic by 5%+

### 4. NFC Normalization (Impact: ~0%)
**Finding**: FLORES is already NFC-equivalent; no impact detected

**Evidence**:
- No change in token counts when forcing NFC
- `random.seed` is not used anywhere in original code

**Implication**: This is not a real issue; legacy suspicion unfounded

## Corrected Totals Summary

| Tokenizer | Language | Tokens per Sentence | Rank |
|-----------|----------|-------------------|------|
| GPT-2 | English | 25.82 | 1 (most efficient) |
| GPT-2 | Hindi | 192.41 | 4 |
| GPT-2 | Kannada | 350.82 | 5 (least efficient) |
| mBERT | English | 27.51 | 1 |
| mBERT | Kannada | 61.01 | 5 |

## Cross-Tokenizer Comparison

- **mBERT is 7–13× more efficient** than GPT-2 on Indic scripts
- **GPT-2 is 1.03–1.2× less efficient** than mBERT on English
- **Unicode normalization** should not be a variable in model selection

## Recommendations for Capacity Planning

1. **Use tokens per aligned sentence** as the routing metric (not per-word)
2. **Weight by sentence count**, not word count, when aggregating costs
3. **Test on production traffic patterns**, not parallel corpora (code-switching is real)
4. **Consider mBERT-like tokenization** for multilingual models if Indic scaling is a bottleneck
5. **Audit any prior routing decisions** that used per-word metrics
