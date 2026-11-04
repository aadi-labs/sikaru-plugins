#!/usr/bin/env python3
"""Check the plugin manifests, the skills, and (with --cli) every CLI command the skills name.

Usage: python3 scripts/validate.py [--cli PATH_TO_SIKARU]
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFESTS = [
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".codex-plugin/plugin.json",
    ".agents/plugins/marketplace.json",
    ".mcp.json",
    "skills.sh.json",
]
# `sikaru <group> <verb>` as written in skill text; flags and placeholders are ignored.
COMMAND = re.compile(r"\bsikaru ((?:[a-z][a-z-]*)(?: [a-z][a-z-]*){0,2})\b")
TOP_LEVEL = {"login", "logout", "doctor", "config", "credits", "inference", "decision",
             "agent", "eval", "traces", "environment", "generate-skills"}

errors: list[str] = []


def load(path: str):
    try:
        return json.loads((ROOT / path).read_text())
    except (OSError, ValueError) as exc:
        errors.append(f"{path}: {exc}")
        return {}


def frontmatter(skill: Path) -> dict[str, str]:
    text = skill.read_text()
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not match:
        errors.append(f"{skill}: missing frontmatter")
        return {}
    return dict(line.split(": ", 1) for line in match.group(1).splitlines() if ": " in line)


manifests = {path: load(path) for path in MANIFESTS}
versions = {manifests[p].get("version") for p in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json")}
if len(versions) != 1:
    errors.append(f"plugin versions differ: {versions}")

skill_dirs = sorted(p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md"))
if sorted(manifests["skills.sh.json"].get("skills", [])) != skill_dirs:
    errors.append(f"skills.sh.json does not list exactly {skill_dirs}")

commands: set[str] = set()
for name in skill_dirs:
    skill = ROOT / "skills" / name / "SKILL.md"
    meta = frontmatter(skill)
    if meta.get("name") != name:
        errors.append(f"{skill}: name {meta.get('name')!r} does not match its directory")
    if not 0 < len(meta.get("description", "")) <= 1024:
        errors.append(f"{skill}: description must be 1-1024 characters")
    if not (ROOT / "skills" / name / "agents" / "openai.yaml").exists():
        errors.append(f"{skill}: missing agents/openai.yaml")
    for match in COMMAND.finditer(skill.read_text()):
        words = match.group(1).split()
        if words[0] in TOP_LEVEL:
            commands.add(" ".join(words))

if "--cli" in sys.argv:
    binary = sys.argv[sys.argv.index("--cli") + 1]
    for command in sorted(commands):
        result = subprocess.run([binary, *command.split(), "-h"], capture_output=True, text=True)
        if result.returncode != 0:
            errors.append(f"`sikaru {command}` is not a CLI command")

for error in errors:
    print("error:", error)
print(f"{len(skill_dirs)} skills, {len(commands)} CLI commands referenced, {len(errors)} errors")
sys.exit(1 if errors else 0)
