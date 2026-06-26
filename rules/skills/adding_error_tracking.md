## 元数据

- **类型**: Workflow
- **分类**: Error Tracking
- **适用场景**: Add Sentry error tracking, performance monitoring, and source maps to a web application.
- **上游来源**: [adding-error-tracking](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/adding-error-tracking)
- **user-invocable**: —
- **导入日期**: 2026-06-26

---

# Add Error Tracking (Sentry)

Use this skill when the user asks to add error tracking, crash reporting, exception monitoring, or performance tracing.

## Steps

1. **Detect the framework** — check `package.json`, config files, and directory structure to determine the stack (Next.js, React, Node.js, Python/Django/Flask, etc.).

2. **Install the SDK**

   - Next.js: `npx @sentry/wizard@latest -i nextjs`
   - React (Vite): `npm install @sentry/react`
   - Node.js: `npm install @sentry/node`
   - Python: `pip install sentry-sdk`

3. **Initialize Sentry**

   - For Next.js, the wizard creates `sentry.client.config.ts`, `sentry.server.config.ts`, and `sentry.edge.config.ts`. Verify they exist and contain the DSN.

   - For React (Vite), init in `main.tsx`:

     ```tsx
     import * as Sentry from "@sentry/react";

     Sentry.init({
       dsn: import.meta.env.VITE_SENTRY_DSN,
       integrations: [Sentry.browserTracingIntegration()],
       tracesSampleRate: 1.0,
     });
     ```

   - For Node.js, init at the very top of the entry file before any other imports.

4. **Add environment variables**

   ```
   NEXT_PUBLIC_SENTRY_DSN=https://...@sentry.io/...
   SENTRY_AUTH_TOKEN=sntrys_...
   SENTRY_ORG=your-org
   SENTRY_PROJECT=your-project
   ```

5. **Add error boundary** — wrap the app (or critical subtrees) with `Sentry.ErrorBoundary` and a fallback UI.

6. **Source maps** — for production builds, configure the Sentry webpack/vite plugin to upload source maps. For Next.js, this is handled by `withSentryConfig` in `next.config.js`.

7. **Test the integration** — add a temporary button that throws an error to verify events appear in the Sentry dashboard.

## Notes

- Set `tracesSampleRate` to a lower value (e.g. `0.1`) in production to control costs.
- Add `sentry.properties` and `.sentryclirc` to `.gitignore`.
- Never commit `SENTRY_AUTH_TOKEN`.
