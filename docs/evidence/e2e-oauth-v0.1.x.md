# End-to-end check after 0.1.0 (OAuth sign-in, app tool call, skills session)

Run 2026-11-17 against Hermes Agent v0.23.1 and the plugin at `505892ab` (the commit the catalog pins).
The 0.1.0 release listed two things as not observed. This file records what was observed since, and
what still was not.

## Result in one table

| Item | Status |
|---|---|
| Install from the catalog entry by bare name, pinned commit | Observed |
| Model-driven session that loads a plugin skill and calls an `axiom_lite_*` tool | Observed (skill `lite`, tool `axiom_lite_macros`) |
| Connector discovery still live (both metadata documents 200, unauthenticated `POST /mcp` 401) | Observed again |
| Full OAuth sign-in in a browser | **Not observed** |
| An app tool call through Hermes after that sign-in | **Not observed** |
| Model-driven session using `coach-desk` or `my-plan` against a signed-in app | **Not observed** (needs the sign-in) |

## 1. Catalog install

In a throwaway `HERMES_HOME`:

```
$ hermes plugins install hermes-axiom-coach --enable --yes-deps
hermes-axiom-coach [community] pinned @ 505892ab
✓ Plugin hermes-axiom-coach enabled.
$ git -C $HERMES_HOME/plugins/hermes-axiom-coach rev-parse HEAD
505892ab32ca9c1787656df6a227069e19da7bc7
```

## 2. Model-driven session with a skill and a Lite tool

A one-shot session limited to the plugin's toolset and the skills toolset
(`hermes chat --query-file q.txt --oneshot -Q -t axiom-coach,skills`). The model:

1. called `skill_view` on `hermes-axiom-coach:lite` and got the bundled skill back,
2. called `axiom_lite_macros` with a fictional person's inputs and five "no" health answers,
3. got `{"blocked": false, "macros": {"calories": 2290, "proteinG": 176, "fatG": 64, "carbsG": 253}, ...}`,
4. answered with the targets and the general-education line the skill requires.

Transcript excerpt: `skills-session-v0.1.x.txt`. The session ran in an installed Hermes home that has
model credentials, because a throwaway home has none; the plugin was installed there for the run and
removed afterwards (config compared byte for byte before and after).

## 3. Connector endpoints, rechecked

```
GET  /.well-known/oauth-protected-resource      200
GET  /.well-known/oauth-authorization-server    200
POST /mcp (no token)                            401
```

## 4. Why the sign-in was not completed

The app's authorize page offers two ways in, and both end with a secret typed into the page:

- **Email and a 6-digit code.** Read from the app's source: this path looks up *client* accounts only.
  A coach's email gets "No client account uses that email."
- **Paste a connector code.** This is the coach path. The code is made on the app's AI screen, which
  itself needs an app sign-in (another emailed code).

The agent that ran this check may not type a password, a one-time code or a token into a page; those
go only through a credential vault a person fills. The vault held no entry for the app, and the run
was unattended, so nobody could fill one. The sign-in was not attempted, no code was requested and
no token was created.

A test coach account with no real clients was identified for the next attempt (two candidates on the
hosted copy; one has demo programs to list). Nothing was created or changed in the app.

## 5. What closes the gap

One attended step: a person saves the test coach's connector code into the credential vault (masked
prompt), or signs in on the authorize page themselves. After that, unattended:
`hermes mcp login axiom-coach` in a throwaway home, one read-only tool call (list programs), one
`coach-desk` session, then the token is revoked and the throwaway home deleted.

## 6. Finding to fix in the docs

`README.md` says to sign in "with your app email and the emailed code, or paste a connector code".
From the app's source, the email path is for self-serve clients; a coach has to paste a connector
code. The setup command already says this; the README does not. Source-read only, not yet seen on the
page. Proposed README wording for 0.1.1: "self-serve: your app email and the emailed code; coach:
paste a connector code made on the app's AI screen".

## Proposed known_issues text for the catalog entry (0.1.1)

> Observed: catalog install, and a model-driven session that loads a bundled skill and calls a Lite
> tool. Not observed: a full OAuth sign-in followed by an app tool call, and a model-driven session
> using coach-desk or my-plan against a signed-in app. Hermes's OAuth discovery, client registration
> and PKCE authorize request against the app's connector were observed.
