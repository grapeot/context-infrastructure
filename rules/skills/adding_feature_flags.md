## 元数据

- **类型**: Workflow
- **分类**: Analytics & Tracking
- **适用场景**: Add feature flags to an application for gradual rollouts, A/B testing, and kill switches using PostHog, LaunchDarkly, or a simple local implementation.
- **上游来源**: [adding-feature-flags](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/adding-feature-flags)
- **user-invocable**: —
- **导入日期**: 2026-06-26

---

# Add Feature Flags

Use this skill when the user asks to add feature flags, feature toggles, gradual rollouts, or A/B testing.

## Option A: PostHog Feature Flags (Recommended)

1. **Install PostHog** if not already present:

   ```bash
   npm install posthog-js
   ```

2. **Use feature flags in code**:

   ```tsx
   import { useFeatureFlagEnabled } from "posthog-js/react";

   function MyComponent() {
     const showNewFeature = useFeatureFlagEnabled("new-checkout-flow");
     if (showNewFeature) return <NewCheckout />;
     return <OldCheckout />;
   }
   ```

3. **Server-side evaluation** — for server components or API routes:

   ```ts
   import { PostHog } from "posthog-node";

   const posthog = new PostHog(process.env.POSTHOG_API_KEY!);
   const isEnabled = await posthog.isFeatureEnabled("new-checkout-flow", userId);
   ```

4. **Create flags in the PostHog dashboard** — set up targeting rules based on user properties, percentage rollouts, or cohorts.

## Option B: Simple Local Feature Flags

For projects that don't need a third-party service:

1. **Create a flags config** — `lib/feature-flags.ts`:

   ```ts
   export const FLAGS = {
     NEW_CHECKOUT: process.env.NEXT_PUBLIC_FF_NEW_CHECKOUT === "true",
     DARK_MODE: process.env.NEXT_PUBLIC_FF_DARK_MODE === "true",
   } as const;
   ```

2. **Use in components**:

   ```tsx
   import { FLAGS } from "@/lib/feature-flags";

   function App() {
     return FLAGS.NEW_CHECKOUT ? <NewCheckout /> : <OldCheckout />;
   }
   ```

3. **Add env vars** — add flags to `.env` and `.env.example`:

   ```
   NEXT_PUBLIC_FF_NEW_CHECKOUT=false
   NEXT_PUBLIC_FF_DARK_MODE=true
   ```

## Notes

- Use feature flags for all user-facing changes during rollout, not just experiments.
- Clean up stale flags — remove the flag and the old code path once a feature is fully rolled out.
- For server-side flags, cache the evaluation result to avoid per-request API calls.
- Name flags descriptively: `new-checkout-flow` not `flag-1`.
