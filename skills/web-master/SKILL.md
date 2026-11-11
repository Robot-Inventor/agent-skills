---
name: web-master
description: Fundamental principles to keep in mind when writing or editing web-related code. Read this skill before developing an implementation plan or writing or reviewing code for web-related tasks.
license: MIT
metadata:
    author: Robot-Inventor
---

# Web Master

## TypeScript

### Do not use type assertions

Do not reach for type assertions unless you need one. You may use a type assertion only when all of these conditions apply:

- You first write the code without a type assertion and encounter a type error.
- You cannot resolve that type error by improving type definitions elsewhere.
- Adding the type assertion does not compromise type safety.

### Do not use `ReturnType`

Do not use `ReturnType` unless you need it. If you need to use the return type of a specific function defined in the project:

- For a simple type such as `boolean` or `string`, write the type directly.
- For a complex type, define a named type, specify it as the function's return type (`(): T => {}`), and reuse `T`.

If you need the return type of a library function, first check the function's type definitions. Then,

- If the library exports that type, use it.
- If the library does not export the type:
    - Write the type directly if it is a simple primitive type.
    - Otherwise, you may use `ReturnType`.

```ts
// Bad
import foo from "foo";
const myFunc = (): string => {...};
const myFunc2 = (arg: ReturnType<typeof foo>, arg2: ReturnType<typeof myFunc>): number => {...};

// Good
import type { FooResult } from "foo";
const myFunc = (): string => {...};
const myFunc2 = (arg: FooResult, arg2: string): number => {...};
```

### Prefer `as const satisfies` over type annotations

Use a type annotation only as a last resort. Start by writing the code without a type annotation. If that causes a type error, first try to resolve it by improving type definitions elsewhere.

When you write an object and need to guarantee that it conforms to a specific type, use `satisfies`. You don't need to use `satisfies` on values whose type is obvious, such as arrays of strings. You don't need to specify `ReadOnly` for the type of an `as const satisfies` value.

```ts
// Bad
const foo: T = {
    bar: "bar"
};

const foo = {
    bar: "bar"
} as const satisfies ReadOnly<T>;

// Good
const foo = {
    bar: "bar"
} as const satisfies T;
```

### Do not disable linter rules

Do not disable linter rules as an easy workaround. Disable an linter rules only as a last resort when no better option exists. Handle linter errors as follows:

1. Understand what the rule is reporting. Identify the affected code and the purpose behind the rule.
2. Improve the code in a way that addresses that purpose.
3. Disable the rule only when complying with it would make the code **excessively** complex, the warning is a clear false positive, you have another legitimate reason to disable it, or a possible fix would conflict with the rule's underlying intent.

#### Examples

The `no-magic-numbers` rule exists to give numeric values meaningful names when their purpose would otherwise be unclear. You do not need to force an obvious value, such as `60` when it represents the number of seconds in a minute, into a constant just to satisfy the rule. In that case, disabling the rule is acceptable. Replacing `1` with a constant named `ONE` also defeats the purpose of `no-magic-numbers`. Give the value a meaningful name instead, or disable the rule if its meaning is already obvious. Also consider whether the number needs to be hard-coded in the first place.

```ts
// Bad
// eslint-disable-next-line no-magic-numbers
if (myArray.length !== 0) {...}

// Good
if (myArray.length) {...}
```

The `max-lines` and `max-lines-per-function` rules exist as indicators of code readability and maintainability. Warnings for these rules suggest that your code design may be poor. Simply removing line breaks to meet the rules is a superficial solution and actually makes the code harder to read, thus violating the essence of the rules. Instead, you should fix the problem by removing redundant code or properly restructuring and modularizing it. If you've only slightly exceeded the limit and your code is already well-designed, you should disable the rules rather than removing line breaks or forcing splits.

### Do not validate it yourself

TypeScript types are not just an afterthought to JavaScript. With proper type design, validation is rarely needed except at project boundaries such as user input or web API responses. When code is properly designed based on types, function inputs and outputs are reliable, eliminating the need to validate values repeatedly. If project's dependencies include a validation library, you should use it.

```ts
// Bad
const isRecord = (value: unknown): value is Record<string, unknown> =>
    typeof value === "object" && value !== null && !Array.isArray(value);
const isParson = (value: unknown): value is Person =>
    isRecord(value) && typeof value.name === "string" && typeof value.age === "number" && value.age >= 0;

isParson(externalValue) ? externalValue : "Unknown";

// Good
import { type } from "arktype";

const Person = type({
    name: "string",
    age: "number >= 0"
});

const parsed = Person(externalValue);
parsed instanceof type.errors ? "Unknown" : parsed;
```

## CSS

### Define only the necessary styles

When writing CSS, first check if a reset CSS is installed into your project and if the reset CSS is applied to the page. Don't define styles that overlap with the reset CSS, such as `margin: 0`.

You should only specify properties that need to be changed from the parent element, and you should not specify properties that do not need to be changed again. Remember that CSS has inheritance, and style accordingly.

```css
/* reset.css */
* {
    margin: 0;
}
```

```css
/* style.css */

/* Bad */
h1 {
    margin: 0;
    font-weight: bold;
}

h1 div {
    font-weight: bold;
}

/* Good */
h1 {
    font-weight: bold;
}
```

### Intentional typography design

Do not specify `font-family` outside the document root unless absolutely necessary, such as in code blocks. Don't change the font size unless there is a clear reason, such as making unimportant notices smaller or headings larger. Since the base font size may be overridden by browser settings, use `em` or `rem` instead of `px` for font size or areas that depend on font size.

```css
/* Bad */
h1 {
    font-size: 32px;
}

/* Good */
h1 {
    font-size: 2rem;
}
```

## HTML and JSX

### Avoid redundant definitions

If a UI component library is installed in the project, make the most of its components whenever possible, and avoid implementing your own unless absolutely necessary.

Refrain from adding unnecessary attributes. For example, icon component libraries may have `aria-hidden` set by default.

## Testing

### Design tests properly

Test the behavior from an external perspective, not the internal implementation. In other words, tests that require changes when refactoring are bad tests. Test the project's code, not the browser or external libraries. For example, it's obvious that a button element will be displayed in the browser when you write it; this tests the browser's behavior, not the project's code.

Add only the necessary tests. Ensure that your tests verify the correct operation of the code and are capable of detecting when the code breaks. Testing outcomes that are already expected to occur is pointless, and tests that fail to detect when the code is broken are worthless. Test the externally observable behavior of the code when provided with normal, boundary, and anomalous input values.

### Do not export for testing purposes

You should not export functions, values, or other data solely for testing purposes. When testing things that are not used outside of the file except for testing, use [in-source testing](https://vitest.dev/guide/in-source).

### Do not use mocks

Do not mock application-owned modules. Use mocks only at slow, nondeterministic, destructive, or external boundaries. Avoid tests whose assertions only verify mock calls or values configured on mocks. For tests that require access to databases or external servers, use Testcontainers instead of mocking them. If a timer is needed, use the fake timer from the test library.
