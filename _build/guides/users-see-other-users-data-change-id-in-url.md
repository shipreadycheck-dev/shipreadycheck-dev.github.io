---
title: Can users see each other's data by changing an ID in the URL? How to check
description: How to check whether a logged-in user can open another user's invoices, orders or files by editing an ID in your AI-built app, and how to fix it before launch.
slug: users-see-other-users-data-change-id-in-url
updated: 2026-11-09
---

# Can users see each other's data by changing an ID in the URL? How to check

Log in to your app and open something that belongs to you, like an invoice, an order or a saved document. Look at the address bar. If you see something like `/invoices/1042`, try changing it to `/invoices/1041`. If you can now see someone else's invoice, your app has one of the most common security bugs on the web.

This guide explains what the bug is, how to check for it in about ten minutes without reading code, and how to fix it.

## Why this matters

Security people call this an **Insecure Direct Object Reference**, or IDOR. The name is scary, but the idea is simple. [OWASP's guide to preventing it](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html) describes it as people reaching data by changing an ID in a URL or request, because the app never checks whether that data is theirs. Its own example is exactly the one above: changing `/users/123` to `/users/124`.

This is not only a small-app problem. In May 2019, a security journalist told First American Financial that its document-sharing site had this flaw. As [Axios reported](https://www.axios.com/2019/05/24/first-american-mortgage-data-exposure-leaked-885-million-files), the site sent people to an address containing a document number, and changing that number opened other people's files. About 885 million files dating back to 2003 were reachable, including bank account numbers, Social Security numbers and driver's license images. Axios noted there was no public evidence anyone had misused them. In 2021, the [SEC announced](https://www.sec.gov/news/press-release/2021-102) that First American agreed to pay $487,616 to settle charges over failures in its cybersecurity disclosure controls. The SEC's order said the company's own security staff had found the problem several months before the journalist did, and it had not been fixed.

One changed number. No hacking tools. That is why this bug is worth ten minutes of your time.

**Think of it like this:** your app is a coat check. You hand in your coat and get ticket 1042. A careful attendant looks at the ticket and at you. A careless one hands over whatever coat matches the number, so anyone who writes "1041" on a scrap of paper walks off with someone else's coat.

## Why AI-built apps hit this

When you ask an AI tool to "add a page that shows an invoice", the quickest working code takes the ID from the address and fetches that record. It works perfectly when you test it, because you only ever open your own invoices. Nothing on screen tells you the "is this yours?" check is missing.

Logging in doesn't fix it either. A login proves who someone is. It doesn't stop them asking for a record that belongs to someone else. Each request needs its own ownership check.

Random-looking IDs help a little, but they are not a fix. OWASP's guide says long random IDs are a useful extra layer, but the access check is still essential even when IDs are hard to guess. IDs can still end up in the wrong hands, for example through a shared link, and the app should block access when that happens.

## The 10-minute check

### 1. Make two test accounts

Sign up twice in your live app, as user A and user B. Use different browsers, or a normal window and a private window, so you can stay logged in as both.

### 2. Create something as user A

As user A, create one of everything your app stores per user: a project, an order, a note, an uploaded file, a profile. Open each one and copy the page address.

### 3. Open those addresses as user B

Paste each of user A's addresses into user B's browser. You should get an error, a "not found" page, or be sent away. If user B can see user A's data, you've found the bug.

### 4. Try neighboring numbers

If your IDs are plain numbers, change them up or down by one while logged in as user B. Any record that isn't user B's should be blocked.

### 5. Don't forget actions, not just pages

The same bug hides in edit, delete, download and export buttons. OWASP's guide recommends testing every operation that uses an ID: read, create, update, delete, export and admin actions. Also check what's sent behind the scenes. In Chrome, right-click, choose **Inspect**, open the **Network** tab, and click around as user A. Requests with IDs in them, like `/api/orders/1042`, are the ones to test. If you're not comfortable replaying those requests, the prompt below lets your coding agent do the reading.

Only test your own app, with your own test accounts.

### 6. Ask your coding agent to audit it

Paste this into Cursor, Claude Code, Lovable, Bolt or whatever you build with:

> List every page, API route and server function in this app that takes an ID (in the URL, query string, request body or form) and uses it to read, update, delete, download or export a record or file. For each one, show me the exact code that checks the record belongs to the logged-in user, or say clearly that there is no such check. Also tell me where the app gets the current user's ID: from the login session on the server, or from something the browser sends. Do not change anything yet.

Read the answer yourself. If it says "all routes are protected", ask it to show the exact line that does the check for each one.

## How to fix it

The core rule is "find this record, but only if it belongs to the person asking." In database terms, the lookup includes the owner. For example:

```sql
-- Risky: returns any invoice to anyone who asks for it
select * from invoices where id = $1;

-- Safer: returns the invoice only if it belongs to the logged-in user
select * from invoices where id = $1 and user_id = $2;
```

Here `$2` must be the user ID from the server's login session. Then work through these steps:

1. **Check ownership on the server, on every request.** Every page and API route that takes an ID should look up the record the safer way shown above.

2. **Never trust a user ID sent by the browser.** OWASP's guide recommends taking the current user from the session, not from the request. A hidden form field like `user_id=57` can be edited by anyone.

3. **Cover every action.** Apply the same check to edit, delete, download and export, not just the view page.

4. **If you use Supabase or Firebase directly from the browser,** your database rules do this job. Read our [Supabase RLS check](supabase-rls-check.html) or [Firebase rules check](firebase-security-rules-test-mode.html) and make sure each rule ties data to its owner.

5. **Watch your server code that uses a Supabase secret key.** [Supabase's docs](https://supabase.com/docs/guides/getting-started/api-keys) say secret keys, including the older `service_role` key, bypass every Row Level Security policy. They're meant for servers and APIs that run their own authorization checks. So if a server route uses one, that route must check ownership itself.

6. **Use random IDs as an extra layer.** Long random IDs (like UUIDs) make guessing harder. They don't replace the check.

7. **Retest with your two accounts.** Repeat steps 3 to 5 of the 10-minute check after every fix. Then ask your coding agent to add an automated test that logs in as user B, requests user A's record, and expects it to be blocked, so the bug can't quietly come back.

If you find the bug in a live app with real users, fix it first. Then check your logs, if you have them, for one account requesting many records it doesn't own.

## Want someone to check it for you?

The free [10-Minute Pre-Launch Security Checklist](https://shipreadycheck-dev.github.io/#free) includes this exact check (number 7) plus nine others, with a prompt for each one.

Or have us look for you. The [Ship-Ready Check](https://shipreadycheck-dev.github.io/#pricing) reviews your repo for missing ownership checks, open database rules, exposed keys, unverified payments and more, and sends a plain-English report within 24 hours. From $29.
