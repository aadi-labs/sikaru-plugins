# Agent instructions

This repository holds the Sikaru plugin for Claude Code, Codex and Agent Plugins hosts
such as Capy, and the skills it ships. It contains no client code. The CLI and SDKs live in `aadi-labs/sikaru-clients`
and are generated from the Sikaru API definition.

## Source boundaries

- `skills/<name>/SKILL.md` is the authoring source for every host. Claude Code, Codex
  and `npx skills` all read the same files. Keep the frontmatter `name` equal to the
  directory name.
- `author-sikaru-agent` has the same name as the skill published at
  `https://sikaru.ai/skills/author-sikaru-agent/SKILL.md`. When the agent document
  format or `sikaru agent` commands change, update both together.
- Keep the plugin version the same in `.claude-plugin/plugin.json`,
  `.codex-plugin/plugin.json` and the root `plugin.json`.
- The root `plugin.json` and `mcp.json` follow the Agent Plugins 1.0.0 schemas (Capy and
  other spec hosts read them); they allow no extra fields. Keep `mcp.json` listing the
  same servers as `.mcp.json`.
- Name only CLI commands that exist. Check a command with `sikaru <group> <command> -h`
  or `--schema`; never guess flags or fields.
- Link to `https://docs.sikaru.ai/<page>.md` and `https://sikaru.ai/agent-guide.md`
  for detail instead of copying long reference material into a skill.

## Content rules

- Skill descriptions are how agents find the skills. Write them with the words users
  actually type.
- Don't name infrastructure vendors in skill text. Composio is the one exception.
- Never include real keys, tokens, project IDs or customer data in examples.
- Publishing, widening access and paying for credits always need the user's explicit
  approval.

## Validation

Run these after any change:

```sh
python3 scripts/validate.py --cli "$(which sikaru)"
claude plugin validate .
```
