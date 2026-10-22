---
title: The OpenCode breach: your AI keys live in more places than your code
description: OpenCode says AI provider keys stored in its Console may have been exposed. What happened, why it matters for AI-built apps, and how to audit your own keys today.
slug: opencode-console-breach-ai-keys
updated: 2026-10-22
type: field-notes
---

# The OpenCode breach: your AI keys live in more places than your code

Most advice about leaked API keys is about your code: don't paste the key into the frontend, don't commit it to GitHub. This week was a reminder that your keys also live inside the tools you use to build. When one of those tools has a bad night, your key goes with it.

## What happened

OpenCode is a popular open-source AI coding agent. It also offers an optional hosted service called Console, where a team stores its own OpenAI, Anthropic or Google API key so members can use those models without seeing the key itself.

According to [The Hacker News](https://thehackernews.com/2026/10/opencode-console-breach-may-have.html), an intruder reached a legacy OpenCode system on the night of October 16. The next morning, OpenCode emailed affected users with the subject line "Action Required: Potential provider key breach." The company said 1.4% of Console users were affected, all of them people who had linked an outside AI provider, and described the incident as related to a large-scale distillation attack. Distillation means pulling huge numbers of answers out of an AI model to train a rival one, and stolen API keys are one way to pay for it.

[Infosecurity Magazine](https://infosecurity-magazine.com/news/opencode-breach-openai-anthropic) reports that OpenCode notified Anthropic, OpenAI and Google, and that co-founder Dax Raad said only the Console was involved, not OpenCode itself. The Hacker News adds that the command-line and desktop apps store keys locally, and Raad said those keys never reach OpenCode's servers.

Some things are still unknown. OpenCode says keys "may have been exposed" and has not confirmed that any were copied or used, though some users publicly reported unexpected charges on their provider accounts. OpenCode has not said how the attackers got in or how many keys the system held. [StepSecurity's write-up](https://www.stepsecurity.io/blog/opencode-security-breach) notes that, per the vendor, users who did not get the email were not affected.

## Why AI-built apps keep hitting this

The usual mental model is "my key is safe as long as it isn't in my code." That model is incomplete. If you build with AI tools, your key has probably been pasted into a coding agent, a hosting dashboard, an automation tool, a team workspace and a `.env` file on your laptop. Each one is a copy you don't control.

Two details from this incident are worth remembering. First, The Hacker News points out that deleting a key from Console does not revoke it. A copied key keeps working until you kill it at the provider. Second, a budget set inside a tool can't stop someone using a stolen key directly with the provider. The limits that do hold are the ones you set in your OpenAI, Anthropic or Google account.

The real lesson is not "OpenCode is unsafe." It's that most founders reuse one powerful key everywhere, with no spending limit, and would not notice it being abused until the bill arrives. That's a setup problem, and it's fixable in an afternoon.

## Check your own app in 5 minutes

1. **Search your inbox** for "Action Required: Potential provider key breach." If you used OpenCode Console and got it, rotate those keys first.
2. **Make a list of everywhere your AI keys live.** Your app's hosting settings, your coding tools, any automation or team workspace, and files on your computer. Be honest about the "I pasted it in once to test" places.
3. **Open the usage page** for each AI provider you pay for. Look back at least a week for spikes, models you don't use, or activity at hours you weren't working.
4. **Turn on spending limits or budget alerts** in each provider's billing settings, wherever they're offered.
5. **Give each tool its own key.** Then if one tool leaks, you revoke one key and your live app keeps running. When you rotate, create the new key, update everything that uses it, then revoke the old one at the provider.

Then ask your coding agent to map what's in your project:

> List every place in this project where an AI provider API key (OpenAI, Anthropic, Google or others) is read, stored or referenced, including env files, config files, CI settings and frontend code. For each, tell me which provider it is for and whether it could end up in the browser or in git history. Do not change anything yet.

If any key shows up in frontend code or git history, treat it as already public and follow our [exposed API keys guide](exposed-api-keys.html).

## The takeaway

Your AI key is only as safe as the least careful place you've pasted it. One key per tool, spending limits at the provider, and a quick look at usage each week turn a breach like this from a surprise bill into a five-minute rotation.

## Want someone to check it for you?

Start with the free [10-Minute Pre-Launch Security Checklist](https://shipreadycheck-dev.github.io/#free), or add the free [Ship-Ready Scan GitHub Action](https://github.com/shipreadycheck-dev/shipready-scan) to flag exposed keys on every push, before you launch.

Or have us look for you. The [Ship-Ready Check](https://shipreadycheck-dev.github.io/#pricing) reviews your repo for exposed keys, open databases, unverified payments and more, and sends a plain-English report.
