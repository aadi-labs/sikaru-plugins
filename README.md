# Sikaru plugins and skills

The official Sikaru plugin for Claude Code and Codex, plus the same skills for any
agent that loads `SKILL.md` files. Your coding agent learns to sign you up for
Sikaru, choose a project, and then work with it: call catalog models, ask System One
decisions, write and publish managed agents, evaluate them in RL environments, and
upload traces.

The plugin also connects the public Sikaru docs over MCP (`sikaru-docs`,
`https://docs.sikaru.ai/_mcp/server`). That server is read-only and needs no
credentials.

## Install

### Claude Code

```sh
claude plugin marketplace add aadi-labs/sikaru-plugins
claude plugin install sikaru@sikaru
```

### Codex

```sh
codex plugin marketplace add aadi-labs/sikaru-plugins
codex plugin add sikaru@sikaru
```

### Any agent with skills

```sh
npx skills add aadi-labs/sikaru-plugins
```

Or copy a folder from [`skills/`](skills) into your agent's skills directory.

## Then ask your agent

- "Set me up with Sikaru."
- "List the Sikaru models and chat with the cheapest one that supports reasoning."
- "Write a Sikaru agent for this repository, validate it and run one task."
- "Run my eval dataset against the live agent and show me the failures."

## Skills

| Skill | Use it to |
| --- | --- |
| [`sikaru`](skills/sikaru/SKILL.md) | Start any Sikaru task. It routes to the skills below and holds the shared rules. |
| [`sikaru-setup`](skills/sikaru-setup/SKILL.md) | Install the CLI, sign up or sign in, choose a project, get an API key, add credits |
| [`sikaru-inference`](skills/sikaru-inference/SKILL.md) | List and compare catalog models, and chat from the CLI or the OpenAI-shaped SDKs |
| [`sikaru-decision`](skills/sikaru-decision/SKILL.md) | Ask System One choice, yes-or-no and score questions about a text or JSON state |
| [`author-sikaru-agent`](skills/author-sikaru-agent/SKILL.md) | Write, validate, review, publish and run a managed agent from one Markdown document |
| [`sikaru-evals`](skills/sikaru-evals/SKILL.md) | Push environment datasets, run evals against the live agent, and read the failures |
| [`sikaru-traces`](skills/sikaru-traces/SKILL.md) | Upload OTLP, ATIF or OpenInference traces and read run trajectories |

## Requirements

The skills drive the `sikaru` CLI. They need a build with the `decision` and
`credits` groups (`sikaru decision --help` should work):

```sh
curl -fsSL https://app.sikaru.ai/install.sh | sh   # macOS and Linux
npm install -g @aadi-labs/sikaru-cli               # any platform with Node.js 20+
```

Code uses the published SDKs, which share the CLI's version:

| Language | Install | Import |
| --- | --- | --- |
| Python | `pip install sikaru-sdk` or `uv add sikaru-sdk` | `from sikaru_sdk import SikaruApi` |
| TypeScript | `npm install @aadi-labs/sikaru-sdk` | `import { SikaruApi } from "@aadi-labs/sikaru-sdk"` |

Signing up and signing in both start with `sikaru login`, which also saves your default
project. Agents without the CLI follow https://sikaru.ai/auth.md. Code, servers and CI use a
project API key in `SIKARU_API_KEY`, created in the dashboard at https://app.sikaru.ai.

Work is prepaid with credits, and an agent can fund it: `sikaru credits add --amount 20`
creates an offer that an agent wallet pays, even for a brand-new organization. People can
instead save a card in **Billing** at https://app.sikaru.ai, which also adds a one-time $5
starting credit.

## Repository layout

| Path | Contents |
| --- | --- |
| `.claude-plugin/` | Claude Code plugin and marketplace manifests |
| `.codex-plugin/`, `.agents/plugins/` | Codex plugin and marketplace manifests |
| `.mcp.json` | The `sikaru-docs` MCP server |
| `skills/` | The skills; each has a `SKILL.md` and Codex metadata in `agents/openai.yaml` |
| `skills.sh.json` | Skill list for `npx skills` |
| `scripts/validate.py` | Manifest, skill and CLI-command checks |

## Development

```sh
python3 scripts/validate.py --cli "$(which sikaru)"
claude plugin validate .
```

The `--cli` check runs every `sikaru …` command the skills mention with `-h`. A
renamed or removed CLI command fails the check.

## License

MIT
