#!/usr/bin/env python3
"""Scaffold a Codex-native harness from a JSON spec."""

from __future__ import annotations

import argparse
import copy
import json
import re
from pathlib import Path


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value


def read_spec(path: Path) -> dict:
    with path.open() as handle:
        return json.load(handle)


def ensure_list(value):
    return value if isinstance(value, list) else []


def normalize_spec(raw_spec: dict) -> dict:
    spec = copy.deepcopy(raw_spec)
    spec["slug"] = spec.get("slug") or slugify(spec["title"])
    spec["workspace_root"] = spec.get("workspace_root", "_workspace")
    spec["collaboration_pattern"] = spec.get("collaboration_pattern", "supervisor")

    orchestrator = dict(spec["orchestrator"])
    orchestrator["name"] = slugify(orchestrator["name"])
    spec["orchestrator"] = orchestrator

    supporting_skills = []
    for item in ensure_list(spec.get("supporting_skills")):
        skill = dict(item)
        skill["name"] = slugify(skill["name"])
        supporting_skills.append(skill)
    spec["supporting_skills"] = supporting_skills

    agents = []
    for item in ensure_list(spec.get("agents")):
        agent = dict(item)
        agent["name"] = slugify(agent["name"])
        agents.append(agent)
    spec["agents"] = agents

    if "workspace_outputs" not in spec:
        spec["workspace_outputs"] = [
            f'{spec["workspace_root"]}/00_input.md',
            f'{spec["workspace_root"]}/01_plan.md',
            f'{spec["workspace_root"]}/99_final.md',
        ]

    spec["max_threads"] = spec.get("max_threads", max(len(spec["agents"]) + 1, 2))
    spec["max_depth"] = spec.get("max_depth", 1)
    spec["web_search"] = spec.get("web_search", "off")
    return spec


def render_agents_md(spec: dict) -> str:
    title = spec["title"]
    summary = spec["summary"]
    orchestrator = spec["orchestrator"]
    skills = [orchestrator, *ensure_list(spec.get("supporting_skills"))]
    agents = ensure_list(spec.get("agents"))
    outputs = ensure_list(spec.get("workspace_outputs"))
    web_search = spec.get("web_search", "off")
    references = ensure_list(spec.get("reference_harnesses"))
    pattern = spec.get("collaboration_pattern", "supervisor")
    workspace_root = spec.get("workspace_root", "_workspace")
    modes = ensure_list(spec.get("mode_matrix"))

    lines = [
        f"# {title}",
        "",
        summary,
        "",
        "## Codex Structure",
        "",
        "- `AGENTS.md` explains this harness.",
        "- `.agents/skills/` stores the orchestrator and supporting skills.",
        "- `.codex/config.toml` registers reusable subagent roles.",
        "- `.codex/agents/*.toml` points each role to its instruction file.",
        "- `.codex/agents/*.md` contains the actual role instructions.",
        "",
        "Open the project in a trusted state so Codex loads the local `.codex/` config.",
        "",
    ]

    if references:
        lines.extend(["## Reference Lineage", ""])
        for item in references:
            path = item.get("path", "")
            reason = item.get("reason", "")
            lines.append(f"- `{path}`{': ' + reason if reason else ''}")
        lines.append("")

    lines.extend(["## Collaboration Pattern", "", f"- `{pattern}`", ""])
    lines.extend(["## Skills", ""])

    for skill in skills:
        lines.append(f"- `{skill['name']}`: {skill['description']}")

    lines.extend(["", "## Subagent Roles", ""])
    for agent in agents:
        lines.append(f"- `{agent['name']}`: {agent['description']}")

    lines.extend(
        [
            "",
            "## Usage",
            "",
            f"Ask Codex to use the `{orchestrator['name']}` skill, or use a natural-language request that matches it.",
            f"- Recommended start: `{orchestrator['name']}`",
            f"- `web_search` default: `{web_search}`",
            f"- Workspace root: `{workspace_root}`",
        ]
    )

    if outputs:
        lines.extend(["", "## Outputs", ""])
        for item in outputs:
            lines.append(f"- `{item}`")

    if modes:
        lines.extend(["", "## Mode Matrix", ""])
        for item in modes:
            request = item.get("request", "default")
            roles = ", ".join(f"`{role}`" for role in ensure_list(item.get("roles")))
            notes = item.get("notes", "")
            line = f"- `{request}` -> {roles or '`orchestrator only`'}"
            if notes:
                line += f": {notes}"
            lines.append(line)

    lines.extend(
        [
            "",
            "## Validation Checklist",
            "",
            "- Confirm every role in `.codex/config.toml` points to a real `.toml` file.",
            "- Confirm every role `.toml` points to a real `.md` instructions file.",
            "- Remove any unresolved placeholders before considering the harness complete.",
        ]
    )

    lines.append("")
    return "\n".join(lines)


def render_config_toml(spec: dict) -> str:
    lines = [
        "#:schema https://developers.openai.com/codex/config-schema.json",
        "",
        f'web_search = "{spec.get("web_search", "off")}"',
        "",
        "[features]",
        "multi_agent = true",
        "",
        "[agents]",
        f"max_threads = {spec.get('max_threads', max(len(ensure_list(spec.get('agents'))) + 1, 2))}",
        f"max_depth = {spec.get('max_depth', 1)}",
        "",
    ]
    for agent in ensure_list(spec.get("agents")):
        lines.extend(
            [
                f"[agents.{agent['name']}]",
                f'description = "{agent["description"].replace(chr(34), chr(39))}"',
                f'config_file = ".codex/agents/{agent["name"]}.toml"',
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def render_agent_toml(agent: dict) -> str:
    return f'model_instructions_file = "{agent["name"]}.md"\n'


def render_agent_md(agent: dict) -> str:
    title = agent.get("role_title") or agent["name"].replace("-", " ").title()
    body = agent.get("instructions")
    if body:
        return body.rstrip() + "\n"

    focus_areas = ensure_list(agent.get("focus_areas"))
    reports_to = agent.get("reports_to")
    receives_from = ensure_list(agent.get("receives_from"))
    output_path = agent.get("output_path")
    error_handling = ensure_list(agent.get("error_handling"))

    lines = [
        f"# {title}",
        "",
        "Use this role when Codex spawns a subagent from `.codex/config.toml`.",
        "",
        f"{agent['description']}",
        "",
        "## Core Responsibilities",
        "",
        "1. Produce concrete outputs, not abstract commentary.",
        "2. Work within the role boundary instead of expanding scope opportunistically.",
        "3. Coordinate through shared workspace files and the parent thread.",
        "4. Flag contradictions or missing prerequisites quickly.",
    ]

    if focus_areas:
        lines.extend(["", "## Focus Areas", ""])
        for item in focus_areas:
            lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Working Principles",
            "",
            "- Prefer evidence over intuition.",
            "- Keep findings specific enough that the orchestrator can merge them directly.",
            "- Escalate ambiguity early when it changes the deliverable shape.",
            "",
            "## Deliverable Expectations",
            "",
        ]
    )

    if output_path:
        lines.append(f"- Write the output to `{output_path}`.")
    else:
        lines.append("- Write the output in the agreed file location.")

    lines.extend(
        [
            "- Keep the structure easy for the orchestrator to merge or review.",
            "- Distinguish facts, risks, and recommendations when relevant.",
            "",
            "## Team Communication Protocol",
            "",
        ]
    )

    if receives_from:
        lines.append(f"- Read inputs from {', '.join(f'`{item}`' for item in receives_from)} when relevant.")
    if reports_to:
        lines.append(f"- Report final findings to `{reports_to}`.")
    lines.extend(
        [
            "- Report major blockers quickly.",
            "- Call out overlaps or contradictions with adjacent roles instead of silently guessing.",
            "",
            "## Error Handling",
            "",
        ]
    )

    if error_handling:
        for item in error_handling:
            lines.append(f"- {item}")
    else:
        lines.extend(
            [
                "- If the scope is smaller than expected, downshift to the highest-value review or artifact.",
                "- If required context is missing, state the gap and continue with the strongest defensible partial result.",
            ]
        )

    lines.append("")
    return "\n".join(lines)


def render_skill_md(skill: dict, title: str, summary: str, is_orchestrator: bool, spec: dict) -> str:
    body = skill.get("instructions")
    if body:
        return body.rstrip() + "\n"

    header = (
        f'---\nname: {skill["name"]}\n'
        f'description: "{skill["description"]}"\n---\n\n'
        f"# {title if is_orchestrator else skill['name'].replace('-', ' ').title()}\n\n"
    )

    if is_orchestrator:
        lines = [header.rstrip(), "", summary, ""]

        activation_examples = ensure_list(spec.get("activation_examples"))
        if activation_examples:
            lines.extend(["## Activation Examples", ""])
            for item in activation_examples:
                lines.append(f"- `{item}`")
            lines.append("")

        modes = ensure_list(spec.get("mode_matrix"))
        if modes:
            lines.extend(["## Mode Switching", ""])
            for item in modes:
                request = item.get("request", "default")
                roles = ", ".join(f"`{role}`" for role in ensure_list(item.get("roles")))
                notes = item.get("notes", "")
                line = f"- `{request}` -> {roles or '`orchestrator only`'}"
                if notes:
                    line += f": {notes}"
                lines.append(line)
            lines.append("")

        phases = ensure_list(spec.get("phases"))
        if phases:
            lines.extend(["## Workflow", ""])
            for phase in phases:
                lines.append(f"### {phase.get('name', 'Phase')}")
                lines.append("")
                for index, step in enumerate(ensure_list(phase.get("steps")), start=1):
                    lines.append(f"{index}. {step}")
                lines.append("")
        else:
            lines.extend(
                [
                    "## Workflow",
                    "",
                    "1. Inspect the user request, current repository, and any existing harness files.",
                    "2. Search for nearby reference harnesses before inventing a new structure.",
                    "3. Choose the smallest collaboration pattern that fits the work.",
                    "4. Define explicit role boundaries, outputs, and validation checkpoints.",
                    "5. Delegate work with concrete deliverables and dependency order.",
                    "6. Merge outputs, request revisions when needed, and remove unresolved placeholders.",
                    "7. Present final deliverables with file references and remaining risks.",
                    "",
                ]
            )

        workspace_root = spec.get("workspace_root", "_workspace")
        outputs = ensure_list(spec.get("workspace_outputs"))
        lines.extend(["## Workspace Contract", "", f"- Primary workspace root: `{workspace_root}`"])
        for item in outputs:
            lines.append(f"- Expected artifact: `{item}`")
        lines.extend(
            [
                "",
                "## Validation",
                "",
                "- Check that all generated paths resolve.",
                "- Check that the trigger description matches likely user requests.",
                "- Check that the chosen roles materially improve decomposition or quality.",
                "- Remove unresolved placeholders before finalizing the harness.",
                "",
            ]
        )
        return "\n".join(lines)

    return (
        header
        + "Specialist supporting skill for this harness.\n\n"
        + "## Usage\n\n"
        + "- Load this only when the matching specialist needs extra domain guidance.\n"
        + "- Avoid duplicating the orchestrator workflow here.\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a Codex harness from a JSON spec.")
    parser.add_argument("--spec", required=True, help="Path to the JSON spec file")
    parser.add_argument("--target", required=True, help="Target project root")
    args = parser.parse_args()

    spec = normalize_spec(read_spec(Path(args.spec).expanduser()))
    target = Path(args.target).expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)

    slug = spec["slug"]
    title = spec["title"]
    summary = spec["summary"]
    orchestrator = spec["orchestrator"]
    supporting_skills = ensure_list(spec.get("supporting_skills"))
    agents = ensure_list(spec.get("agents"))

    (target / ".agents" / "skills").mkdir(parents=True, exist_ok=True)
    (target / ".codex" / "agents").mkdir(parents=True, exist_ok=True)

    (target / "AGENTS.md").write_text(render_agents_md(spec))
    (target / ".codex" / "config.toml").write_text(render_config_toml(spec))

    for agent in agents:
        name = agent["name"]
        (target / ".codex" / "agents" / f"{name}.toml").write_text(render_agent_toml(agent))
        (target / ".codex" / "agents" / f"{name}.md").write_text(render_agent_md(agent))

    all_skills = [(orchestrator, True), *[(item, False) for item in supporting_skills]]
    for skill, is_orchestrator in all_skills:
        skill_name = skill["name"]
        skill_dir = target / ".agents" / "skills" / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        text = render_skill_md(skill, title, summary, is_orchestrator, spec)
        (skill_dir / "SKILL.md").write_text(text)

    print(f"Scaffolded harness '{slug}' at {target}")


if __name__ == "__main__":
    main()
