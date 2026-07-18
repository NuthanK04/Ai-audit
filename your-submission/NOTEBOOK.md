# Lab notebook

## 2026-07-18 — establish the baseline

Hypothesis: the 10-line corpus and a single GPT-2 tokenizer are insufficient for
a routing decision. I read `fertility.py`, the report, model spec, and log.
Result: the report's Hindi result is a smoke test, not an evaluation. Revision:
use a parallel corpus and retain the legacy metric only as a measured baseline.

## 2026-07-18 — corpus-source dead end

Hypothesis: the original FLORES short URL would make preparation reproducible.
Experiment: ran the downloader against `https://tinyurl.com/flores200dataset`.
Result: it returned a TinyURL HTML landing page, not an archive (`BadZipFile`).
Revision: use the published direct archive URL
`https://dl.fbaipublicfiles.com/nllb/flores200_dataset.tar.gz`; record its
SHA-256 after download. The successful run wrote 997 parallel dev sentences in
five languages.

## 2026-07-18 — audit code and metric

Hypothesis: lowercasing, literal-space splitting, and macro averaging change
the reported statistic. Experiment: compare each variant on the 997-sentence
corpus with GPT-2 and multilingual BERT. Result: GPT-2 English changes +3.71%
under lowercasing; literal-space splitting understates Kannada by 3.60%; macro
and corpus-total ratios differ by up to 1.20% in tested examples. Revision:
keep original case, use `split()`, and sum numerator/denominator before division.

Surprise: NFC normalization and the seeded `random` import initially looked
like likely defects. Testing showed the FLORES lines are NFC-equivalent and no
random function is called. I therefore did not report either as a flaw.

## 2026-07-18 — choose the decision denominator

Hypothesis: whitespace words are an adequate common denominator. Experiment:
compare word and aligned-sentence ratios. Result: GPT-2 Hindi/English is 6.35×
per word but 7.45× per aligned sentence; multilingual BERT is 1.51× vs 1.78×.
Revision: use tokens per aligned sentence for matched-content routing analysis;
production counterpart is tokens per stratified user request.

## 2026-07-18 — reconcile serving data

Hypothesis: batch-48 linear scaling is plausible. Experiment: derive KV bytes
and generated-only goodput from the CSV. Result: 112 KiB KV/token and about 27
full sequences predict pressure near the observed batch-24/32 boundary.
`reported_tok_s` includes prompt tokens: batch-24 long output goodput is only
200.9 generated tok/s by both wall-clock and counter rescaling. Revision: cap
long L4 admission at 24 or add replicas; reject the batch-48 extrapolation.
