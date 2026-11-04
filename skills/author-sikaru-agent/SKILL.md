---
name: author-sikaru-agent
description: Write, validate, publish and run a Sikaru managed agent from one Markdown agent document with the Sikaru CLI. Use when the user wants to build, deploy, host, edit, review, publish, test or run a Sikaru agent, give an agent tools, apps or MCP servers, or turn instructions into a hosted agent.
---

# Author a Sikaru agent

An agent is one Markdown file: optional YAML frontmatter for settings, then the
instructions. The server is the only parser and compiler. Send the exact file. Don't
compute digests or rebuild the document from parsed fields.

Before writing anything, read https://sikaru.ai/agent-guide.md. It has worked
documents, mention rules and hosted invocation snippets. The frontmatter schema is
https://sikaru.ai/schemas/agent-document.json.

## The document

```markdown
---
tools:
  web_search:
    enabled: false
  bash:
    policy: require_approval
web:
  allow_domains: [pandas.pydata.org]
setup:
  packages:
    pip: [pandas]
---
# Data helper

Answer questions about the CSV files in the workspace. Load them with pandas,
show the code you ran, and state any rows you dropped or values you assumed.
```

- `model`: an ID from `sikaru inference models`. Leave it out to use the project
  default.
- `tools`: turn the built-in tools `bash`, `workspace`, `agents`, `memory`,
  `web_search` and `web_fetch` on or off, and set a `policy` of `allow`,
  `require_approval` or `deny`. All are on by default.
- `web`: set `allow_domains` or `block_domains`.
- `setup`: install `pip` and `npm` packages, run `commands`, clone `repos`.
- `access`, `budget`, `sources`: see the agent guide.
- Apps and MCP servers: connect them to the project first, in the dashboard or with
  `sikaru agent connections`. Then mention them in the instructions as `@app/github`
  or `@mcp/research`. Integrations go through Composio apps or custom remote MCP
  servers. Naming a tool in the instructions doesn't grant it. To narrow a grant:

```yaml
access:
  "@app/github":
    tools: [GITHUB_CREATE_ISSUE]
    policy: require_approval
```

## The lifecycle

The project comes from `-p` or from `sikaru config set project` (see `sikaru-setup`).

```sh
# 1. Check, then create. Choose an unused slug; if it's taken, inspect that agent
#    rather than overwrite it. `push` never creates an agent.
sikaru agent validate AGENT --file agent.md
sikaru agent create AGENT --file agent.md --name "Display name"   # add --personal to keep each person's conversations private (fixed at creation)

# 2. Edit: pull the saved draft and its revision, change it, push with that revision.
sikaru agent pull AGENT --file agent.md --query revision
sikaru agent push AGENT --file agent.md --revision REVISION

# 3. Review the access delta, show it to the user, and publish only with their OK.
sikaru agent review AGENT --revision REVISION --format json > review.json
sikaru agent publish AGENT --revision REVISION --access-digest "$(jq -r .accessDigest review.json)"
#    Add --live-version N after the first publication. Pass --acknowledge-widening or
#    --acknowledge-removals only for the changes the user actually reviewed.

# 4. Run it. Leave out the task to start a conversation.
sikaru agent run AGENT "Which pandas function reads a CSV file?"
sikaru agent run AGENT -m MODEL_ID --prompt-file task.md
sikaru agent run AGENT --compute local -C "$PWD" "..."   # tools run in this workspace with the user's OS permissions
sikaru agent logs RUN_ID --follow
sikaru agent stop RUN_ID
```

`sikaru agent run` exit codes:

| Code | Outcome | What to do |
| --- | --- | --- |
| 0 | completed | Report the result. |
| 1 | failed | Read `sikaru agent logs RUN_ID`, then fix the document or the input. |
| 2 | approval required | Show the pending action to the user, and pass on their decision. |
| 3 | cancelled | Report it. |
| 4 | recovery required | Follow the `next` command in the result. |
| 5 | paused for funding | See credits in `sikaru-setup`, then resume with `next`. |

A CLI timeout doesn't cancel a hosted run. Use `sikaru agent stop`.

## Rules

- A saved draft doesn't change live behavior. Only `publish` does, and `eval run`
  tests the live version.
- On a stale-revision conflict, pull the newer draft and reconcile it with the user.
  Don't retry over someone else's work.
- Never change mentions or `access` as part of an automatic prose rewrite.
- Never put credentials in a document. Shared secrets need the managed sandbox
  secrets capability and exact allowed HTTPS hosts. Read placeholders from
  `json.loads(os.environ["SIKARU_SECRET_PLACEHOLDERS"])["slug"]` and use them only
  in request headers.
- Personal apps and secrets resolve to the signed-in runner. A project key doesn't
  become a user because you pass a `user_id` label.
- Verify the returned session and its outcome. Creation alone isn't success.

For hosted invocation from an application (curl, Python or TypeScript), see the
"Hosted invocation snippets" section of the agent guide and
https://docs.sikaru.ai/run/runs-and-tool-requests.md.
