# Decision memo — gated synthetic SFT pilot

## Recommendation

Choose **(a) synthetic casualized-pair SFT**, gated by native-speaker review.
Prompt-only is the day-1 baseline but is unlikely to override a formal prior
reliably across six languages. A ≤1B rewriter adds latency, tokens, and another
model to evaluate when review capacity is the constraint.

## Assumptions and arithmetic

Assume 10,000 responses × 6 languages = 60,000 pairs at 250 input+target
tokens: 15M tokens/epoch, 45M over three epochs. At a conservative 1,000
training tok/s, a 1B LoRA/QLoRA run costs 12.5 A100-hours (50 hours even at 4×
slower), within 336 A100-hours available in two weeks. The reviewer has 20
hours before launch; at 3 minutes/rating, that is 400 ratings: 200 Hindi and
200 Kannada. Reserve 160/language for held-out blind evaluation and 40 for
calibration. The other four languages have automated checks only; that is a
launch risk, not native validation.

## Success, kill, day 1

Success: on 100 blind held-out examples per reviewed language, at least **80%**
are rated casual/natural and at least **95%** preserve meaning, with no more
than a 3-point safety/style regression versus current outputs. Kill SFT by the
end of week 2 if either Hindi or Kannada is below 70% casual-natural, below 92%
meaning preservation, or has a ≥5-point safety regression after one
data-cleaning/retrain iteration. Ship only the prompt baseline if it clears the
same safety bar.

On day 1, prepare 100 Hindi and 100 Kannada held-out responses spanning
greeting, explanation, refusal, and task completion. Blindly compare current,
prompt-only, and a first 1,000-pair LoRA checkpoint; the reviewer ranks
casualness and flags meaning/safety errors. This tests the decision before
spending the A100 allocation on 60,000 unvalidated synthetic pairs.
