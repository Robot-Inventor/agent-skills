---
name: simple-engineering
description: A skill outlining the fundamental principles to keep in mind when writing or editing code. Read this skill before developing an implementation plan or writing or reviewing code, and apply it to your work.
license: MIT
metadata:
  author: Robot-Inventor
---

# Simple Engineering

## Keep it simple and elegant

Overengineering is a shameful and foolish act, and it is important to always pursue simple and elegant solutions.

Before implementing a feature or fixing a bug, consider all options. Instead of just listing similar choices or being bound by preconceptions and previous thinking, consider all options, including completely different approaches. Among the available options, choose the one that is the clearest, simplest, requires the fewest lines of code, and meets the user's requirements. There is no need to use iron plates and nails to repair torn clothes. Choose a right-sized, simple approach rather than an overly large and complex one.

## Avoid reinventing the wheel

Reinventing the wheel should be avoided. Before adding code, check whether existing code in the project or the project's dependencies already provide functionality that covers part or all of that processing. When implementing complex processing, investigate whether a popular and well-maintained library that achieves equivalent functionality exists, and if so, propose using it to the user.

## Keep only necessary changes

Keep the YAGNI (You aren't gonna need it) principle in mind. You should not introduce complexity just because you might need it in the future. Also, there is no need to maintain backward compatibility for unreleased features.

The code ultimately delivered to the user should be such that every line of change is necessary and no unnecessary code remains. Carefully review the diff line by line, rather than file by file, to ensure that all changes are truly necessary.
