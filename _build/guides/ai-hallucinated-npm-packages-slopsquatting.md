---
title: Did your AI coding tool install a fake npm package? How to check for slopsquatting
description: AI coding tools sometimes invent package names, and attackers register them. How to check the packages in your AI-built app are real, and what to do if one isn't.
slug: ai-hallucinated-npm-packages-slopsquatting
updated: 2026-11-16
---

# Did your AI coding tool install a fake npm package? How to check for slopsquatting

When Cursor, Claude Code, Bolt, Lovable or Replit adds a feature, it often installs extra code from the internet called **packages** (or dependencies). Most of them are real, popular and fine. But AI tools sometimes suggest a package name that sounds right and doesn't exist. If someone registers that name first, your app installs their code instead. This guide shows you how to check every package in your app is the one you meant to get, in about fifteen minutes.

## Why this matters

This problem has a name: **slopsquatting**. It works like typosquatting, except the "typo" comes from the AI, not from you.

It isn't rare. A study presented at USENIX Security 2025 tested 16 code-writing AI models on Python and JavaScript tasks. Socket's [write-up of the research](https://socket.dev/blog/slopsquatting-how-ai-hallucinations-are-fueling-a-new-class-of-supply-chain-attacks) reports that 19.7% of the packages the models recommended did not exist, with over 205,000 unique made-up names. Commercial models did better than open-source ones (5.2% versus 21.7% on average), but none scored zero.

The made-up names are also predictable. When researchers reran the same prompts ten times, 43% of the fake names came back every single time. That's what makes this attack practical: an attacker can ask the AI the same questions, collect the names it invents, and register them.

Real cases already exist:

- In early 2024, researcher Bar Lanyado noticed AI models kept suggesting a Python package called `huggingface-cli`, which wasn't the real install name. He uploaded an empty placeholder under that name, and it got over 30,000 downloads in three months, according to [Aikido's summary](https://aikido.dev/blog/slopsquatting-ai-package-hallucination-attacks).
- In January 2026, Aikido researcher Charlie Eriksen found an invented npm name, `react-codeshift`, inside AI-generated "agent skill" files that had been copied into more than 200 repositories. He [registered the name himself](https://aikido.dev/blog/agent-skills-spreading-hallucinated-npx-commands) so an attacker couldn't, and it still got a few downloads a day, apparently from coding agents following those instructions.

A malicious package doesn't need you to run it on purpose. Aikido notes that some run a script the moment they're installed, and try to steal API keys, cloud tokens and other credentials from the machine.

**Think of it like this:** you ask a new assistant to order printer ink, and they confidently write down a supplier that doesn't exist. Normally the order just fails. But if a scammer has set up a shop with that exact name, the order goes through, and the box that arrives isn't ink.

## Why AI-built apps hit this

Two things make it more likely in vibe-coded apps. First, the AI often installs packages for you, so no human reads the name before it runs. Second, people tend to trust a name that looks official, like `something-cli` or `react-something`. The Cloud Security Alliance's [research note on slopsquatting](https://labs.cloudsecurityalliance.org/research/csa-research-note-slopsquatting-ai-supply-chain-20260419/) points out that agents can resolve and install packages on their own, so nobody may notice a suspicious name at all.

## The 15-minute check

### 1. Find your package list

In your project, open the file called `package.json`. Look for the sections named `dependencies` and `devDependencies`. Each line is a package name and a version. If you see a file called `package-lock.json` next to it, that's your lockfile, which records the exact versions that were installed.

If your project uses Python, the equivalent is usually `requirements.txt` or `pyproject.toml`. The same idea applies.

### 2. Mark the names you don't recognize

You don't need to know every package. Big, well-known ones like `react`, `next`, `express`, `stripe` or `@supabase/supabase-js` are not what this check is looking for. Circle anything that:

- you've never heard of,
- looks like two real names mashed together,
- has a name very close to a popular package, or
- was added recently, in a change you didn't ask for.

### 3. Check each suspicious package is real and established

For each name you circled, you want three answers: does it exist, how long has it existed, and who publishes it. npm's own command `npm view` shows a package's details, including when each version was published, according to the [npm view docs](https://docs.npmjs.com/cli/v12/commands/npm-view). npm's [malware reporting page](https://docs.npmjs.com/reporting-malware-in-an-npm-package) also shows `npm owner ls <package-name>`, which lists who maintains it.

Warning signs:

- npm can't find the package at all. Your code is asking for something that doesn't exist, and anyone could register it tomorrow.
- It was first published very recently, especially in the last few months.
- The maintainer or linked source code doesn't match the project it claims to be. A package that says it's from a big company but is published by an unknown account is a red flag.

Aikido's advice is to verify the publisher, not just the name or download count.

### 4. Ask your coding agent to audit it

Paste this into Cursor, Claude Code, Bolt or whatever you build with:

> List every package in package.json (dependencies and devDependencies) and any packages the code runs with npx, pnpm dlx, yarn dlx or bunx, including in docs, scripts and agent skill or rules files. For each one, run `npm view <name>` and `npm owner ls <name>` and tell me: does it exist on npm, when was it first published, who maintains it, and what is its repository URL. Flag any package that does not exist, was first published in the last 90 days, has a name close to a better-known package, or whose maintainer does not match the project it claims to be. Do not install, remove or change anything yet.

Read the answer yourself. If the agent says everything is fine, ask it to show you the raw output for the packages you circled.

## How to fix it

1. **Replace anything that doesn't exist or looks wrong.** Ask your agent what the package was supposed to do, then find the real, established package for that job and check it the same way before switching. For example, Aikido's fix for the `react-codeshift` case was to use the real `jscodeshift` or `react-codemod` instead.
2. **Commit your lockfile.** npm's [package-lock.json docs](https://docs.npmjs.com/cli/v12/configuring-npm/package-lock-json) say it is intended to be committed, so every install and deploy uses the same dependency tree and any change shows up in your history.
3. **Don't let your agent install packages without asking.** Add a line to your agent's rules file such as: "Never install a new package without telling me its exact name and why, and checking it exists on npm with an established publisher." Then review each new package before you approve it.
4. **Check copied commands too.** Install commands in READMEs, tutorials and agent skill files can carry invented names. Check them before you run them.
5. **If you installed something malicious, treat your machine and keys as exposed.** Remove the package, then rotate (replace) the API keys, tokens and passwords that were on that computer or in that project. If you're sure a package is malware, npm has a [Report malware](https://docs.npmjs.com/reporting-malware-in-an-npm-package) option on the package page.

None of this makes you immune. It just means a made-up name has to get past you, not only past the AI.

## Want someone to check it for you?

The free [10-Minute Pre-Launch Security Checklist](https://shipreadycheck-dev.github.io/#free) walks through the most common launch mistakes, with a copy-paste prompt for each one.

Or have us look for you. The [Ship-Ready Check](https://shipreadycheck-dev.github.io/#pricing) reviews your repo for suspicious dependencies, exposed keys, open database rules, unverified payments and more, and sends a plain-English report within 24 hours. From $29.
