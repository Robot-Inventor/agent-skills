---
name: simple-engineering
description: Fundamental principles to keep in mind when writing or editing code. Read this skill before developing an implementation plan or writing or reviewing code,
license: MIT
metadata:
    author: Robot-Inventor
---

# Simple Engineering

## Keep it simple and elegant

Overengineering is a shameful and foolish act, and it is important to always pursue simple and elegant solutions.

Before implementing a feature or fixing a bug, consider all options. Instead of just listing similar choices or being bound by preconceptions and previous thinking, consider all options, including completely different approaches. Among the available options, choose the one that is the clearest, simplest, requires the fewest lines of code, and meets the user's requirements. There is no need to use iron plates and nails to repair torn clothes. Choose a right-sized, simple approach rather than an overly large and complex one.

Do not preemptively extract code into a separate function if it will only be used once. Unless the function is intended for reuse, serves to encapsulate complex logic, or has a clear, independent name that improves the readability of the calling code, keep the logic inlined at the call site.

Also avoid bringing unnecessary complexity into your code. Avoid introducing excessive validation, overly defensive implementations, unnecessary intermediate representations, or unnecessary complexity that does not serve the code's purpose. Check the type definitions and actual processing, and remove any impossible conditional branches. There is no need to wrap code in a new try-catch block if an exception is unlikely to occur normally or if a try-catch already exists inside the called function.

For example, a function that opens product links for a specific website may only need to verify the hostname. Checking the pathname may add complexity without improving security. You might remove validation by defining the function argument as a type such as `https://example.com/product/{string}`, or by accepting only a product ID and constructing the link inside the function. These are examples, but you should look for simpler implementations of the same kind. Ask what purpose the code serves and whether the implementation contains only what that purpose requires.

## Avoid reinventing the wheel

Avoid reinventing the wheel. Before adding code, check whether existing code or dependencies already provide functionality that covers part or all of that processing. Before writing code, investigate whether a popular and well-maintained library that achieves equivalent functionality exists, and if so, propose using it to the user.

## Keep only necessary changes

Keep the YAGNI (You aren't gonna need it) principle in mind. You should not introduce complexity just because you might need it in the future. Also, there is no need to maintain backward compatibility for unreleased features.

Every line of change is necessary and no unnecessary code remains. Carefully review the diff line by line, rather than file by file, to ensure that all changes are truly necessary.

## Keep the codebase clean

Remove code that is no longer needed. Avoid forcibly adding to existing code that is semantically different; maintain clean code by splitting code as needed and refactoring, including redesigning the code.

Refactoring should not be done only at special times; if there are poorly designed areas within the scope of the current changes that can be resolved with small-scale refactoring during normal work, refactoring should be proactively performed. However, explicit permission from the user should be sought before performing large-scale refactoring.

## DRY principle and modifiability

Keep the DRY principle and modifiability in mind. Avoid defining the same thing repeatedly; instead, aim for code that is easy to modify, where changing a single location automatically updates all related processes. For instance, regarding i18n, the ideal approach is to manage available languages and their labels in one place, such that adding or removing a language requires only updating that single location and adding or removing the corresponding translation file.
