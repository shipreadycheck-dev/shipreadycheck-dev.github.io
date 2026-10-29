---
title: The AGENTS.md attack: why your coding agent should never run in Downloads
description: Researchers found a planted AGENTS.md file that tried to make a coding agent install malware. What happened, why it matters, and how to check your setup today.
slug: agents-md-downloads-folder-coding-agent-hijack
updated: 2026-10-29
type: field-notes
---

# The AGENTS.md attack: why your coding agent should never run in Downloads

Most founders think of their coding agent as a helper that does what they type. This week's research is a reminder that it also does what the files around it say. If one of those files was written by a stranger, the stranger is giving the orders.

## What happened

Coding agents like OpenAI's Codex and Anthropic's Claude Code automatically read instruction files, such as AGENTS.md or CLAUDE.md, from the folder you start them in. These are plain text notes like "use this test command" or "follow this style." The agent treats them as instructions from you.

According to [BleepingComputer](https://www.bleepingcomputer.com/news/security/ai-coding-agents-hijacked-using-agentsmd-file-in-downloads-folder/), researchers at Forever Security, a company that monitors risks from AI agents, found a malicious AGENTS.md file in a customer's Downloads folder. A coding agent there had tried to install a rogue npm package called "function-color." The researchers could not determine how the file got onto the machine. They noted that browsers save files to Downloads by default and said a web page could drop a file there.

The researchers then tested the idea. Using a harmless stand-in that only opened the calculator app, they got Codex to run it in about 90% of attempts. [Help Net Security](https://www.helpnetsecurity.com/2026/10/26/ai-coding-agents-malware-openai-codex/) reports that the changes the file made to Codex's settings applied to the whole computer, so later sessions in other projects would run the attacker's command too. It also reports that npm has since removed the package.

Claude Code was affected differently. The researchers wrote a CLAUDE.md file modeled on the one they found and found Claude much harder to trick. Still, in their tests it sometimes accepted a settings change that sent its traffic to a server the attacker controlled, which could expose the user's login token and, in some tests, lead to code running on the machine.

Neither article mentions a CVE or reports a fix from OpenAI or Anthropic. The researchers told BleepingComputer the agents are working as designed, and that "there is nothing here for OpenAI or Anthropic to patch."

## Why AI-built apps keep hitting this

The old rule was simple: don't run programs you don't trust. Text files were safe to have lying around. With coding agents, that rule quietly broke. A text file in the right folder now carries the same authority as you typing at the keyboard. Help Net Security quotes the researchers putting it bluntly: "Markdown is the new executable."

Founders who build with AI are especially exposed to this, for three reasons.

First, we use our agents for everything, not just code. "Sort my Downloads folder" or "look at the file I just downloaded" are natural requests, and Downloads is exactly where files from strangers land. Help Net Security reports that, in Forever Security's data, about half of its customers run a coding agent in Downloads.

Second, we copy a lot of other people's work. Starter templates, sample repos and boilerplate from a tutorial can all arrive with instruction files we never open.

Third, we tend to click "allow" to keep things moving. Approval prompts and sandboxes are the safety net when an instruction file goes bad, and they only work if they stay on.

The insight most people miss: where you start your agent is a security decision. The folder sets who gets to give it orders.

## Check your own app in 5 minutes

1. **Notice where you start your agent.** Open it inside one specific project folder. Never start it in Downloads, your Desktop or your home folder.
2. **Find instruction files you didn't write.** In each project, look for files named AGENTS.md or CLAUDE.md, including in the top folder and in subfolders. Open each one in a plain text editor and read it before your agent does. They are short and written in plain English.
3. **Watch for red flags.** Be suspicious of any instruction file that asks the agent to install a package, change its own settings, send requests to a server or address, or turn off approval prompts or the sandbox. Normal ones talk about code style, tests and project structure.
4. **Keep the safety net on.** Leave approval prompts and sandbox protections enabled. Treat any instruction that asks you to bypass them as a warning sign, not a shortcut.
5. **If you find a planted file, act.** Following the researchers' advice, assume your agent's login token has leaked and replace it. If "function-color" was ever installed on a machine, treat that machine as compromised and get help cleaning it up.

Then ask your coding agent for a second look, from inside the project folder:

> List every AGENTS.md, CLAUDE.md or similar agent instruction file in this project and summarize what each one asks you to do. Also tell me whether any instruction or agent setting installs packages, points to an outside server or address, or turns off approval prompts or the sandbox. Do not change anything yet.

Read the answer yourself. If anything in it surprises you, stop and look closer before you run another task.

## The takeaway

Your coding agent follows the notes in its folder as if you wrote them. Start it only in project folders you trust, read any instruction file you didn't write, and keep approvals on. That habit takes seconds and closes off a whole class of attack.

## Want someone to check it for you?

Start with the free [10-Minute Pre-Launch Security Checklist](https://shipreadycheck-dev.github.io/#free), or add the free [Ship-Ready Scan GitHub Action](https://github.com/shipreadycheck-dev/shipready-scan) to flag exposed keys on every push.

Or have us look for you. The [Ship-Ready Check](https://shipreadycheck-dev.github.io/#pricing) reviews your repo for exposed keys, open databases, unverified payments and more, and sends a plain-English report.
