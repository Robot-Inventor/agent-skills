# Review Instructions

Review the code for design issues, bugs, vulnerabilities, and oversights, and report the findings categorized as critical, high, medium, low, or informational. Evaluate and report bugs, oversights, and vulnerabilities by rating both their likelihood of occurrence and the magnitude of their impact when they occur on a scale of 1 to 5. Also, review whether the current implementation faithfully adheres to the user's requirements.

Read the global and project-specific `AGENTS.md` files, along with all relevant skills, and audit whether the code under review strictly adheres to their instructions. In addition to the aforementioned review output, also use the ponytail-review skill if available.

Also check for over-engineering, such as excessive implementation or unnecessary conditional branching, in accordance with simple-engineering skill. You should also consider whether there are simpler designs or alternative approaches to the overall logic of the changed parts, following the principles of simple-engineering. Identify the purpose of the changes from a broad perspective, such as what features are being added, and devise several design proposals to achieve that purpose. Next, compare them with the current code design, and if the proposed design is simpler and more elegant, suggest changing to that design.

Flag excessive validation, overly defensive implementation, and unnecessary complexity that does not serve the code's intended purpose. For example, a function that opens product links for a specific website may only need to verify the hostname. Checking the pathname may add complexity without improving security. You might remove validation by defining the function argument as a type such as `https://example.com/product/{string}`, or by accepting only a product ID and constructing the link inside the function. Ask what purpose the code serves and whether the implementation contains only what that purpose requires.

## Checklist

- Checked for bugs and vulnerabilities, and categorized them into critical, high, medium, low, and informational.
- Rated bugs and vulnerabilities on a scale of 1 to 5 for occurrence and impact.
- Identified the purpose of the code changes, considered multiple approaches to achieving that purpose, and compared them with the current implementation.
- Investigated whether there are any fundamental issues with the current implementation.
- Looked for opportunities to simplify the code.
- Checked for over-engineering.
