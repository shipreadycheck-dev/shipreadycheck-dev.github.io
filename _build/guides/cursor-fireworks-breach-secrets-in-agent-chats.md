---
title: The Cursor breach root cause: why secrets pasted into AI chats don't stay there
description: Cursor traced its malicious extension incident to a vendor's leaked key and agent chat logs holding unredacted credentials. What happened and how to check yours.
slug: cursor-fireworks-breach-secrets-in-agent-chats
updated: 2026-11-19
type: field-notes
---

# The Cursor breach root cause: why secrets pasted into AI chats don't stay there

Two weeks ago we wrote about the [fake Claude Code extension in Cursor](cursor-claude-code-extension-backdoor.html). This week Cursor explained how the attacker got in. The answer is a lesson for anyone who has ever pasted a password into a chat with a coding agent.

## What happened

On November 13, Cursor published a [security incident update](https://cursor.com/blog/security-incident-update). It says an attacker obtained an access key that Cursor had issued to Fireworks, an AI company Cursor worked with. In Cursor's words, "the key was exposed by Fireworks." [Dark Reading](https://darkreading.com/application-security/cursor-malicious-claude-code-extension-third-party-breach) reports that Fireworks said a cloud provider hosting some of its systems had a security incident on October 23, in which attackers obtained API keys and access tokens.

The attacker used the Cursor key to copy data from a read-only storage bucket. Cursor says that bucket held coding agent traces, which are records of agent sessions, mostly from 2025. They came from sessions that were not in Privacy Mode, which Cursor was permitted to use for model training.

Here is the key detail. Some of those traces contained credentials that had not been redacted. According to [The Hacker News](https://thehackernews.com/2026/11/stolen-fireworks-ai-key-led-to-cursor.html), the attacker used them to reach some of the outside software tools Cursor uses. From there they got archived non-production code, limited support data and emails, and credentials that users had sent to Cursor's support team. [BleepingComputer](https://bleepingcomputer.com/news/security/cursor-confirms-security-breach-led-to-malicious-claude-code-extension) reports that a stolen credential is also what let the attacker place the malicious Claude Code extension in the cache behind Cursor's marketplace on October 29.

Cursor says traces from fewer than 0.05% of non-Privacy Mode users were exposed, and API credentials for fewer than 0.01% of customers. Affected users were notified directly, and team admins received lists of keys to rotate. Cursor says that if you were not notified, your data was not in the affected traces, and that prompts and code from Privacy Mode sessions were not affected. It has since moved all inference off Fireworks and rotated exposed credentials.

## Why AI-built apps keep hitting this

Most founders treat the chat with their coding agent like a private conversation. Paste in the database password so it can fix the connection, paste in the Stripe key so it can test checkout, move on.

It is closer to emailing the secret to a company. That message is stored as data. Depending on your settings, it may be kept, used for training, and handled by other companies the tool works with. Redaction tools try to strip secrets out, and this incident shows that some slip through. Then the security of your password depends on a chain of companies you have never heard of, and the weakest link in that chain is the one that matters.

None of this means Cursor is uniquely risky. Any AI tool you chat with may keep a record of what you send it, depending on its settings. The insight most people miss: a secret you paste into any AI chat is a new copy of that secret, and you don't control where copies go. The same goes for a key sent in a support ticket, which was also on the list of exposed data here.

The fix is mostly a habit. Your agent rarely needs to see the secret itself. It needs to know the secret exists and what it is called.

## Check your own app in 5 minutes

1. **Search your inbox for a Cursor security email.** If you got one, rotate every key it lists first. If you used the Claude Code extension in Cursor around October 29, follow the steps in [Cursor's security notice](https://cursor.com/blog/claude-code-extension-security-notice).
2. **Turn on Privacy Mode if you use Cursor.** Per [Cursor's help page](https://cursor.com/help/security-and-privacy/privacy), open settings with Cmd+Shift+J on Mac or Ctrl+Shift+J on Windows, choose General, and switch Privacy Mode on. Other AI tools have similar data settings. Check each one you use.
3. **Make a list of secrets you have pasted into any AI chat.** Think about every tool, not just Cursor: your coding agent, your app builder's chat, general chatbots and support tickets. Database passwords, payment keys and AI provider keys matter most.
4. **Rotate anything on that list that still works.** Create a new key or password at the service it belongs to, update your app's hosting settings, then revoke the old one. Changing a privacy setting today does not undo a secret you already sent.
5. **Change the habit.** Store secrets as environment variables in your hosting settings or a local `.env` file that is not committed to git. When your agent needs one, tell it the name, such as `DATABASE_URL`, never the value.

Then ask your coding agent to check the project for secrets written out in full:

> List every place in this project where a password, API key, token or database connection string is written out directly instead of being read from an environment variable. Include code, config files, notes, logs and any files you or other tools have created. For each one, tell me what service it belongs to. Do not change anything yet, and do not print the secret values themselves.

If anything turns up, follow our [exposed API keys guide](exposed-api-keys.html).

## The takeaway

Cursor's breach started with one vendor's leaked key and spread through credentials people had pasted into agent sessions. Treat every AI chat as a place secrets can be copied, not a private room. Keep secrets in environment variables, refer to them by name, and rotate anything you have already pasted.

## Want someone to check it for you?

Start with the free [10-Minute Pre-Launch Security Checklist](https://shipreadycheck-dev.github.io/#free), or add the free [Ship-Ready Scan GitHub Action](https://github.com/shipreadycheck-dev/shipready-scan) to flag exposed keys on every push.

Or have us look for you. The [Ship-Ready Check](https://shipreadycheck-dev.github.io/#pricing) reviews your repo for exposed keys, open databases, unverified payments and more, and sends a plain-English report.
