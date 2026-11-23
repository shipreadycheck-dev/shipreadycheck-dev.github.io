---
title: Can a stranger run up your AI bill? Rate limits and spending caps for AI-built apps
description: How to check whether anyone can drain your OpenAI or Gemini credit through your AI-built app, and how to add rate limits and hard spending caps before launch.
slug: ai-api-bill-rate-limits-spending-caps
updated: 2026-11-23
---

# Can a stranger run up your AI bill? Rate limits and spending caps for AI-built apps

Every time someone uses the AI feature in your app, like a chat box, a summary button or an image generator, you pay the AI provider for it. That's fine when real users click it a few times a day. It's a problem when a script clicks it ten thousand times an hour.

Hiding your API key on the server matters, but it isn't the whole job. If your server forwards any request to OpenAI or Gemini for anyone who asks, a stranger doesn't need your key. They can use your app as a free AI service that you pay for.

Here's how to check in about 15 minutes, and how to add two limits: a rate limit in your app and a hard spending cap at your provider.

## Why this matters

OWASP's top 10 list of risks for apps built on large language models includes this one. Its [LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/) entry describes "Denial of Wallet": attackers send a high volume of requests to exploit the pay-per-use pricing of AI services, leaving the app owner with costs they can't sustain.

Real bills show how fast this adds up. [Cybernews reported](https://cybernews.com/security/stolen-gemini-api-key-can-massively-rack-up-cloud-bill/) on a Reddit post, which it noted was unverified, from a three-person team in Mexico. They said a compromised Google Cloud API key ran up a bill of $82,314.44 over February 11 and 12, almost all of it Gemini usage, on an account that usually cost about $180. The poster said they had basic alerts, but nothing that actually stopped usage.

That last detail is the key lesson. An alert tells you about the damage. A cap limits it. In May 2026, [Tech News Day reported](https://technewsday.com/google-cloud-users-report-api-key-abuse-leading-to-massive-ai-bills/) that other Google Cloud customers described bills worth tens of thousands of dollars from abused keys, and that Google has since added safeguards such as new key types and required restrictions on keys.

Those cases involved stolen keys. An open AI endpoint in your own app leads to the same kind of bill, without anyone needing to steal anything.

**Think of it like this:** your AI feature is a taxi account in your name. Hiding the key is like keeping the account number secret. But if your front desk books a taxi for anyone who walks in and asks, the secret number doesn't save you. A rate limit is the desk saying "three rides per guest per day." A spending cap is the taxi company refusing more rides once the month's budget is used up.

## Why AI-built apps hit this

When you ask an AI tool to "add a chatbot," it builds the shortest path that works: a page that sends a message to a server route, and a route that passes it to the AI provider. Nothing in that request asks for limits, so usually none get added.

Three gaps are common:

- **The route doesn't check who's calling.** The page may require login, but the server route behind it often doesn't. Anyone who finds the route's address can call it directly.
- **There's no per-user limit.** One account can send as many requests as it likes, as fast as it likes.
- **There's no size limit.** A single huge message, or a request for a very long answer, costs far more than a normal one.

## The 15-minute check

### 1. List every paid service your app calls

Write down each AI provider (OpenAI, Gemini, Anthropic and so on) and any other pay-per-use service, like image generation, text messages or email.

### 2. Check for a hard cap at each provider

Log in to each provider's billing or limits settings and find out whether you have a cap that blocks requests, or only an alert.

- **OpenAI:** [OpenAI's spend limits guide](https://developers.openai.com/api/docs/guides/spend-limits) explains that a spend alert only sends a notification while traffic continues. A hard spend limit makes requests fail. You can set one for the whole organization or for a single project. In your organization or project **Limits** settings, under **Spend**, choose **Edit spend limit**, enter a **Monthly spend limit**, turn on **Enforce a hard limit**, and save.
- **Gemini:** Since March 2026, Google AI Studio lets you set a [monthly spend cap per project](https://blog.google/innovation-and-ai/technology/developers-tools/more-control-over-gemini-api-costs/) on its Spend page. Google says caps have about a 10 minute delay, and you are responsible for charges in that window. Google Cloud also offers [budgets with spend caps](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps) that can suspend an eligible service, including the Gemini API, once the cap is reached. A regular budget only sends alerts.
- **Everyone else:** look for "hard limit" or "spend cap." If you only find alerts, treat it as having no cap.

### 3. Find your AI request

Open your live app in Chrome. Right-click, choose **Inspect**, and open the **Network** tab. Now use your AI feature once. Look for the request that fires when you click.

- If it goes to your own site, like `/api/chat`, or to a function on your backend, like a Supabase Edge Function, that's normal. Note the address for the next step.
- If it goes straight to a provider like `api.openai.com` from the browser, your secret key is probably in your website's code. Stop here and read our [exposed API key check](exposed-api-keys.html) first.

### 4. Ask your coding agent to audit it

Paste this into Cursor, Claude Code, Lovable, Bolt or whatever you build with:

> List every server route, API endpoint and server function in this app that calls a paid service such as OpenAI, Gemini, Anthropic, image generation, SMS or email. For each one, tell me: does it reject requests from people who are not logged in, checked on the server? Is there a per-user rate limit or daily quota, and where is the count stored? Is there a limit on input size and on response length? Show me the exact lines for each check, or say clearly that there is none. Do not change anything yet.

Read the answer yourself. If it says a route is "protected," ask it to show the exact line that does the check.

## How to fix it

Work through these in order. The first one protects you today, even before any code changes.

1. **Turn on a hard cap at every provider.** Set it to an amount you could afford to lose in a month. Keep alerts on too, at a lower amount, so you hear about trouble early. Caps are not instant: OpenAI says spend can slightly exceed the limit, and Google notes its delay. When a cap is hit, your AI feature stops working until you raise it or the month resets, so pick a number with some headroom.
2. **Use a separate key or project for each app.** Then one app's cap and usage don't get mixed up with everything else you run.
3. **Require login on the server for every paid route.** Hiding a button on the page isn't enough. The route itself should reject requests that don't come from a logged-in user.
4. **Add a per-user rate limit and a daily quota.** OWASP recommends rate limiting and user quotas that restrict how many requests a single source can make in a given time. Keep the count on the server or in your database, never in the browser, where users can reset it. Ask your coding agent to suggest an approach that fits your hosting.
5. **Limit input size and answer length.** OWASP's guidance also says to keep inputs under reasonable size limits. Ask your agent to reject oversized messages and set a maximum response length on each AI call.
6. **Watch usage.** OWASP recommends monitoring for unusual patterns. A weekly look at your provider's usage page is a good start.

Once the limits are in, test them with your own account: send requests faster than your limit allows and confirm the app politely refuses. Only test your own app.

## Want someone to check it for you?

Start with the free [10-Minute Pre-Launch Security Checklist](https://shipreadycheck-dev.github.io/#free), or add the free [Ship-Ready Scan GitHub Action](https://github.com/shipreadycheck-dev/shipready-scan) to flag exposed keys on every push.

Or have us look for you. The [Ship-Ready Check](https://shipreadycheck-dev.github.io/#pricing) reviews your repo for unprotected paid endpoints, exposed keys, open database rules, unverified payments and more, and sends a plain-English report within 24 hours. From $29.
