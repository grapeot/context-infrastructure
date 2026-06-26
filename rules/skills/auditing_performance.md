## 元数据

- **类型**: Workflow
- **分类**: Code Quality & Security
- **适用场景**: Audit and optimize application performance, including bundle size, rendering, database queries, and Core Web Vitals.
- **上游来源**: [auditing-performance](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/auditing-performance)
- **user-invocable**: —
- **导入日期**: 2026-06-26

---

# Performance Audit

Use this skill when the user asks to optimize performance, reduce load times, fix slow pages, or audit Core Web Vitals.

## Steps

1. **Analyze bundle size**
   - Run `npx @next/bundle-analyzer` (Next.js) or `npx vite-bundle-visualizer` (Vite) to identify large dependencies.
   - Look for large libraries that could be replaced with lighter alternatives (e.g. `moment` → `date-fns`, `lodash` → individual imports or native methods).
   - Check for duplicated dependencies in the bundle.
   - Verify tree-shaking is working (no barrel file re-exports pulling in unused code).

2. **Audit rendering performance**
   - Identify components that re-render unnecessarily — look for inline object/array/function creation in JSX props.
   - Check for expensive computations in render paths that should use `useMemo`.
   - Verify lists use proper `key` props (not array index for dynamic lists).
   - Look for layout thrashing (reading DOM measurements then writing styles in a loop).

3. **Check data fetching**
   - Identify request waterfalls — sequential API calls that could be parallelized with `Promise.all`.
   - Look for data fetched on the client that could be fetched on the server.
   - Check for missing pagination on large data sets.
   - Verify API responses aren't over-fetching (returning fields the client doesn't need).

4. **Database query optimization**
   - Look for N+1 query patterns (a query per item in a list).
   - Check for missing indexes on columns used in WHERE, ORDER BY, and JOIN clauses.
   - Identify queries that could use `SELECT` with specific columns instead of `SELECT *`.
   - Look for missing connection pooling.

5. **Check assets**
   - Verify images use modern formats (WebP/AVIF) and are properly sized.
   - Check for missing `loading="lazy"` on below-the-fold images.
   - Verify fonts use `font-display: swap` and are preloaded.
   - Check for render-blocking CSS or JavaScript.

6. **Generate recommendations** — produce a prioritized list of optimizations ranked by impact (High / Medium / Low) with estimated effort for each.

## Notes

- Focus on measurable improvements — use Lighthouse, WebPageTest, or the Performance tab in DevTools.
- Don't prematurely optimize — profile first, optimize bottlenecks.
- For React apps, use React DevTools Profiler to identify slow components.
