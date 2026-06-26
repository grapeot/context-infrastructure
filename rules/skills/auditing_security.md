## 元数据

- **类型**: Workflow
- **分类**: Code Quality & Security
- **适用场景**: Perform a systematic security audit of a codebase, checking for OWASP Top 10 vulnerabilities, secrets exposure, and insecure patterns.
- **上游来源**: [auditing-security](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/auditing-security)
- **user-invocable**: —
- **导入日期**: 2026-06-26

---

# Security Audit

Use this skill when the user asks to audit security, check for vulnerabilities, review code for security issues, or harden an application.

## Steps

1. **Scan for hardcoded secrets** — search for API keys, tokens, passwords, and connection strings in source files. Check for patterns like:
   - `password=`, `secret=`, `token=`, `api_key=`
   - Base64-encoded credentials
   - AWS keys (`AKIA...`), Stripe keys (`sk_live_...`), GitHub tokens (`ghp_...`)
   - Files: `.env` committed to git, `config.json` with credentials

2. **Check authentication & authorization**
   - Verify all API routes check authentication before processing.
   - Ensure role-based access control is enforced server-side, not just in the UI.
   - Check that password hashing uses bcrypt/argon2 (not MD5/SHA1).
   - Verify session tokens are HTTP-only, secure, and have reasonable expiry.

3. **Check for injection vulnerabilities**
   - **SQL injection**: look for string concatenation in SQL queries instead of parameterized queries.
   - **XSS**: look for `dangerouslySetInnerHTML`, `innerHTML`, or unescaped user input rendered in templates.
   - **Command injection**: look for `exec()`, `eval()`, `child_process.exec()` with user input.
   - **Path traversal**: check file operations for unsanitized user input in paths.

4. **Review dependency security**
   - Run `npm audit` or `pip audit` to check for known vulnerabilities.
   - Flag outdated dependencies with known CVEs.
   - Check for overly permissive dependency ranges.

5. **Check CORS and CSP configuration**
   - Verify CORS doesn't use `Access-Control-Allow-Origin: *` in production.
   - Check for Content Security Policy headers.
   - Verify `X-Frame-Options`, `X-Content-Type-Options`, and `Strict-Transport-Security` headers.

6. **Review data exposure**
   - Check API responses for leaking sensitive fields (password hashes, internal IDs, PII).
   - Verify error messages don't expose stack traces or internal details in production.
   - Check logging for sensitive data being written to logs.

7. **Generate report** — produce a summary with severity ratings (Critical / High / Medium / Low) for each finding, with the file path, line number, and recommended fix.

## Notes

- This is a code review, not a penetration test. Recommend tools like `npm audit`, `trivy`, or `snyk` for automated scanning.
- Always check `.gitignore` to ensure `.env`, credentials, and key files are excluded.
- For comprehensive auditing, recommend the OWASP Testing Guide.
