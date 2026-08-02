---
name: prove-it-diagnostics
description: Prove it for debugging, performance investigation, bottleneck analysis, profiling, and optimization work. When reading code does not prove the cause, run a minimal reproduction, add temporary traces, measure bottlenecks, and verify the fix or improvement.
license: MIT
metadata:
  author: Robot-Inventor
---

# Prove It Diagnostics

Use this skill to pinpoint the causes of bugs and performance bottlenecks and fix them. Reading code alone may not reveal the source of a bug or bottleneck. Do not claim that a speculative code change fixed a bug or improved performance. Run the code, gather evidence, identify the cause, and verify the fix.

## Steps

The following is the core of this skill; please follow the specified steps.

## 1. Establish a performance baseline for optimization tasks

For performance optimization tasks, create and run a benchmark before making changes. Run the benchmark as many times as practical. Use averages, percentiles, and other relevant statistics to establish a stable baseline instead of relying on a single run.

## 2. Read the code

Read the code related to the bug or performance issue. For debugging tasks, you may fix the issue and skip the remaining steps when you find a clear cause, such as an incorrect operator or an obvious contradiction in the logic.

Continue with the remaining steps when you cannot identify the cause with confidence or when you find suspicious code but lack enough evidence to blame it.

### 3. Verify the cause

Do not rely on code inspection alone. Run experiments to identify the source of the bug or bottleneck.

For debugging tasks:

1. Create a reproduction in a temporary file or REPL and run it to confirm the bug. If the reproduction does not fail, add relevant behavior from the target code until it reproduces the bug.
2. Remove or revert each part of the reproduction to find the smallest program that still triggers the bug. A minimal reproduction narrows the list of possible causes.
3. Investigate the minimal reproduction, identify the cause, and fix it. Address the root cause instead of applying a superficial workaround, as described in the Rules section.
4. Confirm that the fix prevents the bug in the minimal reproduction.
5. Apply the fix to the production code and confirm that it resolves the original bug. If the bug remains, return to the reproduction step and repeat the process.

For performance optimization tasks:

1. Use benchmarks, profilers, timing logs, or similar tools to identify the slow operation.
2. Fix the bottleneck, then use the same measurements to confirm that performance improved.
3. Apply the fix to the production code and confirm the improvement there. If performance does not improve, return to bottleneck analysis and repeat the process.

### 4. Clean up

Remove temporary logs, reproduction code, generated files, and log data created during verification.

## Rules

If a user reports that your fix did not resolve the bug or improve performance, treat your previous diagnosis as unverified and restart the investigation.

Surface-level and stop-gap fixes are shameful; identify and fix the root cause. For example, when an error triggers a bug, find and fix the source of the error instead of adding a fallback for the failure. Keep asking yourself, “Is this the root cause?”

When evidence points to a bug in a dependency, do not patch the dependency. Tell the user that the dependency appears to contain a bug, describe the evidence, and propose changes they can make in their project without modifying the dependency.

When you get stuck, try these approaches:

- Add temporary logs across the affected path. Use them to find the boundary between correct and incorrect behavior, or between fast and slow execution.
- When behavior contradicts the code’s logic or you cannot make progress, search the relevant library’s GitHub issues and pull requests, Stack Overflow, and community articles for reports of the same problem and possible solutions.
