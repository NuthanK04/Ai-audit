# AI Audit Assignment

A comprehensive audit of AI tokenizer behavior and multilingual capacity allocation, with reproducible experiments and documented findings.

## Quick Start

### Part A: Tokenizer Audit
Evaluate tokenizer behavior across multiple languages using official FLORES-200 dataset:

```powershell
cd partA
python prepare_flores.py --out data/flores_dev
python audit_tokenizers.py --data data/flores_dev --tokenizer gpt2 --tokenizer hf:bert-base-multilingual-cased --out results.csv
```

### Part B: Verification & Calculation
Run verification scripts to validate capacity allocation:

```powershell
cd partB
python b1_calculation.py
python b3_verify.py
python b4_verify.py
```

### Part C: Estimation
Estimate capacity implications:

```powershell
cd partC
python estimate.py
```

## Project Structure

```
├── README.md                          # This file
├── NOTEBOOK.md                        # Chronological research log
├── REPORT_v0.md                       # Initial findings report
├── fertility.py                       # Reference tokenizer implementation
├── partA/                             # Tokenizer Audit
│   ├── README.md                      # Full Part A documentation
│   ├── prepare_flores.py              # Download FLORES-200 corpus
│   ├── audit_tokenizers.py            # Run tokenizer comparison
│   ├── experiments.py                 # Additional tokenizer experiments
│   ├── fertility_split_fix.py         # Whitespace handling fix
│   ├── fertility_ratio_fix.py         # Normalization fix validation
│   ├── corpus_selection.md            # Corpus methodology
│   ├── results.csv                    # Measured tokenizer metrics
│   ├── results.md                     # Results interpretation
│   ├── recommendation_memo.md         # Key findings summary
│   ├── requirements.txt               # Python dependencies
│   └── data/
│       └── flores_dev/                # FLORES-200 multilingual corpus
├── partB/                             # Capacity Allocation
│   ├── answers.md                     # Written answers
│   ├── b1_calculation.py              # Question 1 calculations
│   ├── b3_verify.py                   # Question 3 verification
│   ├── b4_verify.py                   # Question 4 verification
│   └── memo.md                        # Analysis notes
├── partC/                             # Estimation
│   ├── memo.md                        # Methodology and findings
│   ├── estimate.py                    # Capacity estimation
│   └── results.md                     # Estimation results
├── starter_kit/                       # Reference materials
│   ├── fertility.py
│   ├── REPORT_v0.md
│   ├── bench/
│   └── corpus_sample/
├── bench/                             # Benchmark logs
└── corpus_sample/                     # Sample corpus reference
```

## Documentation

### NOTEBOOK.md
Chronological research log tracking:
- Hypothesis → Experiment → Result → Conclusion
- Key decisions and pivots
- Evidence-grounded reasoning

### AI_USAGE.md
Summary of AI assistance during the assignment:
- Tools and techniques
- Decision support
- Code review

## Key Findings

### Part A: Tokenizer Audit
- **Whitespace handling** causes significant measurement errors (up to 3.6%)
- **Mean sentence ratios** do not directly translate to capacity costs
- **Per-word fertility** is not the right routing metric; use **tokens per aligned sentence**
- Measured corrections show GPT-2 Hindi/English divergence is **7.45×** (not 6.35×)

### Part B: Capacity Allocation
See [partB/answers.md](partB/answers.md)

### Part C: Estimation
See [partC/memo.md](partC/memo.md)

## Technologies & Dependencies

### Core Language & Runtime
- **Python 3.9+** — Primary programming language
- **PowerShell 5.1** — Terminal/scripting for environment management

### Data & Tokenization
- **Hugging Face Transformers** — BERT multilingual tokenizer implementation
- **Hugging Face Datasets** — FLORES-200 corpus download and management
- **tiktoken** — OpenAI's GPT-2/GPT-3 tokenizer reference implementation
- **Unicode (unicodedata)** — NFC normalization and character handling

### Data Processing & Analysis
- **pandas** — CSV aggregation, metrics computation, data frames
- **csv (stdlib)** — Results serialization and logging
- **json (stdlib)** — Structured output for verification scripts

### Verification & Testing
- **pytest** — Unit testing framework (for verification scripts)
- **pathlib** — Cross-platform file path handling
- **argparse** — Command-line argument parsing for reproducibility

### Development & Version Control
- **Git** — Version control (GitHub repository)
- **Python Standard Library** — csv, json, pathlib, argparse, unicodedata, collections

### Environment
- **VS Code** — Development editor
- **GitHub** — Remote repository and version history

## Methodology

All conclusions are supported by:
✓ Reproducible code with fixed seeds  
✓ Public datasets (FLORES-200)  
✓ Measured evidence over assertions  
✓ Cross-checked calculations  
✓ Verification scripts  

## Development Notes

This repository was developed incrementally with multiple Git commits reflecting the progression from reproduction to experimentation to analysis. The commit history mirrors the research process.

---

**Assignment:** Flan AI (Multilingual Tokenizer Audit)  
**Date:** July 2026
