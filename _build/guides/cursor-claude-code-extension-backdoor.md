---
title: The fake Claude Code extension in Cursor: when the right name is the attack
description: A tampered Claude Code extension in Cursor's marketplace planted a backdoor on developer machines. What happened, why it matters, and how to check yours today.
slug: cursor-claude-code-extension-backdoor
updated: 2026-11-05
type: field-notes
---

# The fake Claude Code extension in Cursor: when the right name is the attack

Most founders decide whether to trust an extension once, when they install it. After that, updates arrive quietly in the background. This week showed what happens when one of those quiet updates is not what it claims to be.

## What happened

On October 29, Cursor found a malicious version of the Claude Code extension (`anthropic.claude-code`) in its own extension marketplace. According to [Cursor's security notice](https://cursor.com/blog/claude-code-extension-security-notice), versions 2.1.312 and 2.1.313 for Windows and macOS were available from about 2:27am to 1:35pm Pacific time that day. Cursor states these versions "were not developed by Anthropic."

The notice says the tampered code collected details about the computer and sent them to the attacker's server. It added the attacker's SSH key, labeled `svc-telemetry`, to the user's list of keys allowed to log in. It then tried to turn on remote login and open a hidden connection back to the attacker, and set itself up to keep retrying after a restart. Turning on remote login needs admin rights, so Cursor says that step likely failed on most machines. The key and the restart setup were written anyway.

[Microsoft's analysis](https://www.microsoft.com/en-us/security/blog/2026/10/30/inside-malicious-claude-code-branded-cursor-extension-persistent-ssh-backdoor/) adds that the code also collected the names, though not the values, of environment variables containing words like KEY, TOKEN or SECRET. Microsoft found no evidence the package reached the official Visual Studio Marketplace or npm.

[The Hacker News](https://thehackernews.com/2026/10/official-claude-code-vs-code-extension.html) reports that Cursor said at most 5,000 users were affected and that it will contact them directly. Cursor removed the bad versions, shut its marketplace down while it rotated keys and rebuilt it, and worked with the hosting provider to take the attacker's server offline. The current clean version is 2.1.314. How the attacker got the tampered extension into Cursor's marketplace has not been disclosed.

## Why AI-built apps keep hitting this

The extension had the right name and, according to The Hacker News, was published under Anthropic's publisher identity. Nothing about it looked wrong. That was the whole attack.

Here is the part most people miss: the name of an extension is not the same as where it came from. Editors like Cursor run their own marketplace. The same extension can be offered in more than one store, and each store is its own place where things can go wrong. Anthropic and Microsoft say the official channels were not affected. The copy in one store was.

Founders building with AI are especially exposed for three reasons.

First, we install a lot of AI extensions and plugins, often while trying a new tool on a busy afternoon. Each one is code with broad access to our computer.

Second, updates are automatic. You may have reviewed an extension the day you installed it. You did not review the update that arrived on a Thursday morning.

Third, our laptops hold the keys to our apps. Your OpenAI key, Supabase service key, Stripe secret key and GitHub login often live in files and settings on the same machine you code on. Even a list of their names tells an attacker what is worth going after.

So treat your editor as part of your app's security, not just a place to type. If your production keys live on your laptop, your laptop is part of production.

## Check your own app in 5 minutes

1. **Check your inbox.** Look for an email from Cursor about this extension. The Hacker News reports Cursor will contact affected users directly.
2. **Check the version.** Open Cursor, go to Extensions, and find Claude Code. It should be 2.1.314 or later. A newer version does not prove you were never on a bad one, so if Cursor was open on October 29, do the next step too.
3. **Run Cursor's one-line check.** On a Mac, open Terminal and paste the command shown below this list, taken from Cursor's notice. It only reads a file. On Windows, use the PowerShell command in [Cursor's notice](https://cursor.com/blog/claude-code-extension-security-notice).
4. **If the key is found, act in this order.** Run Cursor's remediation script for your system, linked in the notice. Cursor warns that uninstalling the extension may not remove everything, and suggests considering a full rebuild of the computer. Then, from a different computer you trust, replace every key and login that machine could reach: AI provider keys, database keys, payment keys and GitHub tokens. If this feels out of your depth, get help before you keep working on that machine.
5. **Trim your extensions.** Remove any editor extension you don't use every week. Fewer extensions means fewer updates you have to trust.

The Mac check from step 3:

```
grep -qs svc-telemetry ~/.ssh/authorized_keys && echo "svc-telemetry key found" || echo "No key found; machine not impacted"
```

Then ask your coding agent for a second look:

> Without making any changes, check this computer for signs of the malicious Claude Code extension versions 2.1.312 and 2.1.313 from Cursor's marketplace. Tell me which version of the anthropic.claude-code extension is installed in Cursor, whether ~/.ssh/authorized_keys contains a key labeled svc-telemetry, and whether a LaunchAgent named com.apple.sysmond.plist exists. Also list the names of environment variables on this machine that hold keys or tokens, so I know what I would need to rotate. Do not change anything yet.

Treat the answer as a lead, not a verdict. Cursor's own check and script are the source of truth.

## The takeaway

A trusted name in your editor's store is not a guarantee of what's inside the update. Run Cursor's check if you use it, keep fewer extensions, and keep your most powerful keys off the machine where you install things. Then one bad update is far more likely to cost you an afternoon than your app.

## Want someone to check it for you?

Start with the free [10-Minute Pre-Launch Security Checklist](https://shipreadycheck-dev.github.io/#free), or add the free [Ship-Ready Scan GitHub Action](https://github.com/shipreadycheck-dev/shipready-scan) to flag exposed keys on every push.

Or have us look for you. The [Ship-Ready Check](https://shipreadycheck-dev.github.io/#pricing) reviews your repo for exposed keys, open databases, unverified payments and more, and sends a plain-English report.
