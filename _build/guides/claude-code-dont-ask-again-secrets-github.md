---
title: The Claude Code "don't ask again" leak: how your agent's memory can expose passwords
description: Researchers found passwords and keys saved by Claude Code's "don't ask again" approvals in public GitHub repos. What happened, why, and how to check yours.
slug: claude-code-dont-ask-again-secrets-github
updated: 2026-11-12
type: field-notes
---

# The Claude Code "don't ask again" leak: how your agent's memory can expose passwords

Most founders think of a secret as safe once it is out of the code. New research this week is a reminder that your coding agent keeps notes too. If you once typed a password into a command it ran, that password may now live in one of those notes.

## What happened

When Claude Code wants to run a command, it asks for permission. One of the options is "Yes, and don't ask again." According to [Claude Code's settings documentation](https://code.claude.com/docs/en/settings), choosing it saves that approval as a rule in a file inside your project called `.claude/settings.local.json`.

Researchers at the security company Apiiro looked at what ends up in that file. As [The Hacker News](https://thehackernews.com/2026/11/claude-codes-dont-ask-again-file.html) reports, the saved rule is the full approved command. If the command contained a password or token, the secret is stored in plain text. Apiiro found 104,185 copies of the file in public GitHub repositories. Of those, 1,122 contained at least one secret, for 1,379 distinct secrets in total. More than a third could open databases directly, including 379 database passwords.

Counting older versions in git history, shared settings files and saved chat logs, the total rose to 2,539 secrets across 1,994 repositories. Popular scanners missed some of them. The Hacker News reports that neither Gitleaks nor TruffleHog flagged 215 of the 1,122 files. Of 16 coding agents Apiiro compared, Claude Code was the only one confirmed to save the full approved command in a project file by default.

[iTWire](https://itwire.com/business-it-news/security/claude-code-approval-files-found-exposing-company-secrets-on-github-says-apirro-researchers) notes the researchers did not test whether the secrets still worked, so this shows exposure, not confirmed break-ins. One notified company did confirm its key was live.

Anthropic's documentation says Claude Code keeps this file out of git by adding it to your computer's global git ignore list the first time it writes the file. The Hacker News points out that this protection stays on that one computer and never goes into the project's own `.gitignore`. Per [Cybernews](https://cybernews.com/security/ai-agents-leaking-secrets-on-github/), Anthropic's Boris Cherny said on Hacker News that the team is "looking into what we can do to prevent this," and argued that the leaked files must have been created by hand and then committed. He also recommended turning on GitHub's secret scanning.

## Why AI-built apps keep hitting this

The usual advice about secrets is "keep them in a `.env` file and never commit it." The gap is that agents create new files that hold secrets, and nobody thinks of them as secret files.

A common path: your agent can't connect to the database, so you paste the connection string, password and all, into the chat. The agent runs a command with it. You click "don't ask again" to stop the prompts. The secret is now saved in a file inside your project. Whether it stays private depends on a safety net that lives on one computer. If the file was created by hand, copied to another machine, or already tracked by git, that net isn't there, and the next push can carry it to GitHub. In half of the affected repos, the file had been there for at least 217 days.

The insight most people miss: a secret you hand your agent can end up in a file in your project. Your agent's memory is part of your codebase, and it deserves the same care as your `.env`. "Don't ask again" saves a whole command, not just a permission.

## Check your own app in 5 minutes

1. **Look for the folder on GitHub.** Open your repository on GitHub and look for a folder named `.claude`. Inside it, check for `settings.local.json` and `settings.json`.
2. **Read what's inside.** `settings.json` is meant to be shared with your team, but neither file should ever hold a secret. Open each one. Look for anything that resembles a password, a token, a long random string, or a web address with a username and password in it. Normal entries look like short commands such as running tests.
3. **If you find a secret, rotate it first.** Change the password or create a new key at the service it belongs to, then revoke the old one. Deleting the file does not undo the leak, because old versions stay in git history and in any copies of your repo.
4. **Then clean up.** Remove the secret from the file on your computer, stop tracking `settings.local.json` in git, and add it to your project's `.gitignore` so the protection travels with the project.
5. **Change the habit.** Don't paste passwords or keys into the chat. Store them as environment variables and have the agent refer to them by name.

Then ask your coding agent for a second look:

> Check this project and its full git history for `.claude/settings.local.json`, `.claude/settings.json` and any other agent settings or chat log files. Tell me whether any of them is tracked by git, whether `.claude/settings.local.json` is listed in this project's `.gitignore`, and whether any version of these files ever contained a password, token, API key or connection string. List what you find and which service each secret belongs to. Do not change anything yet.

If anything turns up, treat it as already public and follow our [exposed API keys guide](exposed-api-keys.html).

## The takeaway

Your coding agent remembers what you approve, and those memories are files. Keep secrets out of the chat, add `.claude/settings.local.json` to your project's `.gitignore`, and check the `.claude` folder before you push. It takes minutes and closes a leak that scanners can miss.

## Want someone to check it for you?

Start with the free [10-Minute Pre-Launch Security Checklist](https://shipreadycheck-dev.github.io/#free), or add the free [Ship-Ready Scan GitHub Action](https://github.com/shipreadycheck-dev/shipready-scan) to flag exposed keys on every push.

Or have us look for you. The [Ship-Ready Check](https://shipreadycheck-dev.github.io/#pricing) reviews your repo for exposed keys, open databases, unverified payments and more, and sends a plain-English report.
