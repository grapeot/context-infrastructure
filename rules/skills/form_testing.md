## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: Use Cursor's browser to fill and submit every form in the app with valid and invalid data, verifying validation, error states, and success flows.
- **上游来源**: [form-testing](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/form-testing)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# Form Testing

Systematically test every form in the app using Cursor's built-in browser.

## Workflow

### 1. Find All Forms

Use `browser_snapshot` to get the accessibility tree. Look for `form` elements, or groups of `input`, `select`, `textarea` elements.

Navigate through the app's main pages to discover all forms:
- Login / signup pages
- Settings / profile pages
- Search bars
- Contact / feedback forms
- Checkout flows
- Modals with inputs

### 2. Test Each Form

For each form, run three test passes:

**Pass 1: Empty submission**
- Submit the form with all fields empty
- Verify validation errors appear for required fields
- Check that no server error occurs (should be client-side validation)

**Pass 2: Invalid data**
- Email fields: enter `notanemail`
- Password fields: enter `a` (too short)
- Number fields: enter `abc`
- Phone fields: enter `12345`
- URL fields: enter `not-a-url`
- Check that appropriate error messages appear

**Pass 3: Valid data**
- Fill every field with realistic test data using `browser_fill` or `browser_fill_form`
- Submit the form
- Verify success state (redirect, toast, confirmation message)
- Check `browser_console_messages` for errors
- Check `browser_network_requests` for failed API calls

### 3. Check Edge Cases

- **Double submission**: Click submit twice quickly — should be prevented
- **Long input**: Paste a very long string (1000+ chars) — should be truncated or rejected
- **Special characters**: Enter `<script>alert('xss')</script>` — should be escaped
- **Tab order**: Use `browser_press` with Tab to verify focus moves logically through fields

### 4. Report

```
Form Test Results:
  Login form (/login):
    Empty submit: PASS — shows "Email required", "Password required"
    Invalid email: PASS — shows "Invalid email"
    Valid submit: PASS — redirects to /dashboard
    XSS check: PASS — input escaped

  Settings form (/settings):
    Empty submit: FAIL — submits without validation, returns 500
    Valid submit: PASS — shows "Settings saved" toast
```

Fix any failures found.
