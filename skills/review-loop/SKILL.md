---
name: review-loop
description: Thoroughly improve code quality by requesting a review from a sub-agent after completing tasks requiring code editing, before returning the conversation turn to the user. Use for any task that edits code or configuration. Read this skill before starting edits, and after completing the requested changes run an isolated sub-agent review loop before returning the final response.
license: MIT
metadata:
  author: Robot-Inventor
---

# Review Loop Skill

This skill involves thoroughly improving code quality by repeatedly requesting a review from a sub-agent after editing and improving the code based on the results. Humans typically improve code quality by creating a pull request after editing code and having it reviewed by a reviewer. Such reviews are important because they can identify problems that might be missed through self-review alone.

## When to apply

Apply this skill in the following situations:

- When you have performed a task that requires code editing, and
- After completing the task instructed by the user, and
- Before returning the conversation to the user

## Steps

The following is the core of this skill; please follow the specified steps.

### 1. Request a code review

Request a code review from the subagent.

If you have the option to choose whether to fork the context or launch the subagent in an isolated context when starting it, **always** launch it in an isolated context. When requesting a review from a sub-agent, be sure to provide them with an overview of the task requested by the user, and instruct them to thoroughly review the changes made to the current workspace.

Code reviews by sub-agents can take time. Please note that if you re-spawn a sub-agent currently undergoing a review simply because it has not yet responded, the review process will start over from scratch, resulting in even longer wait times. If the workspace contains a mix of changes made by you and by the user, please specify the files to be reviewed when submitting your review request.

### 2. Receive reviews and improve your code

Once you receive the review results from the sub-agent, consider whether each point is valid. You may ignore clearly unreasonable points, but you must address valid points and correct the code accordingly.

In particular, if you receive feedback on a part that doesn't strictly follow the user's instructions as a result of compromises, do not ignore it. Instead, correct it according to the review to align with the user's instructions as much as possible. If you absolutely cannot comply with the user's request, you may ignore the sub-agent's point about that part, but be sure to inform the user of the compromise you made when you return the conversation to them.

### 3. Review loop

After addressing valid feedback from the subagent, repeat steps 1 and 2 ("1. Request a code review" and "2. Receive reviews and improve your code") until there is no more valid feedback from the subagent, thoroughly improving your code quality. In this review loop, always have a new subagent review your code each time.

### 4. Report the results to the user

Once the review loop is complete, return the conversation to the user. Be sure to honestly report to the user any points where you had to compromise and did not strictly follow their instructions.
