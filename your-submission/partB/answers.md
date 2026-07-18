# Part B — capacity reconciliation

## B1

KV bytes/token = `28 layers × 8 KV heads × 128 dimensions × 2 (K,V) × 2 bytes`
= **114,688 bytes = 112 KiB/token**. Weights use about `4.2B × 2 = 8.4 GB`.
Assuming 24 GiB advertised memory, KV budget is `0.92 × 24 − 8.4 − 1.6 = 12.08
GiB`. A 4,096-token sequence needs `4096 × 112 KiB = 448 MiB`; therefore
`12.08 GiB / 448 MiB = 27.6`, or about **27 sequences**. At long batch 24 the
log is already 0.93 KV utilization; at 32 it is 0.97 with 7 preemptions. This
matches the prediction (rounding/allocator blocks explain the difference).

## B2

Long-context reported throughput peaks at batch 24 (1607.4 tok/s), then falls
to 1384.0 at 32 and 1298.5 at 48. KV utilization is `0.93 → 0.97 → 0.97`,
preemptions `0 → 7 → 23`, and p50 TTFT `500.5 → 636.9 → 955.4 ms`. KV-cache
exhaustion causes eviction/recompute or swapping, turning added requests into
cache churn. Cap a long-context L4 at 24 active requests or route overflow to
another replica. For batch 32 this predicts retaining about 1607 rather than
1384 reported tok/s (+16%) and zero preemptions. Two batch-24 replicas would
give about `2 × 200.9 = 401.8` generated tok/s for 48 requests, versus 162.3
generated tok/s in the single batch-48 run.

## B3

`reported_tok_s` counts prompt **plus** generated tokens, so long prompts
inflate it without proving faster reply generation. Batch-24 long honest
goodput is **200.9 generated tok/s**, independently:

```text
24 × 512 / 61.16 = 200.9
1607.4 × 512 / (3584 + 512) = 200.9
```

The report should call 1607.4 end-to-end processed tok/s, not generation
throughput; long prompts worsen TTFT and do not establish faster replies.
Batch 48 is 1298.5 reported tok/s, not 3200, and preempts 23 sequences, so the
linear extrapolation is contradicted by the log.

## B4

Pull the scheduler's cumulative `num_preemptions_total`, segmented by prompt
length. It should be zero through long batch 24 and rise by about 7 at batch 32
and 23 at batch 48, alongside saturated KV blocks and rising TTFT. That
confirms cache pressure rather than compute saturation.
