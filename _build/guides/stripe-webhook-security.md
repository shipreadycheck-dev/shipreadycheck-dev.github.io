---
title: Can people get your paid plan for free? Checking Stripe in a vibe-coded app
description: How unverified Stripe webhooks and browser-set prices let people unlock paid features without paying in apps built with AI tools, and how to check and fix yours.
slug: stripe-webhook-security
updated: 2026-10-15
---

# Can people get your paid plan for free? Checking Stripe in a vibe-coded app

You asked your AI tool for Stripe payments. The test card went through, the success page says thank you, and the user got Pro. It works, so it feels done.

But there are three quiet mistakes AI tools often make in payment code, and each one can let someone get your paid plan without paying. This guide shows how to check for all three.

## How Stripe tells your app someone paid

When a customer pays, Stripe sends a message to your server called a **webhook**. It says something like "checkout completed for this customer". Your app reads it and unlocks their plan.

**Think of it like this:** a webhook is a letter saying "this person paid". If your app believes any letter that says so, anyone can write one.

## Mistake 1: the webhook doesn't check it's really from Stripe

Stripe signs every webhook with a secret only you and Stripe know. Your code has to check that signature. If it doesn't, anyone can send your server a fake "payment succeeded" message.

AI-generated code often skips this check, and it [shows up across many vibe-coded apps](https://vibe-eval.com/patterns/stripe-webhook-and-paid-trust/). A safe handler looks roughly like this:

```js
const event = stripe.webhooks.constructEvent(
  rawBody,                                  // the raw request body, not parsed JSON
  req.headers["stripe-signature"],
  process.env.STRIPE_WEBHOOK_SECRET
);
```

Two details matter. First, it must use the **raw** request body. Many apps parse the body as JSON first, and then the check can never pass. Second, if `constructEvent` throws, the handler must reject the request instead of carrying on.

## Mistake 2: the price comes from the browser

If your checkout code sends the price from the page to your server, like `unit_amount: req.body.price`, a buyer can edit that request and pay one cent for anything. The server should accept only a product ID and look up the real price itself, or use a Stripe Price ID.

## Mistake 3: the success page unlocks access

Some apps unlock Pro when the user lands on `/success`. Anyone can type that address. Access should come only from a verified webhook, never from visiting a page.

## How to check your own app

Paste this into your coding agent:

> Check the Stripe integration. 1) Does the webhook handler verify the signature with stripe.webhooks.constructEvent on the raw request body, and reject the request if it fails? 2) Is every price set on the server, never taken from the browser? 3) Does access come only from the verified webhook, not from the success page? 4) Does the handler ignore duplicate event IDs? Show me the code for each answer. Do not change anything yet.

Then test it yourself. With the [Stripe CLI](https://docs.stripe.com/stripe-cli), forward real signed test events to your local app:

```
stripe listen --forward-to localhost:3000/api/stripe/webhook
```

Then send the same endpoint an unsigned request, with no Stripe signature. A correct handler accepts the real event and rejects the fake one with an error. If both succeed, you have Mistake 1.

## How to fix it

1. Verify every webhook with `constructEvent` on the raw body, using the signing secret from your Stripe dashboard.
2. Set prices on the server only.
3. Unlock access only from the verified `checkout.session.completed` event, and store processed event IDs so a retried event doesn't grant access twice.
4. Remove any logic that unlocks access from the success page.

## Want someone to check it for you?

The free [10-Minute Pre-Launch Security Checklist](https://shipreadycheck-dev.github.io/#free) includes a payment check with a ready-to-paste prompt.

Or send us your repo. The [Ship-Ready Check](https://shipreadycheck-dev.github.io/#pricing) checks your payment flow, database rules and keys, and sends a plain-English report within 24 hours. From $29.
