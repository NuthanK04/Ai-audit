# Corpus Selection Methodology

## Why FLORES-200?

FLORES-200 was chosen for this audit because:

1. **Official and Public**: Maintained by Meta AI, widely used in multilingual NLP research
2. **Balanced Coverage**: 997 parallel sentences across multiple language families
3. **Web Prose Domain**: Represents realistic translated content (not casual chat or code)
4. **Preserved Case and Punctuation**: Allows testing of actual casing and punctuation effects
5. **Known Source**: URLs and SHA-256 checksums recorded for reproducibility

## Corpus Limitations

This audit measures tokenization on **matched parallel content**, which has important limitations:

- **No code-switching**: Real user input often mixes languages within a single message
- **Limited context length**: FLORES sentences are short; doesn't test long-context behavior
- **Translated web prose**: Not representative of casual user traffic, chat interfaces, or code
- **Single domain**: Results may not generalize to specialized corpora (medical, legal, code)

## Alternative Corpora Considered

| Corpus | Reason Not Selected |
|--------|-------------------|
| Wikipedia | Very large but single-domain; code-switching common |
| Common Crawl | Massive diversity but no parallel alignment |
| mC4 | Multilingual but no ground truth alignment |
| Custom chat logs | Proprietary and not reproducible |

## Corpus Preparation

The `prepare_flores.py` script:
1. Downloads FLORES-200 dev set via Hugging Face Datasets
2. Filters to 5 target languages: English, Hindi, Kannada, Tamil, Telugu
3. Selects exactly 997 parallel sentences per language
4. Preserves case, punctuation, and NFC normalization
5. Records source metadata and SHA-256 hash
6. Saves to local CSV with per-sentence alignment

## Validation

The corpus is validated by:
- Checksum verification against known FLORES-200 release
- Line count verification (997 sentences per language)
- Character encoding validation (UTF-8)
- Whitespace and punctuation preservation check
