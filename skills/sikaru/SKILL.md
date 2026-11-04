---
name: sikaru
description: Start here for anything Sikaru. Use when the user mentions Sikaru, sikaru.ai, the `sikaru` CLI, `sikaru_sdk` or `@aadi-labs/sikaru-sdk`, or wants a hosted platform to call catalog models, ask System One decisions, run managed agents, evaluate agents in RL environments or analyze agent traces. Routes to the setup, inference, decision, agent, eval and trace skills.
---

# Sikaru

Sikaru runs managed agents, evaluations and trace analysis, and serves a catalog of
models, over one API at `https://api.sikaru.ai`. There are three clients, all at the
same version:

| Client | Install | Use |
| --- | --- | --- |
| CLI | `curl -fsSL https://app.sikaru.ai/install.sh \| sh` or `npm install -g @aadi-labs/sikaru-cli` | `sikaru ...` |
| Python SDK | `pip install sikaru-sdk` | `from sikaru_sdk import SikaruApi` |
| TypeScript SDK | `npm install @aadi-labs/sikaru-sdk` | `import { SikaruApi } from "@aadi-labs/sikaru-sdk"` |

Install only these published packages. Don't vendor, build or hand-edit client code.

## First, make sure the user can reach Sikaru

Run `sikaru doctor`. If the command is missing, the user is signed out, or no
project is set, follow the `sikaru-setup` skill before anything else. It covers
installing the CLI, creating an account, signing in, choosing a project, and getting
an API key for code.

## Pick the skill for the job

| The user wants to | Skill | CLI group |
| --- | --- | --- |
| Install, sign up, sign in, choose a project, get an API key, add credits | `sikaru-setup` | `login`, `config`, `doctor`, `credits` |
| Call a catalog model, list models, use the OpenAI-shaped SDK | `sikaru-inference` | `sikaru inference` |
| Classify or score a text or JSON state (choice, yes-or-no, score) | `sikaru-decision` | `sikaru decision` |
| Write, validate, publish or run a managed agent | `author-sikaru-agent` | `sikaru agent` |
| Create an RL environment dataset and evaluate an agent in it | `sikaru-evals` | `sikaru environment`, `sikaru eval` |
| Upload traces from another system or read a run's trajectory | `sikaru-traces` | `sikaru traces` |

Every API operation can also be called under its product group. When a group verb
doesn't cover what you need, run `sikaru <group> --help`, then
`sikaru <group> <command> --schema` to get exact arguments. Don't guess flags.

## Read the docs instead of guessing

- The `sikaru-docs` MCP server that ships with this plugin searches the public docs.
- `https://docs.sikaru.ai/llms.txt` indexes every guide and endpoint. Add `.md` to
  any docs page URL to get Markdown.
- `https://docs.sikaru.ai/openapi.json` has the exact request and response fields.
  Use only operations listed there.

## Rules for every Sikaru task

- Keep keys secret. Never print `SIKARU_API_KEY` or a sign-in token, and never put
  one in a committed file, an agent document, a browser bundle or chat output.
- `SIKARU_API_KEY` takes precedence over `sikaru login`. Unset it when the user
  wants their personal signed-in identity.
- `sikaru login` saves the default project; pass `-p PROJECT` only to use another.
  Never invent a project ID; read it from `sikaru config show` or `defaultProjectId`.
- An accepted request is not a finished run. Read the run's status or events until
  it reaches `completed`, `failed` or `cancelled` before you report a result.
- When you retry a submission, reuse its idempotency key. A new key means new work.
- Publishing an agent, widening its access, and adding credits all need the user's
  explicit approval. Show what will change first.
- Use `--format json` (or `-o json` where offered) and `--query` when you parse output.
  Check the exit code.
