# Stripe Integration Guide: Peptide Checker

**Version:** 1.0
**Date:** 2026-03-24
**Author:** Reuben Bowlby / HUMMBL
**Classification:** Technical Integration Guide
**Based on:** PEPTIDE_CHECKER_TECHNICAL_SPEC.md, PEPTIDE_CHECKER_BUSINESS_PLAN.md

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Stripe Billing for SaaS Subscriptions](#2-stripe-billing-for-saas-subscriptions)
3. [Product and Price Configuration](#3-product-and-price-configuration)
4. [Next.js + Stripe Integration](#4-nextjs--stripe-integration)
5. [Checkout Flow](#5-checkout-flow)
6. [Webhook Handler](#6-webhook-handler)
7. [Customer Portal](#7-customer-portal)
8. [Freemium Model Implementation](#8-freemium-model-implementation)
9. [Pricing Page](#9-pricing-page)
10. [Revenue Tracking and Analytics](#10-revenue-tracking-and-analytics)
11. [Tax Handling](#11-tax-handling)
12. [Testing and Launch](#12-testing-and-launch)
13. [Code Scaffolding](#13-code-scaffolding)
14. [Implementation Checklist](#14-implementation-checklist)

---

## 1. Architecture Overview

### Where Stripe Fits in the Stack

From the technical spec, Peptide Checker uses:

- **Frontend:** Next.js 14 (App Router) + Tailwind CSS on Vercel
- **Backend:** Python FastAPI on Railway
- **Database:** SQLite (Turso) -- user table already has `stripe_customer_id` and `tier` columns
- **Auth:** NextAuth.js v5 with email magic links
- **Payments:** Stripe (this guide)

Stripe integration lives primarily in the Next.js frontend layer. The FastAPI backend reads subscription status from the `users` table (synced via webhooks) to enforce rate limits and feature gates.

```
Browser
  │
  ├── Pricing Page ──→ Stripe Checkout (hosted) ──→ Success/Cancel URLs
  │
  ├── Account Page ──→ Stripe Customer Portal (hosted) ──→ Return URL
  │
  └── App Pages ──→ Next.js middleware (checks tier) ──→ Gate premium features
                        │
                        └── Reads from: users.tier (synced by webhooks)

Stripe ──webhook──→ Next.js /api/webhooks/stripe (route.ts)
                        │
                        └── Updates: users.tier, users.stripe_customer_id
                              via FastAPI or direct DB call
```

### Why Stripe Checkout (Not Custom Forms) for MVP

For an MVP SaaS product, Stripe Checkout is the correct choice over Stripe Elements (custom payment forms):

| Factor | Stripe Checkout | Stripe Elements |
|--------|----------------|-----------------|
| Development time | Hours | Days |
| PCI compliance | SAQ A (simplest tier) | SAQ A-EP (more complex) |
| Mobile responsive | Automatic | Must build |
| Localization | 40+ languages | Must build |
| Payment methods | Auto-shows relevant (cards, Apple Pay, Google Pay) | Must configure each |
| Conversion optimization | Stripe A/B tests continuously | You are on your own |
| 3D Secure / SCA | Handled automatically | Must implement flow |

Stripe Checkout redirects to a Stripe-hosted payment page. It handles all the hard parts (card validation, 3DS authentication, error handling, localization) and returns the user to your success URL. Build a custom form only when you need deeply embedded checkout UX that Checkout cannot support -- which is not the case for Peptide Checker.

---

## 2. Stripe Billing for SaaS Subscriptions

### How Stripe Billing Works

Stripe Billing manages the full subscription lifecycle:

1. **Products** represent what you sell (Peptide Checker Premium, Peptide Checker Pro)
2. **Prices** define how much and how often (e.g., $9.99/month, $99/year)
3. **Customers** are your users, linked by `stripe_customer_id` in your database
4. **Subscriptions** are active billing relationships between a Customer and one or more Prices
5. **Invoices** are generated automatically each billing period
6. **Payment Intents** handle the actual charge

### Subscription Lifecycle

```
User clicks "Subscribe"
    │
    ▼
Create Checkout Session (mode: 'subscription')
    │
    ▼
User completes payment on Stripe-hosted page
    │
    ▼
Stripe creates: Customer + Subscription + first Invoice
    │
    ▼
Webhook: checkout.session.completed
    │
    ▼
Your app: save stripe_customer_id, set tier = 'premium'
    │
    ▼
Monthly: Stripe auto-charges, sends invoice.paid webhook
    │
    ▼
If payment fails: invoice.payment_failed webhook → grace period → dunning emails
    │
    ▼
If canceled: customer.subscription.deleted webhook → set tier = 'free'
```

### Stripe Billing Pricing

Stripe Billing charges 0.5% on recurring charges on top of the standard Stripe processing fee (2.9% + $0.30 per successful card charge). For a $9.99/month subscription:

- Stripe processing: $0.29 + $0.30 = $0.59
- Stripe Billing: $0.05
- **Total Stripe fees: $0.64 per charge**
- **Net revenue per subscriber: $9.35/month**

At $19.99/month (Pro tier): net ~$18.77/month after fees.

---

## 3. Product and Price Configuration

### Tier Structure from the Business Plan

The business plan defines two paid tiers:

| Tier | Price | Features |
|------|-------|----------|
| **Free** | $0 | Public vendor database, basic search, regulatory tracker, storage calculator (30 req/min, 500/day) |
| **Premium** | $9.99/month | Alerts, unlimited COA scans, detailed vendor reports, priority rate limits (300 req/min, 20K/day) |
| **Pro** | $19.99/month | Everything in Premium + B2B API access, bulk data export, HPLC chromatogram analysis (Phase 4) |

### Creating Products and Prices in Stripe

Products and Prices can be created via the Stripe Dashboard (recommended for initial setup) or the API.

**Dashboard approach (recommended for MVP):**

1. Go to Stripe Dashboard > Products
2. Click "+ Add product"
3. Create "Peptide Checker Premium"
   - Set recurring price: $9.99 / month
   - Optionally add annual price: $99.00 / year (save ~17%)
4. Create "Peptide Checker Pro"
   - Set recurring price: $19.99 / month
   - Optionally add annual price: $199.00 / year (save ~17%)

**API approach (for reproducibility):**

```typescript
// scripts/create-stripe-products.ts
// Run once to set up products. Save the price IDs in .env.

import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

async function createProducts() {
  // Premium tier
  const premium = await stripe.products.create({
    name: 'Peptide Checker Premium',
    description: 'Alerts, unlimited COA scans, detailed vendor reports',
    metadata: { tier: 'premium' },
  });

  const premiumMonthly = await stripe.prices.create({
    product: premium.id,
    unit_amount: 999, // $9.99 in cents
    currency: 'usd',
    recurring: { interval: 'month' },
    metadata: { tier: 'premium' },
  });

  const premiumAnnual = await stripe.prices.create({
    product: premium.id,
    unit_amount: 9900, // $99.00 in cents
    currency: 'usd',
    recurring: { interval: 'year' },
    metadata: { tier: 'premium' },
  });

  // Pro tier
  const pro = await stripe.products.create({
    name: 'Peptide Checker Pro',
    description: 'API access, bulk export, advanced analytics',
    metadata: { tier: 'pro' },
  });

  const proMonthly = await stripe.prices.create({
    product: pro.id,
    unit_amount: 1999, // $19.99 in cents
    currency: 'usd',
    recurring: { interval: 'month' },
    metadata: { tier: 'pro' },
  });

  const proAnnual = await stripe.prices.create({
    product: pro.id,
    unit_amount: 19900, // $199.00 in cents
    currency: 'usd',
    recurring: { interval: 'year' },
    metadata: { tier: 'pro' },
  });

  console.log('Premium Monthly Price ID:', premiumMonthly.id);
  console.log('Premium Annual Price ID:', premiumAnnual.id);
  console.log('Pro Monthly Price ID:', proMonthly.id);
  console.log('Pro Annual Price ID:', proAnnual.id);
  // Save these IDs in your .env file
}

createProducts();
```

### Price IDs

After creation, store the price IDs in environment variables:

```
STRIPE_PRICE_PREMIUM_MONTHLY=price_xxxxxxxxxxxxx
STRIPE_PRICE_PREMIUM_ANNUAL=price_xxxxxxxxxxxxx
STRIPE_PRICE_PRO_MONTHLY=price_xxxxxxxxxxxxx
STRIPE_PRICE_PRO_ANNUAL=price_xxxxxxxxxxxxx
```

These IDs are safe to expose client-side (they are not secrets). They are used when creating Checkout Sessions to specify which plan the user selected.

---

## 4. Next.js + Stripe Integration

### Package Installation

```bash
npm install stripe @stripe/stripe-js @stripe/react-stripe-js
```

| Package | Purpose | Side |
|---------|---------|------|
| `stripe` | Node.js SDK for server-side API calls | Server only |
| `@stripe/stripe-js` | Loads Stripe.js in the browser | Client only |
| `@stripe/react-stripe-js` | React components (Elements, EmbeddedCheckout) | Client only |

### Server-Side Stripe Client

```typescript
// lib/stripe.ts
import Stripe from 'stripe';

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2025-12-18.acacia', // pin to a specific API version
  typescript: true,
});
```

This file is imported only in Server Components, Server Actions, and API routes. Never import it in Client Components.

### Client-Side Stripe

```typescript
// lib/stripe-client.ts
'use client';

import { loadStripe } from '@stripe/stripe-js';

export const stripePromise = loadStripe(
  process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!
);
```

### Environment Variables

```env
# .env.local (NEVER commit this file)

# Server-side only (no NEXT_PUBLIC_ prefix)
STRIPE_SECRET_KEY=<your-stripe-secret-key>
STRIPE_WEBHOOK_SECRET=<your-webhook-signing-secret>

# Client-side safe (NEXT_PUBLIC_ prefix)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxxxxxxxxxxxx

# Price IDs (safe to expose, but keep server-side for flexibility)
STRIPE_PRICE_PREMIUM_MONTHLY=price_xxxxxxxxxxxxx
STRIPE_PRICE_PREMIUM_ANNUAL=price_xxxxxxxxxxxxx
STRIPE_PRICE_PRO_MONTHLY=price_xxxxxxxxxxxxx
STRIPE_PRICE_PRO_ANNUAL=price_xxxxxxxxxxxxx
```

**Security rules:**
- `STRIPE_SECRET_KEY` must never appear in client bundles. No `NEXT_PUBLIC_` prefix.
- `STRIPE_WEBHOOK_SECRET` is server-only.
- The publishable key is designed to be public; it goes in `NEXT_PUBLIC_` so it is available in the browser.
- Never trust prices sent from the client. Always look up the Price ID server-side.

---

## 5. Checkout Flow

### Server Action to Create a Checkout Session

Using Next.js Server Actions (the modern pattern, replacing API routes for this use case):

```typescript
// app/actions/stripe.ts
'use server';

import { stripe } from '@/lib/stripe';
import { auth } from '@/lib/auth'; // NextAuth.js
import { redirect } from 'next/navigation';

export async function createCheckoutSession(priceId: string) {
  const session = await auth();

  if (!session?.user?.email) {
    redirect('/login?callbackUrl=/pricing');
  }

  // Look up or create the Stripe customer
  let customerId: string | undefined;

  // Check if user already has a Stripe customer ID in your database
  const user = await getUserByEmail(session.user.email);
  if (user?.stripe_customer_id) {
    customerId = user.stripe_customer_id;
  } else {
    const customer = await stripe.customers.create({
      email: session.user.email,
      metadata: { userId: user.id.toString() },
    });
    customerId = customer.id;
    await updateUserStripeCustomerId(user.id, customer.id);
  }

  const checkoutSession = await stripe.checkout.sessions.create({
    customer: customerId,
    line_items: [{ price: priceId, quantity: 1 }],
    mode: 'subscription',
    success_url: `${process.env.NEXT_PUBLIC_APP_URL}/account?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/pricing`,
    subscription_data: {
      metadata: { userId: user.id.toString() },
    },
    allow_promotion_codes: true, // enable discount codes
  });

  if (checkoutSession.url) {
    redirect(checkoutSession.url);
  }
}
```

### Pricing Page Button Component

```typescript
// components/checkout-button.tsx
'use client';

import { createCheckoutSession } from '@/app/actions/stripe';

export function CheckoutButton({
  priceId,
  label,
}: {
  priceId: string;
  label: string;
}) {
  return (
    <form action={() => createCheckoutSession(priceId)}>
      <button
        type="submit"
        className="bg-blue-600 text-white px-6 py-3 rounded-lg
                   hover:bg-blue-700 transition font-medium"
      >
        {label}
      </button>
    </form>
  );
}
```

### Success Page

After successful payment, Stripe redirects to your `success_url`. Use the `session_id` query parameter to display confirmation:

```typescript
// app/account/page.tsx
import { stripe } from '@/lib/stripe';

export default async function AccountPage({
  searchParams,
}: {
  searchParams: { session_id?: string };
}) {
  if (searchParams.session_id) {
    const session = await stripe.checkout.sessions.retrieve(
      searchParams.session_id
    );
    // Display: "Thanks for subscribing! Your plan is now active."
  }

  // ... render account page with subscription status
}
```

---

## 6. Webhook Handler

Webhooks are how Stripe tells your app about events that happen asynchronously (payments succeeding, failing, subscriptions being canceled). This is the most critical piece of the integration.

### Which Events to Listen For

| Event | When It Fires | Your Action |
|-------|---------------|-------------|
| `checkout.session.completed` | User completes Checkout | Save `stripe_customer_id`, set tier |
| `invoice.paid` | Recurring payment succeeds | Confirm subscription is active, log payment |
| `invoice.payment_failed` | Recurring payment fails | Notify user, start grace period |
| `customer.subscription.updated` | Plan change, renewal, trial end | Update tier if plan changed |
| `customer.subscription.deleted` | Subscription canceled (end of period) | Set tier = 'free' |
| `customer.subscription.paused` | Subscription paused | Set tier = 'free' temporarily |

### Webhook Handler Code

```typescript
// app/api/webhooks/stripe/route.ts
import { Stripe } from 'stripe';
import { NextResponse } from 'next/server';
import { headers } from 'next/headers';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

// Disable Next.js body parsing -- Stripe needs the raw body for signature verification
export const runtime = 'nodejs';

export async function POST(req: Request) {
  let event: Stripe.Event;

  try {
    const body = await req.text(); // raw body, NOT .json()
    const signature = (await headers()).get('stripe-signature') as string;

    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    console.error(`Webhook signature verification failed: ${message}`);
    return NextResponse.json(
      { error: `Webhook Error: ${message}` },
      { status: 400 }
    );
  }

  try {
    switch (event.type) {
      case 'checkout.session.completed': {
        const session = event.data.object as Stripe.Checkout.Session;
        await handleCheckoutCompleted(session);
        break;
      }

      case 'invoice.paid': {
        const invoice = event.data.object as Stripe.Invoice;
        await handleInvoicePaid(invoice);
        break;
      }

      case 'invoice.payment_failed': {
        const invoice = event.data.object as Stripe.Invoice;
        await handlePaymentFailed(invoice);
        break;
      }

      case 'customer.subscription.updated': {
        const subscription = event.data.object as Stripe.Subscription;
        await handleSubscriptionUpdated(subscription);
        break;
      }

      case 'customer.subscription.deleted': {
        const subscription = event.data.object as Stripe.Subscription;
        await handleSubscriptionDeleted(subscription);
        break;
      }

      default:
        console.log(`Unhandled event type: ${event.type}`);
    }
  } catch (error) {
    console.error(`Error handling ${event.type}:`, error);
    return NextResponse.json(
      { error: 'Webhook handler failed' },
      { status: 500 }
    );
  }

  return NextResponse.json({ received: true }, { status: 200 });
}

// --- Handler Functions ---

async function handleCheckoutCompleted(session: Stripe.Checkout.Session) {
  const userId = session.metadata?.userId;
  const customerId = session.customer as string;
  const subscriptionId = session.subscription as string;

  // Retrieve the subscription to get the price/product info
  const subscription = await stripe.subscriptions.retrieve(subscriptionId);
  const priceId = subscription.items.data[0].price.id;
  const tier = getTierFromPriceId(priceId);

  // Update your database
  await updateUser(userId, {
    stripe_customer_id: customerId,
    stripe_subscription_id: subscriptionId,
    tier: tier,
  });
}

async function handleInvoicePaid(invoice: Stripe.Invoice) {
  // Recurring payment succeeded -- subscription remains active
  const customerId = invoice.customer as string;
  console.log(`Payment succeeded for customer ${customerId}`);
  // Optionally log to a payments table for your own records
}

async function handlePaymentFailed(invoice: Stripe.Invoice) {
  const customerId = invoice.customer as string;
  // Stripe will retry automatically (Smart Retries) and send dunning emails.
  // You may want to:
  // 1. Show a banner in the app: "Payment failed, please update your card"
  // 2. Send your own notification email
  // 3. After final retry failure, Stripe will cancel the subscription
  //    and fire customer.subscription.deleted
  console.warn(`Payment failed for customer ${customerId}`);
}

async function handleSubscriptionUpdated(subscription: Stripe.Subscription) {
  const customerId = subscription.customer as string;
  const priceId = subscription.items.data[0].price.id;
  const tier = getTierFromPriceId(priceId);

  await updateUserByStripeCustomerId(customerId, { tier });
}

async function handleSubscriptionDeleted(subscription: Stripe.Subscription) {
  const customerId = subscription.customer as string;

  // Subscription is fully canceled -- downgrade to free
  await updateUserByStripeCustomerId(customerId, {
    tier: 'free',
    stripe_subscription_id: null,
  });
}

// --- Helpers ---

function getTierFromPriceId(priceId: string): string {
  const premiumPrices = [
    process.env.STRIPE_PRICE_PREMIUM_MONTHLY,
    process.env.STRIPE_PRICE_PREMIUM_ANNUAL,
  ];
  const proPrices = [
    process.env.STRIPE_PRICE_PRO_MONTHLY,
    process.env.STRIPE_PRICE_PRO_ANNUAL,
  ];

  if (premiumPrices.includes(priceId)) return 'premium';
  if (proPrices.includes(priceId)) return 'pro';
  return 'free';
}
```

### Critical Implementation Notes

1. **Raw body is required.** Stripe verifies webhooks by hashing the raw request body. Use `await req.text()`, not `await req.json()`. The App Router does not parse the body automatically, but be aware that middleware or other configurations could interfere.

2. **Idempotency.** Stripe may send the same event more than once. Your handlers must be idempotent -- processing the same event twice should not cause problems. Use the `event.id` to deduplicate if needed.

3. **Return 200 quickly.** Stripe expects a 2xx response within 20 seconds. Do not perform long-running operations in the webhook handler. If you need to do heavy work, queue it and return 200 immediately.

4. **Retry behavior.** In live mode, Stripe retries failed webhook deliveries for up to 3 days with exponential backoff. In test mode, it retries 3 times over a few hours.

---

## 7. Customer Portal

The Stripe Customer Portal is a hosted page where subscribers can:

- Update their payment method (card on file)
- View invoice history and download receipts
- Switch between plans (upgrade/downgrade)
- Cancel their subscription
- Update billing address

This eliminates the need to build any subscription management UI yourself.

### Dashboard Configuration

1. Go to Stripe Dashboard > Settings > Billing > Customer portal
2. Click "Activate link"
3. Configure:
   - **Cancellation:** Allow cancellations, optionally collect cancellation reason, offer a retention coupon
   - **Plan switching:** Allow upgrades and downgrades between Premium and Pro
   - **Payment method updates:** Enable
   - **Invoice history:** Enable
   - **Branding:** Set logo, brand color, headline

### Server Action to Redirect to Portal

```typescript
// app/actions/stripe.ts (add to existing file)

export async function createPortalSession() {
  const session = await auth();
  if (!session?.user?.email) {
    redirect('/login');
  }

  const user = await getUserByEmail(session.user.email);
  if (!user?.stripe_customer_id) {
    redirect('/pricing'); // Not a subscriber yet
  }

  const portalSession = await stripe.billingPortal.sessions.create({
    customer: user.stripe_customer_id,
    return_url: `${process.env.NEXT_PUBLIC_APP_URL}/account`,
  });

  redirect(portalSession.url);
}
```

### Account Page Button

```typescript
// components/manage-subscription-button.tsx
'use client';

import { createPortalSession } from '@/app/actions/stripe';

export function ManageSubscriptionButton() {
  return (
    <form action={createPortalSession}>
      <button
        type="submit"
        className="text-blue-600 hover:text-blue-800 underline"
      >
        Manage Subscription
      </button>
    </form>
  );
}
```

---

## 8. Freemium Model Implementation

### Feature Gating Strategy

The tech spec defines three access tiers. Feature gating happens at two levels:

1. **Frontend:** Next.js middleware checks `user.tier` and redirects or shows upgrade prompts
2. **Backend:** FastAPI rate limiter checks `user.tier` and enforces request limits

### Database Schema (Already in Tech Spec)

The `users` table from the technical spec already includes the necessary columns:

```sql
CREATE TABLE users (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    email                 TEXT NOT NULL UNIQUE,
    name                  TEXT,
    tier                  TEXT NOT NULL DEFAULT 'free',   -- 'free', 'premium', 'pro'
    stripe_customer_id    TEXT,
    stripe_subscription_id TEXT,                          -- ADD THIS COLUMN
    subscription_status   TEXT DEFAULT 'none',            -- ADD: 'active', 'past_due', 'canceled', 'none'
    current_period_end    TEXT,                           -- ADD: subscription period end date
    created_at            TEXT NOT NULL DEFAULT (datetime('now')),
    last_login            TEXT
);
```

The three additional columns (`stripe_subscription_id`, `subscription_status`, `current_period_end`) should be added to the schema in the tech spec. They enable the app to check subscription status without calling the Stripe API on every request.

### Next.js Middleware for Feature Gating

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { getToken } from 'next-auth/jwt';

// Routes that require Premium or Pro tier
const PREMIUM_ROUTES = [
  '/tools/coa-analyzer',      // Unlimited COA scans
  '/vendors/*/detailed',      // Detailed vendor reports
  '/alerts',                  // Vendor alerts
  '/api/v1/export',           // Bulk data export (Pro only)
];

export async function middleware(request: NextRequest) {
  const token = await getToken({ req: request });
  const path = request.nextUrl.pathname;

  // Check if path matches a premium route
  const isPremiumRoute = PREMIUM_ROUTES.some((route) => {
    const pattern = route.replace('*', '[^/]+');
    return new RegExp(`^${pattern}$`).test(path);
  });

  if (isPremiumRoute) {
    if (!token) {
      // Not logged in -- redirect to login
      return NextResponse.redirect(
        new URL(`/login?callbackUrl=${path}`, request.url)
      );
    }

    const tier = token.tier as string;
    if (tier === 'free' || !tier) {
      // Logged in but free tier -- show upgrade prompt
      return NextResponse.redirect(
        new URL(`/pricing?upgrade=true&from=${path}`, request.url)
      );
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/tools/:path*', '/vendors/:path*/detailed', '/alerts/:path*', '/api/v1/export/:path*'],
};
```

### Backend Rate Limiting by Tier

The tech spec already defines rate limits. Implement in FastAPI using `slowapi`:

```python
# backend/app/middleware/rate_limit.py
from slowapi import Limiter
from slowapi.util import get_remote_address

def get_rate_limit(request):
    """Return rate limit string based on user tier."""
    user = request.state.user  # set by auth middleware
    if user and user.tier == 'pro':
        return "300/minute"
    elif user and user.tier == 'premium':
        return "300/minute"
    elif user:
        return "60/minute"
    else:
        return "30/minute"  # anonymous

limiter = Limiter(key_func=get_remote_address)
```

### Feature Availability Matrix

| Feature | Anonymous | Free (Auth) | Premium ($9.99) | Pro ($19.99) |
|---------|-----------|-------------|-----------------|--------------|
| Vendor database (search/filter) | Yes | Yes | Yes | Yes |
| Regulatory status tracker | Yes | Yes | Yes | Yes |
| Storage calculator | Yes | Yes | Yes | Yes |
| Peptide info pages | Yes | Yes | Yes | Yes |
| COA upload (basic, 3/day) | Yes | Yes (5/day) | Unlimited | Unlimited |
| Detailed vendor reports | No | No | Yes | Yes |
| Vendor alerts | No | No | Yes | Yes |
| Historical data access | No | No | Yes | Yes |
| API access | No | No | No | Yes |
| Bulk data export | No | No | No | Yes |
| Rate limit | 30 req/min | 60 req/min | 300 req/min | 300 req/min |
| Daily request cap | 500 | 2,000 | 20,000 | 20,000 |

### Soft vs Hard Gates

Use **soft gates** (show content with an upgrade prompt) for features where seeing a preview drives conversion:

- Detailed vendor reports: show the first 3 data points, blur the rest with "Upgrade to see full report"
- Historical test data: show the latest result, gate the history chart

Use **hard gates** (redirect to pricing page) for features that are entirely premium:

- Vendor alerts
- API access
- Bulk export

---

## 9. Pricing Page

### Stripe Pricing Table vs Custom Page

Stripe offers an embeddable Pricing Table component that requires zero code -- you configure it in the Dashboard and paste a `<script>` tag. For Peptide Checker, a **custom pricing page** is recommended because:

1. **Better storytelling.** You need to explain what each tier unlocks in the context of peptide verification (COA scans, vendor alerts, detailed reports). The Stripe component is generic.
2. **Annual/monthly toggle.** Custom pages handle this more elegantly.
3. **Design integration.** A custom page matches the site's Tailwind styling.
4. **Upgrade context.** You can show the specific feature the user was trying to access when redirected (e.g., "Upgrade to unlock Detailed Vendor Reports").

The Stripe Pricing Table is a good option if you want to ship even faster and do not need the customization. You can always start with the Stripe component and replace it with a custom page later.

### Custom Pricing Page Design

```typescript
// app/pricing/page.tsx
'use client';

import { useState } from 'react';
import { CheckoutButton } from '@/components/checkout-button';

export default function PricingPage() {
  const [annual, setAnnual] = useState(false);

  return (
    <div className="max-w-5xl mx-auto py-16 px-4">
      <h1 className="text-4xl font-bold text-center">
        Verify peptide quality with confidence
      </h1>
      <p className="text-lg text-gray-600 text-center mt-4 max-w-2xl mx-auto">
        Free tools for everyone. Premium features for serious researchers.
      </p>

      {/* Annual/Monthly Toggle */}
      <div className="flex justify-center mt-8 gap-3 items-center">
        <span className={!annual ? 'font-bold' : 'text-gray-500'}>Monthly</span>
        <button
          onClick={() => setAnnual(!annual)}
          className="relative w-14 h-7 bg-gray-300 rounded-full"
        >
          <span
            className={`absolute top-0.5 left-0.5 w-6 h-6 bg-white rounded-full
                        transition ${annual ? 'translate-x-7' : ''}`}
          />
        </button>
        <span className={annual ? 'font-bold' : 'text-gray-500'}>
          Annual <span className="text-green-600 text-sm">Save 17%</span>
        </span>
      </div>

      {/* Pricing Cards */}
      <div className="grid md:grid-cols-3 gap-8 mt-12">
        {/* Free */}
        <div className="border rounded-xl p-8">
          <h2 className="text-2xl font-bold">Free</h2>
          <p className="text-4xl font-bold mt-4">$0</p>
          <ul className="mt-6 space-y-3 text-gray-700">
            <li>Vendor database search</li>
            <li>Regulatory status tracker</li>
            <li>Storage calculator</li>
            <li>3 COA scans per day</li>
          </ul>
          <a href="/register" className="block mt-8 text-center ...">
            Get Started
          </a>
        </div>

        {/* Premium */}
        <div className="border-2 border-blue-600 rounded-xl p-8 relative">
          <span className="absolute -top-3 left-1/2 -translate-x-1/2
                           bg-blue-600 text-white px-3 py-1 rounded-full text-sm">
            Most Popular
          </span>
          <h2 className="text-2xl font-bold">Premium</h2>
          <p className="text-4xl font-bold mt-4">
            {annual ? '$8.25' : '$9.99'}
            <span className="text-lg font-normal text-gray-500">/mo</span>
          </p>
          {annual && (
            <p className="text-sm text-gray-500">Billed $99/year</p>
          )}
          <ul className="mt-6 space-y-3 text-gray-700">
            <li>Everything in Free, plus:</li>
            <li>Unlimited COA scans</li>
            <li>Detailed vendor reports</li>
            <li>Vendor quality alerts</li>
            <li>Historical test data</li>
          </ul>
          <CheckoutButton
            priceId={
              annual
                ? process.env.NEXT_PUBLIC_STRIPE_PRICE_PREMIUM_ANNUAL!
                : process.env.NEXT_PUBLIC_STRIPE_PRICE_PREMIUM_MONTHLY!
            }
            label="Subscribe"
          />
        </div>

        {/* Pro */}
        <div className="border rounded-xl p-8">
          <h2 className="text-2xl font-bold">Pro</h2>
          <p className="text-4xl font-bold mt-4">
            {annual ? '$16.58' : '$19.99'}
            <span className="text-lg font-normal text-gray-500">/mo</span>
          </p>
          {annual && (
            <p className="text-sm text-gray-500">Billed $199/year</p>
          )}
          <ul className="mt-6 space-y-3 text-gray-700">
            <li>Everything in Premium, plus:</li>
            <li>B2B API access</li>
            <li>Bulk data export</li>
            <li>Priority support</li>
          </ul>
          <CheckoutButton
            priceId={
              annual
                ? process.env.NEXT_PUBLIC_STRIPE_PRICE_PRO_ANNUAL!
                : process.env.NEXT_PUBLIC_STRIPE_PRICE_PRO_MONTHLY!
            }
            label="Subscribe"
          />
        </div>
      </div>
    </div>
  );
}
```

### Free Trial Considerations

For Peptide Checker MVP, a free trial is **not recommended** at launch. Reasons:

- The free tier already provides substantial value, which serves as the "trial"
- Free trials attract low-intent users who churn immediately after the trial
- Trials add complexity (trial_end webhooks, grace periods, UI states)
- Better approach: let the free tier prove value, then gate the features users actually want

If you add trials later, Stripe makes it trivial:

```typescript
const checkoutSession = await stripe.checkout.sessions.create({
  // ... other params
  subscription_data: {
    trial_period_days: 7, // 7-day free trial
  },
});
```

---

## 10. Revenue Tracking and Analytics

### Stripe Dashboard (Built-in, Free)

Stripe's built-in Billing analytics dashboard provides:

| Metric | Description |
|--------|-------------|
| **MRR** | Monthly Recurring Revenue (sum of all active subscription values, normalized to monthly) |
| **Active subscribers** | Count by plan |
| **Churn rate** | Percentage of subscribers who cancel per month |
| **New MRR** | Revenue from new subscriptions |
| **Expansion MRR** | Revenue from upgrades |
| **Contraction MRR** | Revenue lost to downgrades |
| **Churned MRR** | Revenue lost to cancellations |
| **Net MRR movement** | New + Expansion - Contraction - Churned |

Configure metrics at Dashboard > Billing > Overview > Configure.

Note: Stripe analytics data has a ~72-hour delay before appearing in the Dashboard.

### Stripe Revenue Recognition

Stripe Revenue Recognition (available on Stripe Billing Scale plan) automatically generates ASC 606 / IFRS 15 compliant reports. For a solo founder, this is overkill at launch but becomes relevant if you need investor-ready financials or if you take on annual billing (which creates deferred revenue). The standard Billing analytics are sufficient for Phase 2-3.

### Integration with Analytics Tools

For Peptide Checker, the tech spec recommends Plausible for privacy-focused web analytics. To connect subscription data:

**Option 1: Custom events via Plausible API**
Track conversion events (subscribe, upgrade, cancel) from your webhook handler:

```typescript
// In your webhook handler, after processing checkout.session.completed:
await fetch('https://plausible.io/api/event', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'Subscription',
    url: 'https://peptidechecker.com/pricing',
    domain: 'peptidechecker.com',
    props: { tier: 'premium', billing: 'monthly' },
  }),
});
```

**Option 2: PostHog (if you switch later)**
PostHog has a native Stripe integration that syncs customer and subscription data automatically. Useful for cohort analysis (which features do paying users use most?).

### Key Metrics to Track from Day One

| Metric | Target (Month 6) | Target (Month 12) |
|--------|-------------------|---------------------|
| MRR | $1,000-$2,000 | $8,000-$15,000 |
| Active subscribers | 100-200 | 500-1,000 |
| Monthly churn rate | <8% | <6% |
| Conversion rate (free to paid) | 2-3% | 3-5% |
| ARPU | $9.99-$12.00 | $12.00-$15.00 |

These targets align with the business plan's revenue projections.

---

## 11. Tax Handling

### Stripe Tax

Stripe Tax automatically calculates and collects sales tax, VAT, and GST. For a US-based SaaS product selling digital goods:

- SaaS products are taxable in many US states (the rules vary state by state)
- Stripe Tax determines the customer's location and applies the correct rate
- Tax is added to the checkout total or can be included in the price

### Setup

1. Go to Stripe Dashboard > Settings > Tax
2. Set your business address (tax origin)
3. Register for tax in states where you have nexus (obligation to collect)
4. Set the default product tax code to `txcd_10103001` (Software as a Service - business use) or `txcd_10103000` (SaaS - personal use)
5. Enable automatic tax calculation on Checkout Sessions:

```typescript
const checkoutSession = await stripe.checkout.sessions.create({
  // ... other params
  automatic_tax: { enabled: true },
});
```

### When to Enable

For an MVP with <$100K revenue, tax compliance is important but the cost of getting it wrong is low. Start with Stripe Tax enabled from day one -- it costs 0.5% per transaction but saves significant accounting headaches. The alternative is tracking nexus, rates, and filings manually, which is not viable for a solo founder.

### Tax Registration

You must register with state tax authorities before collecting tax. At launch, you likely have nexus only in your home state. As revenue grows, you may trigger economic nexus thresholds (typically $100K in sales or 200 transactions per state per year). Stripe Tax tells you when you are approaching thresholds.

---

## 12. Testing and Launch

### Test Mode Workflow

Stripe provides a complete sandbox environment. All test mode operations use separate API keys (prefixed `sk_test_` and `pk_test_`).

1. **Create test products and prices** in the Stripe Dashboard (test mode toggle in upper right)
2. **Use test card numbers** to simulate payments
3. **Trigger test webhooks** using the Stripe CLI
4. **Verify your database** updates correctly after each event

### Test Card Numbers

| Card Number | Scenario |
|-------------|----------|
| `4242 4242 4242 4242` | Successful payment |
| `4000 0000 0000 3220` | Triggers 3D Secure authentication |
| `4000 0000 0000 9995` | Payment declined (insufficient funds) |
| `4000 0000 0000 0341` | Attaching card fails |
| `4000 0025 0000 3155` | Requires authentication on all transactions |
| `4000 0000 0000 0002` | Card declined (generic) |

Use any future expiration date, any 3-digit CVC, and any 5-digit ZIP code.

For programmatic testing (API calls), use PaymentMethod tokens like `pm_card_visa` instead of raw card numbers.

### Local Webhook Testing with Stripe CLI

```bash
# Install Stripe CLI
# macOS: brew install stripe/stripe-cli/stripe
# Windows: scoop install stripe

# Login
stripe login

# Forward webhooks to your local dev server
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# The CLI will output a webhook signing secret (whsec_...) -- use this
# as STRIPE_WEBHOOK_SECRET in .env.local during development

# In another terminal, trigger test events:
stripe trigger checkout.session.completed
stripe trigger invoice.paid
stripe trigger invoice.payment_failed
stripe trigger customer.subscription.deleted
```

### Testing Checklist

- [ ] Successful subscription purchase (Premium monthly)
- [ ] Successful subscription purchase (Premium annual)
- [ ] Successful subscription purchase (Pro monthly)
- [ ] Successful subscription purchase (Pro annual)
- [ ] User tier updates to 'premium' or 'pro' after purchase
- [ ] Rate limits change after upgrade
- [ ] Premium features become accessible after purchase
- [ ] Payment failure triggers appropriate handling
- [ ] Subscription cancellation via Customer Portal works
- [ ] Tier downgrades to 'free' after cancellation
- [ ] Plan upgrade from Premium to Pro works
- [ ] Plan downgrade from Pro to Premium works
- [ ] Webhook signature verification rejects invalid signatures
- [ ] Duplicate webhook events are handled idempotently
- [ ] Anonymous users see upgrade prompts on premium features
- [ ] Free users see upgrade prompts on premium features

### Go-Live Checklist

From Stripe's official go-live documentation:

1. **Replace API keys.** Swap `sk_test_` and `pk_test_` keys with `sk_live_` and `pk_live_` keys. Use environment variables -- never hardcode.

2. **Rotate keys.** Generate fresh live keys immediately before launch. If test keys were ever exposed (in git history, logs, screenshots), the live keys must be completely new.

3. **Recreate products in live mode.** Products, Prices, and Coupons created in test mode do not carry over to live mode. Recreate them (or run the `create-stripe-products.ts` script with live keys).

4. **Register live webhook endpoint.** In Stripe Dashboard > Developers > Webhooks, add your production URL (`https://peptidechecker.com/api/webhooks/stripe`) and select the events to receive.

5. **Set API version.** Pin to a specific Stripe API version in your code. Upgrade deliberately, not automatically.

6. **Test with real cards.** Make a real $1 charge (or a real subscription purchase) and then refund it. Verify the webhook flow works end-to-end in production.

7. **Error handling.** Verify that declined cards, expired cards, and network errors are handled gracefully in the UI.

8. **Logging.** Ensure you are logging webhook events and errors server-side. Do not log full card numbers or PII.

9. **PCI compliance.** Using Stripe Checkout means you qualify for SAQ A (Self-Assessment Questionnaire A), the simplest PCI compliance level. Stripe fills out most of the form for you. Complete it in Dashboard > Settings > Compliance.

10. **Legal pages.** Ensure your Terms of Service and Privacy Policy reference subscription billing, cancellation policy, and refund policy.

---

## 13. Code Scaffolding

### Directory Structure

```
peptide-checker/
├── app/
│   ├── api/
│   │   └── webhooks/
│   │       └── stripe/
│   │           └── route.ts          # Stripe webhook handler
│   ├── actions/
│   │   └── stripe.ts                 # Server Actions: createCheckoutSession, createPortalSession
│   ├── pricing/
│   │   └── page.tsx                  # Pricing page with tier cards
│   ├── account/
│   │   └── page.tsx                  # Account page with subscription status
│   └── layout.tsx
├── components/
│   ├── checkout-button.tsx           # Subscribe button (calls server action)
│   ├── manage-subscription-button.tsx # Portal redirect button
│   ├── upgrade-prompt.tsx            # Soft gate component ("Upgrade to see more")
│   └── tier-badge.tsx                # Displays user's current tier
├── lib/
│   ├── stripe.ts                     # Server-side Stripe client
│   ├── stripe-client.ts             # Client-side Stripe (loadStripe)
│   └── auth.ts                       # NextAuth.js config
├── middleware.ts                      # Feature gating middleware
├── scripts/
│   └── create-stripe-products.ts     # One-time product/price setup
├── .env.local                        # Environment variables (NEVER commit)
└── .env.example                      # Template for env vars (commit this)
```

### Key Files and Their Purposes

| File | Purpose | When It Runs |
|------|---------|--------------|
| `lib/stripe.ts` | Initializes server-side Stripe SDK with secret key | Imported by server code |
| `lib/stripe-client.ts` | Loads Stripe.js for client-side use | Imported by client components |
| `app/actions/stripe.ts` | Server Actions for creating Checkout and Portal sessions | Called by form submissions |
| `app/api/webhooks/stripe/route.ts` | Receives and processes Stripe webhook events | Called by Stripe servers |
| `middleware.ts` | Checks user tier before rendering premium routes | Every request to gated routes |
| `app/pricing/page.tsx` | Displays pricing tiers with subscribe buttons | User visits /pricing |
| `components/checkout-button.tsx` | Button that triggers checkout flow | On pricing page |
| `components/manage-subscription-button.tsx` | Button that redirects to Stripe Customer Portal | On account page |
| `components/upgrade-prompt.tsx` | Blur overlay with upgrade CTA for soft-gated content | On premium content pages |
| `scripts/create-stripe-products.ts` | Creates Products and Prices in Stripe | Run once during setup |

### .env.example

```env
# Stripe (get keys from https://dashboard.stripe.com/apikeys)
STRIPE_SECRET_KEY=<your-stripe-secret-key>
STRIPE_WEBHOOK_SECRET=<your-webhook-signing-secret>
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=<your-stripe-publishable-key>

# Stripe Price IDs (created via Dashboard or scripts/create-stripe-products.ts)
STRIPE_PRICE_PREMIUM_MONTHLY=price_xxxxxxxxx
STRIPE_PRICE_PREMIUM_ANNUAL=price_xxxxxxxxx
STRIPE_PRICE_PRO_MONTHLY=price_xxxxxxxxx
STRIPE_PRICE_PRO_ANNUAL=price_xxxxxxxxx

# Also expose price IDs to client for pricing page toggle
NEXT_PUBLIC_STRIPE_PRICE_PREMIUM_MONTHLY=price_xxxxxxxxx
NEXT_PUBLIC_STRIPE_PRICE_PREMIUM_ANNUAL=price_xxxxxxxxx
NEXT_PUBLIC_STRIPE_PRICE_PRO_MONTHLY=price_xxxxxxxxx
NEXT_PUBLIC_STRIPE_PRICE_PRO_ANNUAL=price_xxxxxxxxx

# App
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

---

## 14. Implementation Checklist

This checklist maps to the business plan's "Weeks 11-12" timeline (subscription and revenue prep).

### Phase 1: Stripe Account Setup (Day 1)

- [ ] Create Stripe account at stripe.com
- [ ] Complete business profile (name, address, bank account for payouts)
- [ ] Note test API keys from Dashboard > Developers > API keys
- [ ] Install Stripe CLI locally

### Phase 2: Products and Prices (Day 1)

- [ ] Create Premium product with monthly ($9.99) and annual ($99) prices
- [ ] Create Pro product with monthly ($19.99) and annual ($199) prices
- [ ] Record Price IDs in `.env.local`
- [ ] Run `scripts/create-stripe-products.ts` or configure via Dashboard

### Phase 3: Core Integration (Days 2-3)

- [ ] Install npm packages: `stripe`, `@stripe/stripe-js`, `@stripe/react-stripe-js`
- [ ] Create `lib/stripe.ts` (server) and `lib/stripe-client.ts` (client)
- [ ] Add `stripe_subscription_id`, `subscription_status`, `current_period_end` columns to `users` table
- [ ] Build `app/actions/stripe.ts` with `createCheckoutSession` and `createPortalSession`
- [ ] Build `app/api/webhooks/stripe/route.ts` webhook handler
- [ ] Build pricing page at `app/pricing/page.tsx`
- [ ] Build checkout button component
- [ ] Build manage subscription button component

### Phase 4: Feature Gating (Day 4)

- [ ] Implement `middleware.ts` for premium route protection
- [ ] Build upgrade prompt component for soft gates
- [ ] Update FastAPI rate limiter to check user tier
- [ ] Test all gated features with free, premium, and pro accounts

### Phase 5: Testing (Days 5-6)

- [ ] Set up Stripe CLI webhook forwarding
- [ ] Test complete subscription purchase flow (all 4 price combinations)
- [ ] Test payment failure handling
- [ ] Test cancellation via Customer Portal
- [ ] Test plan upgrades and downgrades
- [ ] Verify database updates correctly for all webhook events
- [ ] Run through full testing checklist (Section 12)

### Phase 6: Customer Portal (Day 6)

- [ ] Configure Customer Portal in Stripe Dashboard
- [ ] Set cancellation options and retention coupon
- [ ] Enable plan switching
- [ ] Test portal flow end-to-end

### Phase 7: Go Live (Day 7)

- [ ] Switch to live API keys
- [ ] Recreate products and prices in live mode
- [ ] Register production webhook endpoint
- [ ] Enable Stripe Tax (set tax code, register in home state)
- [ ] Complete PCI SAQ A in Dashboard
- [ ] Make a real test purchase and refund
- [ ] Update Terms of Service with billing/cancellation policy
- [ ] Deploy

### Estimated Total Implementation Time: 5-7 days

This assumes the Next.js frontend and FastAPI backend are already deployed (per the tech spec's Phase 1 MVP). The Stripe integration is a Phase 2 feature that layers on top of the existing auth and database infrastructure.

---

## Sources

- [Stripe Billing Documentation](https://stripe.com/billing)
- [Recurring Pricing Models](https://docs.stripe.com/products-prices/pricing-models)
- [Build a Subscriptions Integration](https://docs.stripe.com/billing/subscriptions/build-subscriptions)
- [Sell Subscriptions as a SaaS Startup](https://docs.stripe.com/get-started/use-cases/saas-subscriptions)
- [Integrate a SaaS Business on Stripe](https://docs.stripe.com/saas)
- [How Subscriptions Work](https://docs.stripe.com/billing/subscriptions/overview)
- [Using Webhooks with Subscriptions](https://docs.stripe.com/billing/subscriptions/webhooks)
- [Types of Events (Stripe API Reference)](https://docs.stripe.com/api/events/types)
- [Stripe Checkout vs Elements](https://support.stripe.com/questions/choosing-between-payment-links-invoicing-checkout-and-payment-element)
- [Configure the Customer Portal](https://docs.stripe.com/customer-management/configure-portal)
- [Integrate the Customer Portal with the API](https://docs.stripe.com/customer-management/integrate-customer-portal)
- [Embeddable Pricing Table](https://docs.stripe.com/payments/checkout/pricing-table)
- [Stripe Billing Analytics](https://docs.stripe.com/billing/subscriptions/analytics)
- [Revenue Recognition Reports](https://docs.stripe.com/revenue-recognition/reports)
- [Set Up Stripe Tax](https://docs.stripe.com/tax/set-up)
- [Collect Taxes for Recurring Payments](https://docs.stripe.com/tax/subscriptions)
- [SaaS Sales Tax in the US](https://stripe.com/guides/introduction-to-saas-taxability-in-the-us)
- [Test Card Numbers](https://docs.stripe.com/testing)
- [Go-Live Checklist](https://docs.stripe.com/get-started/checklist/go-live)
- [PCI DSS Compliance Guide](https://stripe.com/guides/pci-compliance)
- [The Ultimate Guide to Stripe + Next.js (2026 Edition)](https://dev.to/sameer_saleem/the-ultimate-guide-to-stripe-nextjs-2026-edition-2f33)
- [Stripe + Next.js 15 Complete Guide](https://www.pedroalonso.net/blog/stripe-nextjs-complete-guide-2025/)
- [Getting Started with Next.js, TypeScript, and Stripe Checkout (Vercel)](https://vercel.com/kb/guide/getting-started-with-nextjs-typescript-stripe)
- [stripe-node Webhook Signing Example (GitHub)](https://github.com/stripe/stripe-node/blob/master/examples/webhook-signing/nextjs/app/api/webhooks/route.ts)
- [Vercel Next.js SaaS Starter](https://github.com/vercel/nextjs-subscription-payments)
- [Next.js SaaS Starter (nextjs/saas-starter)](https://github.com/nextjs/saas-starter)
- [Stripe Billing Pricing](https://stripe.com/billing/pricing)

---

*Guide generated 2026-03-24 | Peptide Checker Stripe Integration*
*This is an internal technical document. Not for public distribution without review.*
