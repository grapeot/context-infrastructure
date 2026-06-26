## 元数据

- **类型**: Workflow
- **分类**: Testing
- **适用场景**: Analyze existing code and write comprehensive unit and integration tests for it. Detects the test framework, identifies untested code paths, and generates tests with proper mocking, edge cases, and assertions. Use when the user asks to add tests, improve coverage, or test a specific module.
- **上游来源**: [writing-tests](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/writing-tests)
- **user-invocable**: —
- **导入日期**: 2026-06-26

---

# Writing Tests

Use this skill when the user asks to add tests to existing code, improve test coverage, or write tests for a specific file or module.

## Steps

1. **Detect the test setup** — check what's already configured:

   ```bash
   # Check package.json for test runner
   cat package.json | grep -E "jest|vitest|mocha|playwright|cypress"
   ```

   Look for config files: `vitest.config.ts`, `jest.config.ts`, `playwright.config.ts`, `.mocharc.*`. Check for existing test files to understand the project's test patterns and conventions.

2. **If no test runner exists** — set one up:

   ```bash
   npm install -D vitest @testing-library/react @testing-library/jest-dom
   ```

   Add a `test` script to `package.json`:

   ```json
   { "test": "vitest run", "test:watch": "vitest" }
   ```

3. **Analyze the target code** — read the file(s) to test and identify:
   - **Public API**: exported functions, classes, components, hooks
   - **Code paths**: conditionals, error handling, edge cases
   - **Dependencies**: external services, databases, APIs that need mocking
   - **Side effects**: file I/O, network calls, DOM mutations

4. **Create the test file** — place it next to the source file or in a `__tests__/` directory, matching the project's convention:

   - `src/utils/format.ts` → `src/utils/format.test.ts`
   - `src/components/Button.tsx` → `src/components/Button.test.tsx`

5. **Write tests following this structure**:

   ```ts
   import { describe, it, expect, vi } from "vitest";

   describe("functionName", () => {
     // Happy path
     it("returns formatted output for valid input", () => { ... });

     // Edge cases
     it("handles empty string", () => { ... });
     it("handles null/undefined input", () => { ... });

     // Error cases
     it("throws on invalid argument", () => { ... });

     // Boundary conditions
     it("handles maximum length input", () => { ... });
   });
   ```

6. **Mock external dependencies** — don't make real API calls or database queries in unit tests:

   ```ts
   vi.mock("@/lib/db", () => ({
     query: vi.fn().mockResolvedValue([{ id: 1, name: "test" }]),
   }));
   ```

   For React components, mock hooks that fetch data:

   ```ts
   vi.mock("@/hooks/useUser", () => ({
     useUser: () => ({ user: { name: "Test" }, isLoading: false }),
   }));
   ```

7. **Test React components** with Testing Library:

   ```tsx
   import { render, screen, fireEvent } from "@testing-library/react";

   it("renders the button and handles click", () => {
     const onClick = vi.fn();
     render(<Button onClick={onClick}>Click me</Button>);
     fireEvent.click(screen.getByRole("button", { name: "Click me" }));
     expect(onClick).toHaveBeenCalledOnce();
   });
   ```

8. **Run the tests** and verify they pass:

   ```bash
   npm test
   ```

   If any fail, fix the test or the code (depending on whether the test expectation or the implementation is wrong).

## What to Test

- **Always test**: public API, error handling, edge cases (empty, null, zero, negative), state transitions, async behavior
- **Skip testing**: private implementation details, third-party library internals, simple getters/setters, type-only code

## Notes

- Match the project's existing test style — if they use `test()` instead of `it()`, follow that.
- Don't test implementation details — test behavior and outputs, not internal method calls.
- Use descriptive test names that explain the scenario: "returns 0 when cart is empty" not "test1".
- One assertion concept per test — multiple `expect` calls are fine if they verify the same behavior.
- For async code, always `await` the result or use `resolves`/`rejects` matchers.
