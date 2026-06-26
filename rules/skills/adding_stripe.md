## 元数据

- **类型**: Workflow
- **分类**: Auth & Payments
- **适用场景**: Integrate Stripe payments into a web application, including checkout sessions, webhooks, and customer portal.
- **上游来源**: [adding-stripe](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/adding-stripe)
- **user-invocable**: —
- **导入日期**: 2026-06-26

---

# Add Stripe Payments

Use this skill when the user asks to add payments, billing, subscriptions, or Stripe integration.

## Steps

1. **Install the SDK**

   ```bash
   npm install stripe @stripe/stripe-js
   ```

2. **Add environment variables**

   ```
   STRIPE_SECRET_KEY=sk_test_...
   NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
   STRIPE_WEBHOOK_SECRET=whsec_...
   ```

3. **Create a Stripe client module** — create `lib/stripe.ts`:

   ```ts
   import Stripe from "stripe";

   export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
     apiVersion: "2024-12-18.acacia",
   });
   ```

4. **Create a checkout API route** — create an endpoint that creates a Stripe Checkout session:

   ```ts
   const session = await stripe.checkout.sessions.create({
     mode: "subscription", // or "payment" for one-time
     payment_method_types: ["card"],
     line_items: [{ price: priceId, quantity: 1 }],
     success_url: `${origin}/success?session_id={CHECKOUT_SESSION_ID}`,
     cancel_url: `${origin}/pricing`,
     customer_email: userEmail,
   });
   return redirect(session.url!);
   ```

5. **Create a webhook handler** — create a `POST` endpoint at `/api/webhooks/stripe`:

   - Verify the webhook signature using `stripe.webhooks.constructEvent`.
   - Handle key events: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`, `invoice.payment_failed`.
   - Update your database with the subscription status.

6. **Add customer portal (optional)** — create an endpoint that redirects to `stripe.billingPortal.sessions.create` so users can manage their subscription.

7. **Add pricing page UI** — create a pricing page with plan cards that call the checkout API route.

## Notes

- Always verify webhook signatures — never trust unverified payloads.
- Use Stripe CLI (`stripe listen --forward-to localhost:3000/api/webhooks/stripe`) for local webhook testing.
- Store the Stripe customer ID in your user database to avoid creating duplicate customers.
- Use `stripe.prices.list` to fetch prices dynamically instead of hardcoding them.
