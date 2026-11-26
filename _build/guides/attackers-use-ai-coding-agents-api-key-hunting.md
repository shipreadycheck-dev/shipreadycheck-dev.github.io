---
title: Attackers use coding agents too: an API key hunt that took under 6 minutes
description: An attacker pointed a free coding agent at a financial firm and went from first request to testing an access key in minutes. What happened and how to check your app.
slug: attackers-use-ai-coding-agents-api-key-hunting
updated: 2026-11-26
type: field-notes
---

# Attackers use coding agents too: an API key hunt that took under 6 minutes

Founders use coding agents to read docs, follow links and try things until something works. This week we got a clear look at an attacker doing the same thing, with the same kind of tool, against a real company. It took less than six minutes.

## What happened

On November 24, [The Register](https://www.theregister.com/security/2026/11/24/an-ai-coding-agent-a-browser-and-a-mac-tool-found-a-financial-firms-access-key-in-under-6-minutes/5311922) published an exclusive report from Jesta, a Tel Aviv security startup that builds tools to detect AI-driven attacks. Jesta described an attempted break-in at one of its customers, a major financial services company it did not name.

According to the report, on November 16 someone connecting from Bucharest pointed OpenCode, a free open-source coding agent, at the company's systems. No special hacking kit was involved. The Register says the toolkit was the agent, the Chrome browser and curl, a command-line tool that comes with Macs.

The agent behaved like a curious developer. Its first requests were refused, so it retried while posing as an Android phone, then asked for the system's API description. That was refused too. It then found a readable API document at a different address, read it, and followed a link inside it seconds later. From there it found an access key and tried to use it. It also tried no key and a key it made up, and tested several URLs before it stopped. [Dataconomy](https://dataconomy.com/2026/11/25/opencode-attack-finds-decoy-financial-firm-key-in-under/) reports the whole attempt ended 5 minutes and 44 seconds after it began.

The good news: the API document and the key were decoys that Jesta had planted. Its system flagged the visitor as an AI agent about a minute in and kept it inside a fake environment. Both articles say nothing real was taken. Jesta's CTO, Lior Finkelshtein, told The Register: "If that key had been real, it would have been in." The company and Jesta reported the activity to law enforcement, and the attacker has not been publicly identified.

Jesta also noted that no blocklist would have caught this. The traffic came from an ordinary internet connection that threat feeds did not list. What gave it away was behavior, such as following a link that only existed inside an API document and testing several keys within seconds.

## Why AI-built apps keep hitting this

Many small apps rely, without saying so, on not being noticed. A test key sits in a docs page. An admin route has no login because "nobody knows the URL." A preview deployment still talks to the real database. A human attacker would have to stumble onto them and bother to dig.

A coding agent doesn't get bored. It reads every page it can reach, follows every link and tries every key it finds. Finkelshtein's point to The Register was that the skill now lives in the model, so the person giving instructions barely needs any. Getting started is about as hard as installing an app.

AI-built apps are worth a second look here for a simple reason: they come together fast. Docs pages, test endpoints, example keys and preview links can pile up quickly, and nobody goes back to check which ones are still public and still working.

The insight most people miss: an unlisted URL is not a lock. Assume anything reachable without logging in will be read, and anything that looks like a key will be tried, within minutes.

## Check your own app in 5 minutes

1. **Look at your app the way a stranger would.** Open your live site in a private browser window, logged out. Visit any docs, API, admin, settings or "test" pages you know about. Anything that loads without asking you to sign in is public.
2. **Search for keys in what you ship.** In your browser, open the page source or developer tools and search for words like "secret", "sk_", "service_role" and "api_key". Our [exposed API keys guide](exposed-api-keys.html) walks through this step by step.
3. **Make sure example keys in docs are fake.** If your docs, README or help pages show a key, confirm it is a placeholder that does not work. If it is real, rotate it today at the service it belongs to.
4. **Check your preview and staging links.** Find old preview deployments in your hosting dashboard. Delete ones you don't need, and make sure none of them connect to real customer data without a login.
5. **Put a ceiling on damage.** Turn on spending caps and usage alerts for your AI and payment provider keys, so a stolen key gets noticed quickly. Our [rate limits and spending caps guide](ai-api-bill-rate-limits-spending-caps.html) shows how.

Then ask your coding agent to map what a stranger could reach:

> List every page, API route and endpoint in this project that can be reached without logging in, including docs, admin, test and preview routes. For each one, tell me what it returns and whether it checks for a logged-in user or a valid key on the server. Also list any real-looking API keys or secrets in docs, README files, example code or anything sent to the browser. Do not change anything yet, and do not print the secret values themselves.

Anything public that you didn't expect is your first fix.

## The takeaway

Attackers now have the same patient, link-following helper you do, and it costs them almost nothing to run. Hidden is no longer the same as safe. Put a real login or server-side key check in front of everything that matters, keep real keys out of anything public, and cap what a stolen key can spend.

## Want someone to check it for you?

Start with the free [10-Minute Pre-Launch Security Checklist](https://shipreadycheck-dev.github.io/#free), or add the free [Ship-Ready Scan GitHub Action](https://github.com/shipreadycheck-dev/shipready-scan) to flag exposed keys on every push.

Or have us look for you. The [Ship-Ready Check](https://shipreadycheck-dev.github.io/#pricing) reviews your repo for exposed keys, open databases, unverified payments and more, and sends a plain-English report.
