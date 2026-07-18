# Routing recommendation

GPT-2 needs 25.82 English tokens per aligned sentence versus 192.41 Hindi
(7.45×), 350.82 Kannada (13.59×), 398.36 Tamil (15.43×), and 336.65 Telugu
(13.04×). That is tokenizer mismatch, not an intrinsic script cost: multilingual
BERT reduces Hindi/English to 1.78× and each Dravidian language to 2.11–2.22×.

Route Indic traffic only to a model whose actual serving tokenizer passes this
matched-request test. Do not budget a blanket 6× Hindi multiplier. Validate
quality, latency, and cost together before routing. The major caveat is that
FLORES is translated web prose rather than casual, code-switched assistant
traffic. Monitor p50/p95 **input tokens per user turn by language and intent
bucket**, plus tokenizer version, to catch that mismatch in production.
