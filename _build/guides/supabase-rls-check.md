---
title: Is your Lovable or Supabase app leaking its database? A 5-minute RLS check
description: How to check whether Row Level Security is protecting your Supabase tables in an app built with Lovable, Bolt or Cursor, and how to fix it before launch.
slug: supabase-rls-check
updated: 2026-10-15
---

# Is your Lovable or Supabase app leaking its database? A 5-minute RLS check

If you built your app with Lovable, Bolt, Cursor or Claude Code and it uses Supabase, there is one setting that decides whether strangers can read your users' data. It is called **Row Level Security**, or RLS. This guide shows you how to check it in about five minutes, without reading any code.

## Why this matters

Your app's website contains a Supabase key called the **anon key**. That's normal: it is meant to be public, and it is how your site talks to the database. The only thing stopping someone from using that key to read or change every row in your database is RLS.

**Think of it like this:** the anon key is the front door of an apartment building. Everyone has it. RLS is the lock on each apartment. With RLS off, anyone who walks in can open every apartment.

This is not a rare edge case. In 2025, researchers scanned 1,645 apps built with Lovable and found 170 of them exposing data through missing or broken RLS rules. It was catalogued as [CVE-2025-48757](https://www.superblocks.com/blog/lovable-vulnerabilities). In early 2026, the AI social network Moltbook was [found exposing its whole database](https://www.getautonoma.com/blog/vibe-coding-failures) through the same mistake, days after launch.

## Why AI tools get this wrong

AI coding tools usually create your tables with SQL. A table created with SQL has RLS **off** unless the same script turns it on. The app works perfectly in testing either way, so nothing tells you anything is wrong.

There's a second, sneakier version: RLS is on, but the rule says `USING (true)`. That rule means "let everyone in", so RLS is technically enabled while doing nothing.

## The 5-minute check

### 1. Look for "RLS disabled" in the dashboard

Open your project in Supabase and go to the **Table Editor**. Click through each table. If any table that holds user data shows **RLS disabled**, it is readable by anyone with your public key.

Supabase also has a **Security Advisor** (under Database or Advisors, depending on your dashboard version) that flags tables without RLS. Run it and read every warning.

### 2. Read the rules on tables that have RLS on

For each table, open its policies. You are looking for two red flags:

- A policy whose condition is just `true`
- A policy that doesn't mention `auth.uid()` on a table where each row belongs to a user

A healthy rule for a table of notes looks like this:

```sql
create policy "own notes" on public.notes
  for select using (auth.uid() = user_id);
```

### 3. Ask your coding agent to audit it

Paste this into Lovable, Cursor, Claude Code or whatever you build with:

> List every Supabase table and whether Row Level Security is enabled. For each policy, show its USING and WITH CHECK clauses. Flag any table holding user data with RLS off, and any policy using `true`. Do not change anything yet.

Then read the answer yourself. Don't take "everything looks secure" as a final answer. Ask it to show you the policies.

### 4. Test it like an attacker would (optional)

Sign up as two test users in your app. Create something as user A. Log in as user B and try to see it, including by changing any ID in the page address. If user B can see user A's data, your rules are broken.

## How to fix it

For each table that holds user data:

1. Turn RLS on: `alter table public.your_table enable row level security;`
2. Add a policy for each action you actually use (select, insert, update, delete), each checking ownership with `auth.uid()`.
3. Replace any `USING (true)` policy on user data.
4. Test again with two users.

If you ever pasted your **service_role** key into the app's frontend code, rotate it in Supabase right away. That key skips RLS entirely, so no rule can protect you while it's public.

## Want a second pair of eyes?

The free [10-Minute Pre-Launch Security Checklist](https://shipreadycheck-dev.github.io/#free) covers RLS plus nine other checks, with a prompt for each one.

Or have us check it for you. The [Ship-Ready Check](https://shipreadycheck-dev.github.io/#pricing) reviews your repo for exposed keys, RLS gaps, unverified payments and more, and sends a plain-English report within 24 hours. From $29.
