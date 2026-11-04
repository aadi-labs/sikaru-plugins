---
name: sikaru-setup
description: Install the Sikaru CLI, sign up or sign in to Sikaru (from the CLI or as an agent through sikaru.ai/auth.md), get a default project, check access, get a project API key for SDK, server or CI use, and add credits. Use when the user wants to get started with Sikaru, create a Sikaru account, log in, or fix "missing credentials", 401, 403 or no-project errors.
---

# Set up Sikaru

Work through these steps in order. Stop at the first one that already passes.

## 1. Install the CLI

```sh
sikaru decision --help >/dev/null 2>&1 && echo ok
```

If that fails, install or upgrade:

```sh
curl -fsSL https://app.sikaru.ai/install.sh | sh
```

With Node.js 20+ (any platform, including Windows): `npm install -g @aadi-labs/sikaru-cli`.

Older builds lack the `decision` and `credits` groups. If `sikaru decision --help`
still fails after installing, the newer CLI may be on a different `PATH` entry.
Check `which -a sikaru`. If the installer doesn't work, tell the user and point them to
https://github.com/aadi-labs/sikaru-clients. Don't build or download binaries from
anywhere else.

## 2. Sign up or sign in

One flow covers both. A new user gets an organization named after them (for example
"Ada's Team") and a default project. An existing user lands in their organization.
The user approves in their own browser: never type their email, password or payment
details into a form for them.

### With the CLI (preferred)

```sh
sikaru login --no-browser
```

The command prints a one-time code and a verification URL on **stderr**. It then
waits until the user approves or the code expires.

- **In an agent shell**, run it in the background so your tool call doesn't time out.
  Read the code and URL from its output, give both to the user, and wait for the
  command to exit 0. If the code expires, run it again.
- On success the CLI saves the default project and prints `Using project ...`. No
  project ID needs to be copied from the dashboard.
- At an interactive terminal, plain `sikaru login` opens the browser for the user.
  Any command run there while signed out starts sign-in automatically. Without a
  terminal, a signed-out command fails with an auth error, so sign in first.
- If `SIKARU_API_KEY` is set, it overrides the sign-in. Unset it for personal access.
- `sikaru login --with-token` reads a token the user pastes from standard input.
  Don't put the token on the command line, where it lands in shell history.

### Without the CLI (agent registration)

Follow https://sikaru.ai/auth.md with the user's email. It registers you, has the user
approve, and gives you a short-lived access token for `Authorization: Bearer`.

- The approval link expires after about 5 minutes. Give it to the user immediately,
  and mint a new attempt if they're too late.
- The user reads a code like `ABCD-EFGH` off the page. If completing the claim says
  the code is invalid, retry once without the hyphen (`ABCDEFGH`).
- A new user's first call, whichever it is, creates their organization and default
  project. `GET https://api.sikaru.ai/v1/projects` returns `defaultProjectId`.
- Model and System One calls without a `Sikaru-Project` header use the default
  project. Send the header to use another one.

## 3. Choose a different project (optional)

Sign-in already chose the default project. To switch:

```sh
sikaru config set project PROJECT_ID
sikaru config show
```

Commands with `-p/--project` use the saved project, or `SIKARU_PROJECT` if that is
set. Signed-in `inference` and `decision` calls bill the saved project, else the
organization's default project.

## 4. Check access

```sh
sikaru doctor
```

It checks the credential, the project and the workspace without starting a run.

| Status | Meaning |
| --- | --- |
| 401 | The credential is missing, invalid, or pointed at the wrong endpoint. Sign in again. |
| 403 | The credential can't do that operation in this project. Use a key with that permission. |
| 404 | Wrong project or resource ID, or it isn't visible to this caller. |

Don't fix an access failure by changing IDs or retrying.

## 5. Get an API key for code, servers and CI

SDKs and automation use a **project API key**, not the CLI sign-in. Install the
published SDK for the project's language:

```sh
pip install sikaru-sdk               # or: uv add sikaru-sdk; import sikaru_sdk
npm install @aadi-labs/sikaru-sdk    # TypeScript, server-side code only
```

The user creates the key in the dashboard (https://app.sikaru.ai) for the project.
Store it in the environment or a secret manager:

```sh
export SIKARU_API_KEY=...   # user pastes it; never echo it back
export SIKARU_PROJECT=PROJECT_ID
```

Grant only the permissions the integration needs:

| Task | Permission |
| --- | --- |
| List agents and read runs and trajectories | `runs:read` |
| Create an agent | `managed_agents:write` |
| Start a run | `runs:create` |
| Read run events | `events:read` |
| Send tool results or approvals | `tool_results:write` |
| Manage connections | `tool_providers:write` |
| Make release decisions | `harness:write` |

Keep the key on the backend. A browser or mobile app calls your backend, and the
backend calls Sikaru.

## 6. Add credits (only when asked or when a run pauses for funding)

`sikaru agent run` exits with code 5 when a run is paused for funding. Check the
balance first:

```sh
sikaru credits balance -o json   # {"state", "availableUsd", "topUpMaxUsd"}
```

| `state` | What to do |
| --- | --- |
| `no_card` | No credits yet. Top up from an agent wallet (the first paid top-up opens the organization's credit account), or ask the user to save a card in **Billing** at https://app.sikaru.ai, which adds a one-time $5 starting credit. Don't enter card details for them. |
| `complimentary` | Usage is covered. No credits needed. |
| `ready` with `topUpMaxUsd` null | An organization admin turned agent top-ups off. Ask the user to add credits in Billing. |
| `ready` | Top up from an agent wallet, up to `topUpMaxUsd`. |

To add credits from an agent wallet:

```sh
sikaru credits add --amount 20 -o json     # creates an offer; prints payUrl and id
sikaru credits status TOP_UP_ID            # "credited" once the payment lands
```

The minimum is 5 US dollars. Confirm the amount with the user before you create an
offer. Give them the pay URL, or pay it only with a wallet they explicitly approved
for this payment. Don't say credits were added until `credits status` reports
`credited`. Then resume the paused run with the `next` command from its result.

Docs: https://sikaru.ai/auth.md, https://docs.sikaru.ai/get-started/authentication.md,
https://docs.sikaru.ai/sdks-and-cli/cli-automation.md,
https://docs.sikaru.ai/sdks-and-cli/credits.md
