# Sikaru plugins and skills

The official Sikaru plugin for Claude Code and Codex, plus the same skills for any
agent that loads `SKILL.md` files: Cursor, Devin, Capy, Pi, OpenCode, Gemini CLI,
GitHub Copilot, Amp, Cline, Windsurf, Goose and more. Your coding agent learns to sign you up for
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

The installer detects the agents you have and asks where to install. To pick one,
pass its name with `-a` (add `-g` to install for your user instead of the project):

| Agent | Command |
| --- | --- |
| Pi | `npx skills add aadi-labs/sikaru-plugins -a pi` |
| OpenCode | `npx skills add aadi-labs/sikaru-plugins -a opencode` |
| Cursor | `npx skills add aadi-labs/sikaru-plugins -a cursor` |
| Devin for Terminal | `npx skills add aadi-labs/sikaru-plugins -a devin` |
| Gemini CLI | `npx skills add aadi-labs/sikaru-plugins -a gemini-cli` |
| GitHub Copilot | `npx skills add aadi-labs/sikaru-plugins -a github-copilot` |
| Amp | `npx skills add aadi-labs/sikaru-plugins -a amp` |
| Cline | `npx skills add aadi-labs/sikaru-plugins -a cline` |
| Windsurf | `npx skills add aadi-labs/sikaru-plugins -a windsurf` |
| Goose | `npx skills add aadi-labs/sikaru-plugins -a goose` |
| Factory Droid | `npx skills add aadi-labs/sikaru-plugins -a droid` |
| Kilo Code | `npx skills add aadi-labs/sikaru-plugins -a kilo` |
| Roo Code | `npx skills add aadi-labs/sikaru-plugins -a roo` |
| Zed | `npx skills add aadi-labs/sikaru-plugins -a zed` |
| Warp | `npx skills add aadi-labs/sikaru-plugins -a warp` |
| OpenHands | `npx skills add aadi-labs/sikaru-plugins -a openhands` |
| Kiro CLI | `npx skills add aadi-labs/sikaru-plugins -a kiro-cli` |
| Qwen Code | `npx skills add aadi-labs/sikaru-plugins -a qwen-code` |

Any other agent that reads `SKILL.md` files works too: copy a folder from
[`skills/`](skills) into its skills directory. See the
[full list of supported agents](https://github.com/vercel-labs/skills/blob/main/docs/agents.md).

### Capy

Capy installs this repository as a plugin, skills and docs server together: open
**Settings → MCP & plugins**, choose **From GitHub repository**, and enter
`https://github.com/aadi-labs/sikaru-plugins`. Click **Sync** on the plugin page to pick
up new versions. To keep the skills in one repository instead, install them where Capy
reads repository skills:

```sh
npx skills add aadi-labs/sikaru-plugins -a universal
```

That writes to `.agents/skills/`, which Capy, Cursor, Codex, OpenCode, Pi and other
agents all read.

### Docs over MCP in other agents

Claude Code, Codex and Capy get the docs server from the plugin. Elsewhere, add
`https://docs.sikaru.ai/_mcp/server` as a remote MCP server (Streamable HTTP, no
credentials):

- OpenCode, in `opencode.json`:
  `{"mcp": {"sikaru-docs": {"type": "remote", "url": "https://docs.sikaru.ai/_mcp/server"}}}`
- Gemini CLI, in `~/.gemini/settings.json`:
  `{"mcpServers": {"sikaru-docs": {"httpUrl": "https://docs.sikaru.ai/_mcp/server"}}}`
- Cursor, in `.cursor/mcp.json`:
  `{"mcpServers": {"sikaru-docs": {"url": "https://docs.sikaru.ai/_mcp/server"}}}`
- GitHub Copilot in VS Code, in `.vscode/mcp.json`:
  `{"servers": {"sikaru-docs": {"type": "http", "url": "https://docs.sikaru.ai/_mcp/server"}}}`

Agents without MCP, such as Pi, read the same docs as Markdown: start at
https://docs.sikaru.ai/llms.txt.

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
| `.mcp.json` | The `sikaru-docs` MCP server for Claude Code and Codex |
| `plugin.json`, `mcp.json` | [Agent Plugins](https://agent-plugins.org/specification) manifest and MCP servers, used by Capy and other spec-following hosts |
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
