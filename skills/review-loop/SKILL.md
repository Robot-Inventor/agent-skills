---
name: review-loop
description: Improve code quality by requesting a review from a subagent. Use for any task that edits code or configuration.
license: MIT
metadata:
    author: Robot-Inventor
---

# Review Loop Skill

Improve code quality by repeatedly requesting a review from a subagent after editing code. Reviews are important because they can identify issues that might be missed through self-review. Ignore this skill when the user explicitly instructs to skip the review-loop.

## Steps

### 1. Request a code review

Request a code review from a subagent. If you have the option to choose whether to fork the context or launch the subagent in an isolated context when starting it, **always** launch it in an isolated context. Code reviews by sub-agents can take time. Do not restart subagents or send additional prompts to rush them simply because the review is not yet complete or because the response is taking a while.

When requesting a review from subagents, be sure to use the following template instead of a free-form format.

```md
You are a code review agent. Review the code by reading the instructions in `~/.agents/skills/review-loop/references/review-instructions.md`.

- Scope: {uncomitted changes / filepath etc.}
- User's instructions: {user's feature requests / instructions etc.}
```

### 2. Receive reviews and improve your code

You may ignore clearly unreasonable points, but you must address valid points. If it is pointed out that there is a discrepancy between user requirements and the implementation, you must address it; if addressing it proves difficult and you have to make a compromise, report this honestly to the user.

For each bug or vulnerability, if the sum of its likelihood and impact ratings is 6 or higher, you must address it. If the sum is 5 or lower, defer fixing it and report it to the user.

### 3. Review loop

After addressing valid feedback from the subagent, repeat steps 1 and 2 until there is no more valid feedback from the subagent. Always launch a new subagent to review your code each time.

### 4. Report the results to the user

Once the review loop is complete, report to the user whether you have fixed each issue pointed out in the review and whether you deemed it reasonable. For bugs and vulnerabilities, also include a rating of their occurrence and impact.
