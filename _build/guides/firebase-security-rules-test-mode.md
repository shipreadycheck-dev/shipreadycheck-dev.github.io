---
title: Is your Firebase database open to everyone? How to check your security rules
description: How to check whether Firebase Security Rules left in test mode are exposing your Firestore, Realtime Database or Storage in an AI-built app, and how to fix them.
slug: firebase-security-rules-test-mode
updated: 2026-11-02
---

# Is your Firebase database open to everyone? How to check your security rules

If your app uses Firebase and you built it with Cursor, Bolt, Claude Code, Replit or a similar tool, a short block of text called **Security Rules** decides who can read and change your data. This guide shows you how to read those rules and spot the open ones in about ten minutes, without being a developer.

## Why this matters

Your app talks to Firebase straight from the user's browser or phone. That is how Firebase is designed, and the config values in your app (including the Firebase `apiKey`) are not meant to be secret. What protects your data is the rules on the server.

When you create a Firestore database, Cloud Storage bucket or Realtime Database, Firebase asks you to pick a starting mode. **Locked mode** denies everyone. **Test mode** lets anyone in, so you can build without errors. Firebase's own [guide to insecure rules](https://firebase.google.com/docs/database/security/resolve-insecurities) warns that with open access, anyone who guesses your project ID can steal, modify or delete the data. Its [basic rules page](https://firebase.google.com/docs/rules/basics?hl=en) adds that once you deploy, your app is publicly accessible even if you haven't launched it yet.

**Think of it like this:** test mode is propping your shop's back door open while the shelves get stocked. That's fine on day one. If you forget about it, anyone walking by can take whatever is inside, and the shop looks completely normal from the front.

This mistake is common. In 2024, researchers scanned more than 5 million websites and found 916 with Firebase set up with no rules or broken rules. GitGuardian's [summary of that research](https://blog.gitguardian.com/misconfigurations-in-google-firebase-lead-to-over-19-8-million-leaked-secrets/) reports over 125 million user records exposed, including emails, phone numbers and billing details. In 2025, Website Planet researchers [reported publicly accessible Firebase databases](https://zendata.security/2025/05/25/massive-data-leak-exposes-passwords-of-1-8-million-users-through-misconfigured-firebase-servers/) behind more than 900 mobile apps, exposing data on over 1.8 million users.

## Why AI-built apps hit this

Coding tools are good at getting your app working. Locked rules make every read fail with a permission error, so the quickest way to "fix" that error is to open the rules up. The app then works perfectly in testing, and nothing on screen tells you the database is open to the whole internet.

There's a second trap. A rule that only checks whether someone is signed in looks safe but isn't. Firebase's docs explain that a rule like `request.auth != null` lets **any** signed-in user read and write everything. If anyone can create an account in your app, that rule protects almost nothing.

## The 10-minute check

### 1. Find your rules

Open your project in the Firebase console. Open **Firestore**, then click the **Rules** tab. In newer versions of the console, Firestore sits under **Databases & Storage**. If your app also uses **Realtime Database** or **Storage**, each one has its own Rules tab. Check every one you use.

If your project has a `firestore.rules`, `storage.rules` or `database.rules.json` file, those are your rules too. Keep in mind that deploying with the Firebase CLI overwrites what's in the console, so the file and the console should match.

### 2. Look for the red flags

Read each rule set. These are the patterns to worry about on anything that holds user data:

| Red flag | What it means |
|---|---|
| `allow read, write: if true;` | Anyone on the internet can read and change everything |
| `allow read, write;` (no condition) | Same: open to everyone |
| `".read": true` or `".write": true` | Realtime Database version of fully open |
| `if request.time < timestamp.date(...)` as the only condition | Open to everyone until that date |
| `if request.auth != null;` on its own | Any signed-in user can see and change every user's data |
| `match /{document=**}` with any of the above | The rule applies to your whole database |

If you see a date-based rule, don't relax just because the date is in the future. Until then, the data is open.

### 3. Compare with a healthy rule

A safer rule ties each piece of data to its owner. This example from Firebase's docs only lets a user read and write documents stored under their own user ID:

```
service cloud.firestore {
  match /databases/{database}/documents {
    match /some_collection/{userId}/{document} {
      allow read, write: if request.auth != null && request.auth.uid == userId
    }
  }
}
```

You don't need to understand every word. The key part is `request.auth.uid == userId`, which means "only the person this data belongs to."

### 4. Ask your coding agent to audit it

Paste this into Cursor, Claude Code, Bolt or whatever you build with:

> List every Firebase service this app uses (Firestore, Realtime Database, Storage) and show me the current security rules for each one. For every rule, explain in plain English who can read and who can write that data. Flag any rule that uses `if true`, has no condition, uses a `request.time` date, or only checks `request.auth != null`. Do not change anything yet.

Read the answer yourself. If it says "looks secure", ask it to show you the exact rules it checked.

### 5. Test with two accounts

Firebase's [rules guide](https://firebase.google.com/docs/firestore/security/get-started) describes a **Rules Playground** on the Rules tab that simulates requests. Note that it tests the rules in the editor, not the ones you have published, so make sure you're looking at your live rules.

For a real-world check, sign up as two test users in your app. Create something as user A, then log in as user B and try to see or edit it. If user B can, your rules are too loose.

## How to fix it

1. **Decide who should see each kind of data.** Usually it's "only the owner", sometimes "anyone can read, only the owner can edit."
2. **Replace open rules with owner-based ones.** Ask your coding agent to write rules using `request.auth.uid` for each collection, then read what it wrote before publishing. Firebase's [insecure rules guide](https://firebase.google.com/docs/database/security/resolve-insecurities) has examples for Firestore, Realtime Database and Storage, including mixed public and private data.
3. **Remove any date-based test mode rule** and any catch-all `match /{document=**}` that opens everything.
4. **Publish, then retest with two users.** Some screens may break because they relied on open access. Fix those by tightening the query or the rule for that one collection, never by opening the whole database again.
5. **If your data was open, assume someone may have looked.** Check for data you didn't create, and never store passwords in your own database. Firebase Authentication handles logins for you.

## Want someone to check it for you?

The free [10-Minute Pre-Launch Security Checklist](https://shipreadycheck-dev.github.io/#free) covers database rules plus nine other checks, with a prompt for each one.

Or have us look for you. The [Ship-Ready Check](https://shipreadycheck-dev.github.io/#pricing) reviews your repo for open database rules, exposed keys, unverified payments and more, and sends a plain-English report within 24 hours. From $29.
