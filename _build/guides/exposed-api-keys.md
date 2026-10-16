---
title: Is your API key exposed in your AI-built app? How to check in 2 minutes
description: How to find OpenAI, Stripe, Gemini or Supabase secret keys leaking from an app built with Lovable, Bolt, Cursor or Claude Code, and what to do if you find one.
slug: exposed-api-keys
updated: 2026-10-15
---

# Is your API key exposed in your AI-built app? How to check in 2 minutes

Ask an AI tool to "add ChatGPT to my app" or "connect Stripe", and the fastest way to make it work is to paste the secret key straight into the code. It works on the first try. It also means anyone visiting your site can copy the key and spend your money.

This guide shows you how to check your own app in about two minutes, and what to do if you find a key.

## Why it's expensive

Bots scan public websites and code for keys constantly. Once one is found, it gets used fast.

In February 2026, a small team's stolen Google API key ran up **about $82,000 in Gemini charges in 48 hours**, on an account that normally spent around $180 a month. Google treated it as the customer's responsibility under its shared-responsibility model, as [The Register reported](https://theregister.com/2026/03/03/gemini_api_key_82314_dollar_charge/).

There's a twist that catches even careful builders: researchers found that Google API keys created for public use, like Maps, [can quietly gain access to Gemini](https://zuplo.com/blog/google-api-key-gemini-vulnerability-lessons) once the Gemini API is enabled on the same project. A key that was safe to publish last year may not be safe today.

## Which keys are safe to be public

Not every key is a secret. Here's the short version:

| Safe in your website | Never in your website |
|---|---|
| Stripe publishable key (`pk_...`) | Stripe secret key (`sk_live_...`, `rk_live_...`) |
| Supabase **anon** key | Supabase **service_role** key |
| Firebase `apiKey` | OpenAI, Anthropic or Gemini keys |
| | Database URLs with a password in them |
| | AWS keys (`AKIA...`), GitHub tokens (`ghp_...`) |

## The 2-minute check

### 1. Look at what your website sends to visitors

Open your live app in Chrome, right-click, and choose **Inspect**. Go to the **Sources** tab, press **Ctrl+Shift+F** (or **Cmd+Option+F** on a Mac) to search all files, and search for each of these one at a time:

- `sk-` (OpenAI and Anthropic keys)
- `sk_live` (Stripe)
- `service_role` (Supabase)
- `AIza` (Google)

Anything you find there, every visitor can find too.

### 2. Check your variable names

Frameworks copy certain variables into the website automatically, based on their prefix: `NEXT_PUBLIC_`, `VITE_`, `REACT_APP_` and `EXPO_PUBLIC_`. If a variable with one of those prefixes holds a secret, it's public, whatever its name says. `NEXT_PUBLIC_OPENAI_SECRET` is not a secret.

### 3. Check your repo

If your code is on GitHub, check that your `.env` file isn't in it and that `.gitignore` contains `.env*`. Then paste this into your coding agent:

> Search this project for API keys or secrets written directly in code, including OpenAI, Anthropic, Stripe secret keys, Supabase service_role keys, Google keys, AWS keys and database URLs with passwords. List every file and line. Do not change anything yet.

## Found one? Do this, in this order

1. **Rotate the key first.** Create a new key in the provider's dashboard and delete the old one. Deleting the key from your code is not enough, because a copy may already exist.
2. **Move the call to your server.** Your website should call your own backend route, and that route calls OpenAI or Stripe using a key stored in a server-only environment variable.
3. **Put a limit on it.** Set a spending cap or budget alert with every AI and cloud provider you use, and add a per-user rate limit to any endpoint that calls a paid API.
4. **Check your bill** for usage you don't recognize.

## Want someone to check it for you?

The free [10-Minute Pre-Launch Security Checklist](https://shipreadycheck-dev.github.io/#free) walks you through this and nine other checks.

Or send us your repo. The [Ship-Ready Check](https://shipreadycheck-dev.github.io/#pricing) finds exposed keys, open databases, unverified payments and more, and sends a plain-English report within 24 hours. From $29.
