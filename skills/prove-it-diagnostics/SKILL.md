---
name: prove-it-diagnostics
description: Prove it for debugging, performance investigation, bottleneck analysis, profiling, and optimization work. When reading code does not prove the cause, run a minimal reproduction, add temporary traces, measure bottlenecks, and verify the fix or improvement.
---

# Prove It Diagnostics

Code reading can close a debugging or performance case only when the cause is proven from the source.

If reading code proves the cause, use that proof. You do not need to build a separate reproduction just to satisfy this skill. Still, verify the fix with the smallest available check.

If reading code reveals an obvious cause, such as an impossible condition, a wrong variable, a missing await, a malformed input transformation, an accidental quadratic loop, an unnecessary repeated allocation, or a call that cannot reach the intended branch, fix that cause and verify it with the smallest available check.

If reading code suggests a cause but does not prove it with enough certainty to rule out other plausible explanations, prove it. Do not patch, refactor, or optimize from a source-reading guess.

## Steps

1. Classify the claim.

   Decide whether the cause is source-proven or still only plausible.

   Source-proven means you can name the exact code path, the exact failing condition or slow operation, and why competing explanations cannot produce the observed behavior.

   Completion criterion: either write the source-proven cause with the code path that proves it, or state that the cause is not yet proven and move to a runnable or measurable check.

2. Reproduce or measure the behavior.

   For debugging, build the smallest reproduction that exercises the suspected behavior. Prefer a temporary file, a REPL, a local script, a unit test, or an isolated test case over reasoning from the full application.

   For performance work, establish a baseline before changing code. Prefer a benchmark, profiler output, repeated timing measurement, flamegraph, trace, or targeted timing log over visual inspection of code.

   The reproduction or measurement should remove unrelated framework, network, UI, database, and timing variables unless those variables are the suspected cause.

   Completion criterion for debugging: the reproduction fails before the fix or shows the wrong value, wrong branch, thrown error, race, or state transition.

   Completion criterion for performance work: the benchmark, profiler output, timing log, or repeated measurement shows the slow operation before the change.

3. Trace the boundary.

   When the reproduction or measurement still leaves uncertainty, add temporary traces inside the affected area. Log values, branch entry, timing, input shape, output shape, cache hits, loop counts, allocation counts, query counts, and async boundaries where they can separate competing explanations.

   Trace from the outside inward until you know the last point that behaves correctly and the first point that behaves incorrectly.

   For performance work, measure each plausible segment until you know which segment consumes the time. Do not optimize the code that merely looks expensive.

   Completion criterion: you can name the boundary: the last-correct point and first-wrong point for bugs, or the measured bottleneck for performance.

4. Make the smallest causal change.

   Change the code that the reproduction, traces, benchmark, or profiler identified. Avoid incidental rewrites, style edits, broad refactors, and speculative cleanup while the cause is still under test.

   Completion criterion for debugging: the same reproduction that failed before now passes, and at least one relevant existing test or application path still works.

   Completion criterion for performance work: the same measurement method shows improvement against the baseline, and the result still produces correct output.

5. Clean the workspace and report the evidence.

   Remove temporary logs, temporary files, throwaway scripts, and benchmark scaffolding unless they should become permanent tests, benchmarks, or diagnostics.

   Report the cause, the evidence that proved it, the change made, and the verification that passed.

   Completion criterion: no accidental temporary instrumentation remains, and the final explanation distinguishes observed facts from remaining uncertainty.

## Rules

A fix without a failing reproduction, trace boundary, or measurement is a hypothesis. Treat it as unproven.

An optimization without a baseline and follow-up measurement is a guess. Treat it as unproven.

A passing reproduction after the fix proves only the reproduced case. Do not claim broader certainty unless you also verified the broader path.

A faster benchmark after the change proves only the measured case. Do not claim a general performance improvement unless the benchmark represents the real workload.

If you made a fix or optimization and the user reports that the bug remains or performance did not improve, treat the original cause as unproven. Return to the Steps, reproduce or measure the behavior, trace the boundary, and verify the next change with evidence before claiming it is fixed or improved.

Temporary logs are allowed when they reduce uncertainty. Add them aggressively when stuck, but remove them before finishing unless the user wants permanent diagnostics.

Performance work needs a baseline. Use repeated timings, a profiler, or a benchmark before changing code, then reuse the same method after changing code.

When the environment prevents execution, say which command, file, REPL input, test, log, benchmark, or profiler run would prove the claim. Do not present an unrun hypothesis as a confirmed cause.
