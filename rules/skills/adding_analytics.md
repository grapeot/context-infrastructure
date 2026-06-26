## 元数据

- **类型**: Workflow
- **分类**: Analytics & Tracking
- **适用场景**: Add PostHog analytics to a web application, including event tracking, page views, feature flags, and session replay.
- **上游来源**: [adding-analytics](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/adding-analytics)
- **user-invocable**: —
- **导入日期**: 2026-06-26

---

# Add Analytics (PostHog)

Use this skill when the user asks to add analytics, event tracking, page views, feature flags, or session replay to a web application.

## Steps

1. **Detect the framework** — check for `next.config.*`, `vite.config.*`, `package.json` scripts, or `index.html` to determine if this is Next.js, React (Vite/CRA), Vue, Svelte, or plain HTML.

2. **Install the SDK**

   - Next.js / React: `npm install posthog-js`
   - Next.js (server-side): `npm install posthog-js posthog-node`
   - Python: `pip install posthog`
   - Node.js backend: `npm install posthog-node`

3. **Create a provider / init module**

   - For Next.js App Router, create `app/providers.tsx`:

     ```tsx
     "use client";
     import posthog from "posthog-js";
     import { PostHogProvider as PHProvider } from "posthog-js/react";
     import { useEffect } from "react";

     export function PostHogProvider({ children }: { children: React.ReactNode }) {
       useEffect(() => {
         posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY!, {
           api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST ?? "https://us.i.posthog.com",
           capture_pageview: false, // we capture manually for SPAs
         });
       }, []);
       return <PHProvider client={posthog}>{children}</PHProvider>;
     }
     ```

   - Wrap `{children}` in the root layout with `<PostHogProvider>`.

   - For Pages Router, init in `_app.tsx` inside a `useEffect`.

4. **Add page-view tracking** — for SPAs, create a component that calls `posthog.capture('$pageview')` on route change using the framework's router events.

5. **Add `.env` variables** — prompt the user for their PostHog project API key and host:

   ```
   NEXT_PUBLIC_POSTHOG_KEY=phc_...
   NEXT_PUBLIC_POSTHOG_HOST=https://us.i.posthog.com
   ```

   Add these keys to `.env.example` as well.

6. **Add custom events** — if the user specifies events to track (e.g. sign-up, purchase), add `posthog.capture("event_name", { ...properties })` calls in the relevant handlers.

7. **Feature flags (optional)** — if requested, show how to use `posthog.isFeatureEnabled("flag-name")` or the `useFeatureFlagEnabled` hook.

8. **Session replay (optional)** — enable by adding `session_recording: { maskAllInputs: false }` to the init config if requested.

## Notes

- Never hardcode API keys — always use environment variables.
- Add `posthog-js` to the Content Security Policy if the project has one.
- For monorepos, install in the package that renders the UI, not the root.
