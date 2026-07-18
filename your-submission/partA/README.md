# Part A — tokenizer audit

## Corpus and reproduction

`prepare_flores.py` downloads official FLORES-200 `dev` and writes 997 parallel
sentences each in English, Hindi, Kannada, Tamil and Telugu. It preserves case
and punctuation, normalizes NFC, removes empty lines, and records source URL
and SHA-256 in `data/flores_dev/SOURCE.txt`. FLORES is translated web prose, not
casual assistant traffic; it cannot estimate code-switching, long context, or
our traffic mix. It measures tokenization on matched content.

```powershell
python partA/prepare_flores.py --out partA/data/flores_dev
python partA/audit_tokenizers.py --data partA/data/flores_dev --tokenizer gpt2 --tokenizer hf:bert-base-multilingual-cased --out partA/results.csv
```

## Findings with measured evidence

| Claim | Measurement | Conclusion |
|---|---|---|
| Lowercasing changes the evaluated text. | GPT-2 English: 25,741 original tokens vs 26,696 lowercased (+3.71%); Hindi 191,828 vs 191,842 (+0.01%). | It distorts the comparison unevenly; corrected code retains case. |
| `split(" ")` miscounts whitespace words. | GPT-2 Kannada: 22.148 legacy vs 22.946 with `split()` (+3.60%). | Repeated spaces become empty “words” and understate fertility. |
| Mean sentence ratios is not total-token cost. | GPT-2 English macro 1.237 vs corpus-total 1.228 tok/word; Kannada 22.944 vs 22.668. | Capacity should weight sentences by their content/tokens. |
| Per-word fertility is the wrong routing headline. | GPT-2 Hindi/English: 6.35× by words but 7.45× by aligned sentence; mBERT: 1.51× vs 1.78×. | Words do not hold user content constant across languages. |
| NFC normalization looks suspicious but is fine. | FLORES lines are NFC-equivalent; token totals do not change. `random.seed` is unused (no random call). | Neither is a reported flaw. `strip()` only removes line-format whitespace, also fine. |

## Corrected totals: tokens divided by total units over 997 sentences

| tokenizer | language | tok/word | tok/grapheme | tok/UTF-8 byte | tok/aligned sentence |
|---|---:|---:|---:|---:|---:|
| GPT-2 | English | 1.23 | 0.21 | 0.21 | 25.82 |
| GPT-2 | Hindi | 7.80 | 2.33 | 0.59 | 192.41 |
| GPT-2 | Kannada | 22.67 | 4.06 | 0.98 | 350.82 |
| GPT-2 | Tamil | 24.62 | 4.20 | 1.00 | 398.36 |
| GPT-2 | Telugu | 20.48 | 4.56 | 0.99 | 336.65 |
| mBERT | English | 1.31 | 0.22 | 0.22 | 27.51 |
| mBERT | Hindi | 1.98 | 0.59 | 0.15 | 48.89 |
| mBERT | Kannada | 3.94 | 0.71 | 0.17 | 61.01 |
| mBERT | Tamil | 3.59 | 0.61 | 0.15 | 58.12 |
| mBERT | Telugu | 3.59 | 0.80 | 0.17 | 59.03 |

For routing, use input **tokens per aligned sentence** (production analogue:
tokens per stratified user request). Tokens drive prefill/KV work and alignment
holds semantic content far more constant than words, graphemes, or bytes.
