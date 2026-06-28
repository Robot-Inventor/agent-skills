---
name: cleanup-changes
description: The skill to revert unnecessary changes and leave only essential changes when a user requests a cleanup of changes, or before committing and creating a pull request.
license: MIT
metadata:
  author: Robot-Inventor
---

# Cleanup Changes Skill

Both humans and agents typically go through a trial-and-error process when writing code, making numerous changes (including non-essential and unnecessary ones) to achieve their final goals. However, non-essential and unnecessary changes resulting from this trial-and-error process should not be included in the final code. Changes should be reviewed as needed, and unnecessary changes should be reversed to focus only on essential ones.

## When to apply

You should perform this skill when a user requests a cleanup of changes, or before creating a commit or pull request.

## Steps

The following is the core of this skill; please follow the specified steps. Do not change the Git staging state unless explicitly instructed to do so by the user. Users may have staged their changes as a snapshot of the code in its last expected state.

### 1. Looking back on the trial-and-error process

Reflect on the trial-and-error process of the task and distinguish between changes that were essentially necessary and changes that, despite being tried, ultimately proved ineffective and unnecessary.

You shouldn't make assumptions about whether a change is essentially necessary. For example, when fixing a bug, review the changes made when the bug was finally fixed, understand the essential and root cause of the bug, and then, based on that, determine whether each change is essentially necessary.

When determining whether each change is necessary, pay particular attention to bugs caused by multiple factors. Bugs can be caused by a single, simple cause, or by multiple factors. If it's caused by a single, simple cause, the last change made when the bug is fixed may be sufficient, and previous changes may be unnecessary. If it's a bug caused by multiple factors, the last change alone may not be enough, and some of the changes made during the trial-and-error process leading up to it may also be necessary. Carefully consider the underlying cause of the bug, including whether it's due to a single cause or multiple factors, and then determine which changes are necessary and which are not.

### 2. Undo unnecessary changes

Revert any changes you determined were unnecessary in the previous step, leaving only the essential changes.

However, even if a change isn't strictly necessary, minor corrections to typos around the current change or small refactorings are acceptable. Generally, in coding, correcting typos found around a change or making small refactorings related to the current change are generally tolerated, even if they aren't strictly necessary.
