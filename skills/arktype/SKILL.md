---
name: ArkType
description: This skill explains how to use ArkType, a validation library for TypeScript. Read this skill when writing validation logic using ArkType.
license: MIT
metadata:
  author: Robot-Inventor
---

# ArkType

This skill explains how to use ArkType, a validation library for TypeScript. Read this skill when writing validation logic using ArkType. ArkType is a library that allows you to validate values ​​using a notation very similar to that of TypeScript type definitions.

## Installation

If ArkType is not yet present in the project's dependencies, you can install it with `npm install arktype`. If the project uses a package manager other than npm, use that instead.

## Basic usage

```ts
import { type } from "arktype";

const User = type({
    name: "string",
    platform: "'android' | 'ios'",
    email: "string.email",
    score: "number.integer <= 100",
    "versions?": "(number | string)[]",
    details: {
        // nested definitions don't need to be wrapped
        "['devices' | 'apps']": "string[]"
    },
    "areWeCoolYet": "boolean = true"
});

// extract the type if needed
type User = typeof User.infer;

const out = User(value);

if (out instanceof type.errors) {
    console.error(out.summary);
} else {
    console.log(`Hello, ${out.name}`);
}

// throws an error if the value is invalid.
const user = User.assert(value);

// `.allows()` is a type guard and does not apply morphs or transformations
if (User.allows(value)) {
    console.log("value is correct");
}
```

Note: Object types allow and preserve undeclared properties by default. Use `"+": "reject"` to reject them or `"+": "delete"` to strip them.

## Optional properties

Optional properties does not implicitly allow `undefined` as a value.

```ts
const User = type({
    // `name` may be absent
    "name?": "string",
    // `value` is required, but may be undefined
    value: "string | undefined",
    // `label` may be absent or explicitly undefined
    "label?": "string | undefined"
});
```

## Constraints

```ts
// you can add non-standard constraints with `.narrow()`
const Odd = type("number").narrow((n, ctx) =>
    n % 2 === 0 ? ctx.mustBe("odd") : true
);
```

## Builtin keywords

In ArkType, for example, you can represent a URL-formatted string with `type("string.url")`, and you can morph it into a URL object while performing validation using `type("string.url.parse")`.

For all built-in primitives and keywords, refer to the documentation: https://arktype.io/docs/keywords

## Regex

```ts
const User = type({
    birthday: "x/^(?<month>\\d{2})-(?<day>\\d{2})-(?<year>\\d{4})$/"
})

const data = User.assert({ birthday: "05-21-1993" })

// fully type-safe
data.birthday.groups.month // "05"
data.birthday.groups.day // "21"
data.birthday.groups.year // "1993"
```

If you don't need the full features of ArkType and only want to use type-safe regular expressions, you can use ArkRegex.

```ts
import { regex } from "arkregex";

// RegExp-compatible
const semver = regex("^(\\d+)\\.(\\d+)\\.(\\d+)$");
```

## Morphs & JSON

```ts
const morphed = type("string").pipe((s) => s.trim());

const parseJson = type("string.json.parse").to({
    version: "string.semver"
});

const out = parseJson('{ "version": "2.0.0" }');
```

## Recursive Types

```ts
import { scope } from "arktype"

const userScope = scope({
    User: {
        id: "string",
        friends: "User[]"
    },
    UsersById: {
        "[string]": "User | undefined"
    }
});

const userModule = userScope.export();
const out = userModule.User(value);
```

## Creating validators and types from variables

```ts
// `as const` is required
const allowedValues = ["foo", "bar", "baz"] as const;

const AllowedValue = type.enumerated(...allowedValues);

// "foo" | "bar" | "baz"
type AllowedValue = typeof AllowedValue.infer;
```
