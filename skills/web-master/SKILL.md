---
name: web-master
description: A skill outlining the fundamental principles to keep in mind when writing or editing web-related code. Read this skill before developing an implementation plan or writing or reviewing code for web-related tasks, and apply it to your work.
license: MIT
metadata:
  author: Robot-Inventor
---

# Web Master

Follow these instructions when writing web-related code.

## TypeScript

### Do not use type assertions

Do not reach for type assertions unless you need one. Never add a type assertion up front because you think you might need it later. You may use a type assertion only when all of these conditions apply:

- You first write the code without a type assertion and encounter a type error.
- You cannot resolve that type error by improving type definitions elsewhere.
- Adding the type assertion does not compromise type safety.

### Do not use `ReturnType`

Do not use `ReturnType` unless you need it. Use the following approaches instead.

If you need to use the return type of a specific function defined in the project somewhere other than that function:

- For a simple primitive type such as `boolean` or `string`, write the type directly.
- For a complex type, define a named type, specify it as the function's return type (`(): T => {}`), and reuse `T`.

If you need the return type of a library function:

- Check the function's type definitions first.
- If the library exports that type, use the exported type.
  - If you need to pass the return type of another library function as a type argument and the library does not export that function's return type, you may use `ReturnType` inside the type argument.
- If the library does not export the type:
  - Write the type directly if it is a simple primitive type.
  - Otherwise, you may use `ReturnType`.

```ts
// Incorrect
import foo from "foo";

const myFunc = (): string => {...};

const myFunc2 = (arg: ReturnType<typeof foo>, arg2: ReturnType<typeof myFunc>): number => {...};

// Correct
import type { FooResult } from "foo";

const myFunc = (): string => {...};

const myFunc2 = (arg: FooResult, arg2: string): number => {...};
```

### Prefer `as const satisfies` over type annotations

Do not add type annotations unless you need them. Start by writing the code without a type annotation. If that causes a type error, first try to resolve it by improving type definitions elsewhere. Use a type annotation only as a last resort when those changes cannot solve the problem.

When you write an object and need to guarantee that it conforms to a specific type, use `satisfies`. If the object will not change, also use `as const`.

```ts
// Incorrect
const foo: Record<string, string> = {
  bar: "bar",
};

// Correct
const foo = {
  bar: "bar",
} as const satisfies T;
```

### Do not disable ESLint rules

Do not disable ESLint rules as an easy workaround. ESLint errors usually identify low-quality code rather than create pointless obstacles. Disabling a rule to silence an error leaves the underlying problem in place.

Disable an ESLint rule only as a last resort when no better option exists. Handle ESLint errors as follows:

1. Understand what ESLint is reporting. Identify the affected code and the purpose behind the rule.
2. Improve the code in a way that addresses that purpose.
3. Disable the rule only when complying with it would make the code **excessively** complex, the warning is a clear false positive, you have another legitimate reason to disable it, or a possible fix would conflict with the rule's underlying intent.

#### Examples

The ESLint `sort-imports` rule defines a consistent import order. In properly modularized code, behavior should not depend on import order, so you should follow the rule.

```ts
// Incorrect
/* eslint-disable sort-imports */
import foo from "foo";
import bar from "bar";

// Correct
import bar from "bar";
import foo from "foo";
```

The `no-magic-numbers` rule exists to give numeric values meaningful names when their purpose would otherwise be unclear. You do not need to force an obvious value, such as `60` when it represents the number of seconds in a minute, into a constant just to satisfy the rule. In that case, disabling the rule is acceptable. Replacing `1` with a constant named `ONE` also defeats the purpose of `no-magic-numbers`. Give the value a meaningful name instead, or disable the rule if its meaning is already obvious. Also consider whether the number needs to be hard-coded in the first place.

```ts
// Incorrect
// eslint-disable-next-line no-magic-numbers
if (myArray.length !== 0) {...}

// Correct
if (myArray.length) {...}
```
