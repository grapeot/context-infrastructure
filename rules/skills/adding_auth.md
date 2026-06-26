## 元数据

- **类型**: Workflow
- **分类**: Auth & Payments
- **适用场景**: Add authentication to a web application using NextAuth.js (Auth.js), including OAuth providers, session management, and protected routes.
- **上游来源**: [adding-auth](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/adding-auth)
- **user-invocable**: —
- **导入日期**: 2026-06-26

---

# Add Authentication (Auth.js)

Use this skill when the user asks to add authentication, login, sign-up, OAuth, or session management.

## Steps

1. **Install dependencies**

   ```bash
   npm install next-auth@beta
   ```

2. **Generate an auth secret**

   ```bash
   npx auth secret
   ```

   This adds `AUTH_SECRET` to `.env.local`.

3. **Create the auth config** — create `auth.ts` in the project root:

   ```ts
   import NextAuth from "next-auth";
   import GitHub from "next-auth/providers/github";
   import Google from "next-auth/providers/google";

   export const { handlers, signIn, signOut, auth } = NextAuth({
     providers: [GitHub, Google],
   });
   ```

4. **Add the route handler** — create `app/api/auth/[...nextauth]/route.ts`:

   ```ts
   import { handlers } from "@/auth";
   export const { GET, POST } = handlers;
   ```

5. **Add environment variables** for each provider:

   ```
   AUTH_SECRET=...
   AUTH_GITHUB_ID=...
   AUTH_GITHUB_SECRET=...
   AUTH_GOOGLE_ID=...
   AUTH_GOOGLE_SECRET=...
   ```

6. **Add sign-in/sign-out UI** — create components that call the `signIn` and `signOut` server actions, or use `<Link href="/api/auth/signin">`.

7. **Protect routes** — use the `auth()` function in server components or middleware:

   ```ts
   import { auth } from "@/auth";

   export default async function ProtectedPage() {
     const session = await auth();
     if (!session) redirect("/api/auth/signin");
     return <div>Welcome {session.user?.name}</div>;
   }
   ```

8. **Add database adapter (optional)** — if the user needs persistent sessions or user records, install a database adapter (e.g. `@auth/drizzle-adapter`, `@auth/prisma-adapter`) and configure it in the auth config.

## Notes

- Auth.js v5 works with Next.js App Router and Server Actions natively.
- For Pages Router, use `getServerSession` in `getServerSideProps` and `useSession` on the client.
- Add `NEXTAUTH_URL` for production deployments.
- Store minimal user data in the session; fetch full profiles from the database when needed.
