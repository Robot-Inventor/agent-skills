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

When you write an object and need to guarantee that it conforms to a specific type, use `satisfies`. If the object will not change, also use `as const`. You don't need to use `as const` on temporary arrays used inline, or `satisfies` on values whose type is obvious, such as arrays of strings. Also, you don't need to specify `ReadOnly` for the type of an `as const satisfies` value.

```ts
// Incorrect
const foo: T = {
    bar: "bar"
};

const foo = {
    bar: "bar"
} as const satisfies ReadOnly<T>;

// Correct
const foo = {
    bar: "bar"
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

The `max-lines` and `max-lines-per-function` rules exist as indicators of code readability and maintainability. Warnings for these rules suggest that your code design may be poor. Simply removing line breaks to meet the rules is a superficial solution and actually makes the code harder to read, thus violating the essence of the rules. Instead, you should fix the problem by removing redundant code or properly restructuring and modularizing it. If you've only slightly exceeded the limit and your code is already well-designed, you should disable the rules rather than removing line breaks or forcing splits.

### Design code with types at its core

TypeScript types are not just an afterthought to JavaScript. Designing with types in mind keeps your code clean and efficient. With proper type design, validation is rarely needed except at project boundaries such as user input or web API responses. When code is properly designed based on types, function inputs and outputs are reliable, eliminating the need to validate values repeatedly.

## CSS

### Define only the necessary styles

When writing CSS, first check if a reset CSS is loaded into your project and if that reset CSS is applied to the page or layout file you are currently working on. If a reset CSS is in place, you do not need to define styles that overlap with it, such as `margin: 0` (this is an example, but not limited to this).

In CSS, you should only specify properties that need to be changed from the parent element, and you should not specify properties that do not need to be changed again. Remember that CSS has inheritance, and style accordingly.

### Intentional typography design

Do not specify `font-family` outside the document root unless absolutely necessary, such as in code blocks. Also, as a general rule, do not change the font size unless there is a clear reason, such as making unimportant notices smaller or headings larger. Since the base font size may be overridden by browser settings, use `em` or `rem` instead of `px` for font size or areas that depend on font size.

## HTML and JSX

### Avoid redundant definitions

If a UI component library is available, actively use its components and reduce custom implementations unless absolutely necessary.

Also, avoid adding unnecessary attributes. For example, icon component libraries may have `aria-hidden` set by default; in such cases, there's no need to set this attribute again when using the component.

## Testing

### Design tests properly

Do not mock application-owned modules. Prefer real implementations and test observable behavior rather than implementation wiring. Use mocks only at slow, nondeterministic, destructive, or external boundaries. Avoid tests whose assertions only verify mock calls or values configured on mocks.

Test the behavior from an external perspective, not the internal implementation. In other words, tests that require changes when refactoring are bad tests. Test the project's code, not the browser or external libraries. For example, it's obvious that a button element will be displayed in the browser when you write it; this tests the browser's behavior, not the project's code.

### Do not export for testing purposes

You should not export functions, values, or other data solely for testing purposes. When testing things that are not used outside of the file except for testing, use [in-source testing](https://vitest.dev/guide/in-source) instead of exporting them and creating a separate test file.

### Do not mock the external environment

For tests that require access to databases or external servers, use Testcontainers instead of mocking them. If a timer is needed, use the fake timer from the test library.
