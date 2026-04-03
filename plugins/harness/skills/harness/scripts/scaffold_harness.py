#!/usr/bin/env python3
"""Scaffold a Codex-native harness from a JSON spec."""

from __future__ import annotations

import argparse
import copy
import json
import re
from pathlib import Path


TRANSLATIONS = {
    "en": {
        "codex_structure": "## Codex Structure",
        "agents_md_explains": "- `AGENTS.md` explains this harness.",
        "skills_store": "- `.agents/skills/` stores the orchestrator and supporting skills.",
        "config_registers": "- `.codex/config.toml` registers reusable subagent roles.",
        "agent_toml_points": "- `.codex/agents/*.toml` points each role to its instruction file.",
        "agent_md_contains": "- `.codex/agents/*.md` contains the actual role instructions.",
        "trusted_state": "Open the project in a trusted state so Codex loads the local `.codex/` config.",
        "reference_lineage": "## Reference Lineage",
        "collaboration_pattern": "## Collaboration Pattern",
        "skills": "## Skills",
        "subagent_roles": "## Subagent Roles",
        "usage": "## Usage",
        "ask_codex": "Ask Codex to use the `{name}` skill, or use a natural-language request that matches it.",
        "recommended_start": "- Recommended start: `{name}`",
        "workspace_root": "- Workspace root: `{value}`",
        "outputs": "## Outputs",
        "mode_matrix": "## Mode Matrix",
        "orchestrator_only": "`orchestrator only`",
        "validation_checklist": "## Validation Checklist",
        "check_config": "- Confirm every role in `.codex/config.toml` points to a real `.toml` file.",
        "check_toml": "- Confirm every role `.toml` points to a real `.md` instructions file.",
        "remove_placeholders": "- Remove any unresolved placeholders before considering the harness complete.",
        "use_role": "Use this role when Codex spawns a subagent from `.codex/config.toml`.",
        "core_responsibilities": "## Core Responsibilities",
        "resp_1": "1. Produce concrete outputs, not abstract commentary.",
        "resp_2": "2. Work within the role boundary instead of expanding scope opportunistically.",
        "resp_3": "3. Coordinate through shared workspace files and the parent thread.",
        "resp_4": "4. Flag contradictions or missing prerequisites quickly.",
        "focus_areas": "## Focus Areas",
        "working_principles": "## Working Principles",
        "principle_1": "- Prefer evidence over intuition.",
        "principle_2": "- Keep findings specific enough that the orchestrator can merge them directly.",
        "principle_3": "- Escalate ambiguity early when it changes the deliverable shape.",
        "deliverable_expectations": "## Deliverable Expectations",
        "write_output_to": "- Write the output to `{path}`.",
        "write_output_default": "- Write the output in the agreed file location.",
        "keep_structure": "- Keep the structure easy for the orchestrator to merge or review.",
        "facts_risks": "- Distinguish facts, risks, and recommendations when relevant.",
        "team_protocol": "## Team Communication Protocol",
        "read_inputs": "- Read inputs from {items} when relevant.",
        "report_to": "- Report final findings to `{name}`.",
        "report_blockers": "- Report major blockers quickly.",
        "call_out_overlaps": "- Call out overlaps or contradictions with adjacent roles instead of silently guessing.",
        "error_handling": "## Error Handling",
        "error_default_1": "- If the scope is smaller than expected, downshift to the highest-value review or artifact.",
        "error_default_2": "- If required context is missing, state the gap and continue with the strongest defensible partial result.",
        "activation_examples": "## Activation Examples",
        "mode_switching": "## Mode Switching",
        "workflow": "## Workflow",
        "phase_default": "Phase",
        "workflow_1": "1. Inspect the user request, current repository, and any existing harness files.",
        "workflow_2": "2. Search for nearby reference harnesses before inventing a new structure.",
        "workflow_3": "3. Choose the smallest collaboration pattern that fits the work.",
        "workflow_4": "4. Define explicit role boundaries, outputs, and validation checkpoints.",
        "workflow_5": "5. Delegate work with concrete deliverables and dependency order.",
        "workflow_6": "6. Merge outputs, request revisions when needed, and remove unresolved placeholders.",
        "workflow_7": "7. Present final deliverables with file references and remaining risks.",
        "workspace_contract": "## Workspace Contract",
        "primary_workspace_root": "- Primary workspace root: `{value}`",
        "expected_artifact": "- Expected artifact: `{value}`",
        "validation": "## Validation",
        "validation_1": "- Check that all generated paths resolve.",
        "validation_2": "- Check that the trigger description matches likely user requests.",
        "validation_3": "- Check that the chosen roles materially improve decomposition or quality.",
        "validation_4": "- Remove unresolved placeholders before finalizing the harness.",
        "specialist_skill": "Specialist supporting skill for this harness.",
        "load_only_when_needed": "- Load this only when the matching specialist needs extra domain guidance.",
        "avoid_duplicating": "- Avoid duplicating the orchestrator workflow here.",
    },
    "ko": {
        "codex_structure": "## Codex 구조",
        "agents_md_explains": "- `AGENTS.md`는 이 하네스를 설명한다.",
        "skills_store": "- `.agents/skills/`에는 오케스트레이터와 보조 스킬이 들어간다.",
        "config_registers": "- `.codex/config.toml`은 재사용 가능한 서브에이전트 역할을 등록한다.",
        "agent_toml_points": "- `.codex/agents/*.toml`은 각 역할의 지시문 파일을 가리킨다.",
        "agent_md_contains": "- `.codex/agents/*.md`에는 실제 역할 지시문이 들어간다.",
        "trusted_state": "Codex가 로컬 `.codex/` 설정을 읽도록 프로젝트를 trusted 상태로 연다.",
        "reference_lineage": "## 참고 하네스 계보",
        "collaboration_pattern": "## 협업 패턴",
        "skills": "## 스킬",
        "subagent_roles": "## 서브에이전트 역할",
        "usage": "## 사용법",
        "ask_codex": "Codex에게 `{name}` 스킬을 사용하라고 요청하거나, 그 의도와 맞는 자연어 요청을 사용한다.",
        "recommended_start": "- 추천 시작점: `{name}`",
        "workspace_root": "- 워크스페이스 루트: `{value}`",
        "outputs": "## 산출물",
        "mode_matrix": "## 모드 매트릭스",
        "orchestrator_only": "`오케스트레이터만`",
        "validation_checklist": "## 검증 체크리스트",
        "check_config": "- `.codex/config.toml`의 모든 역할이 실제 `.toml` 파일을 가리키는지 확인한다.",
        "check_toml": "- 각 역할 `.toml`이 실제 `.md` 지시문 파일을 가리키는지 확인한다.",
        "remove_placeholders": "- 미해결 placeholder를 모두 제거한 뒤 완료로 본다.",
        "use_role": "Codex가 `.codex/config.toml`에서 이 역할의 서브에이전트를 띄울 때 사용한다.",
        "core_responsibilities": "## 핵심 책임",
        "resp_1": "1. 추상적 코멘트보다 구체적 산출물을 만든다.",
        "resp_2": "2. 역할 경계를 지키고, 기회주의적으로 범위를 넓히지 않는다.",
        "resp_3": "3. 공유 워크스페이스 파일과 부모 스레드를 통해 조율한다.",
        "resp_4": "4. 충돌이나 전제 조건 누락은 빠르게 알린다.",
        "focus_areas": "## 집중 영역",
        "working_principles": "## 작업 원칙",
        "principle_1": "- 직감보다 근거를 우선한다.",
        "principle_2": "- 오케스트레이터가 바로 합칠 수 있을 정도로 구체적으로 쓴다.",
        "principle_3": "- 결과물 형태가 바뀔 수 있는 모호함은 초기에 올린다.",
        "deliverable_expectations": "## 산출물 기대치",
        "write_output_to": "- 결과는 `{path}`에 작성한다.",
        "write_output_default": "- 합의된 파일 위치에 결과를 작성한다.",
        "keep_structure": "- 오케스트레이터가 병합하거나 검토하기 쉽게 구조를 유지한다.",
        "facts_risks": "- 필요할 때 사실, 리스크, 권고를 구분해서 쓴다.",
        "team_protocol": "## 팀 커뮤니케이션 규약",
        "read_inputs": "- 관련이 있으면 {items}에서 입력을 읽는다.",
        "report_to": "- 최종 결과는 `{name}`에게 보고한다.",
        "report_blockers": "- 주요 blocker는 빠르게 알린다.",
        "call_out_overlaps": "- 인접 역할과 겹치거나 충돌하는 부분은 추측하지 말고 명시한다.",
        "error_handling": "## 예외 처리",
        "error_default_1": "- 범위가 예상보다 작으면 가장 가치 높은 리뷰나 산출물로 축소한다.",
        "error_default_2": "- 필수 맥락이 없으면 빈칸을 명시하고, 방어 가능한 최선의 부분 결과를 계속 만든다.",
        "activation_examples": "## 활성화 예시",
        "mode_switching": "## 모드 전환",
        "workflow": "## 워크플로우",
        "phase_default": "단계",
        "workflow_1": "1. 사용자 요청, 현재 저장소, 기존 하네스 파일을 점검한다.",
        "workflow_2": "2. 새 구조를 만들기 전에 근처 참고 하네스를 찾는다.",
        "workflow_3": "3. 작업에 맞는 가장 작은 협업 패턴을 고른다.",
        "workflow_4": "4. 역할 경계, 산출물, 검증 지점을 명시한다.",
        "workflow_5": "5. 구체적 deliverable과 의존 순서를 포함해 일을 위임한다.",
        "workflow_6": "6. 결과를 병합하고 필요하면 수정 요청을 하며 미해결 placeholder를 제거한다.",
        "workflow_7": "7. 최종 산출물은 파일 참조와 남은 리스크와 함께 제시한다.",
        "workspace_contract": "## 워크스페이스 계약",
        "primary_workspace_root": "- 기본 워크스페이스 루트: `{value}`",
        "expected_artifact": "- 기대 산출물: `{value}`",
        "validation": "## 검증",
        "validation_1": "- 생성된 모든 경로가 실제로 해석되는지 확인한다.",
        "validation_2": "- 트리거 설명이 실제 사용자 요청과 맞는지 확인한다.",
        "validation_3": "- 선택한 역할이 분업이나 품질 향상에 실제로 기여하는지 확인한다.",
        "validation_4": "- 하네스를 마무리하기 전에 미해결 placeholder를 제거한다.",
        "specialist_skill": "이 하네스를 위한 보조 전문 스킬이다.",
        "load_only_when_needed": "- 해당 전문 역할이 추가 도메인 가이드를 필요로 할 때만 불러온다.",
        "avoid_duplicating": "- 여기서 오케스트레이터 워크플로우를 중복 정의하지 않는다.",
    },
}


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


def get_language(spec: dict) -> str:
    language = str(spec.get("language", "en")).lower()
    return language if language in TRANSLATIONS else "en"


def t(spec: dict, key: str, **kwargs) -> str:
    template = TRANSLATIONS[get_language(spec)][key]
    return template.format(**kwargs) if kwargs else template


def normalize_spec(raw_spec: dict) -> dict:
    spec = copy.deepcopy(raw_spec)
    spec["slug"] = spec.get("slug") or slugify(spec["title"])
    spec["language"] = get_language(spec)
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
        agent["language"] = spec["language"]
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
    spec["web_search"] = spec.get("web_search", "disabled")
    return spec


def render_agents_md(spec: dict) -> str:
    title = spec["title"]
    summary = spec["summary"]
    orchestrator = spec["orchestrator"]
    skills = [orchestrator, *ensure_list(spec.get("supporting_skills"))]
    agents = ensure_list(spec.get("agents"))
    outputs = ensure_list(spec.get("workspace_outputs"))
    web_search = spec.get("web_search", "disabled")
    references = ensure_list(spec.get("reference_harnesses"))
    pattern = spec.get("collaboration_pattern", "supervisor")
    workspace_root = spec.get("workspace_root", "_workspace")
    modes = ensure_list(spec.get("mode_matrix"))

    lines = [
        f"# {title}",
        "",
        summary,
        "",
        t(spec, "codex_structure"),
        "",
        t(spec, "agents_md_explains"),
        t(spec, "skills_store"),
        t(spec, "config_registers"),
        t(spec, "agent_toml_points"),
        t(spec, "agent_md_contains"),
        "",
        t(spec, "trusted_state"),
        "",
    ]

    if references:
        lines.extend([t(spec, "reference_lineage"), ""])
        for item in references:
            path = item.get("path", "")
            reason = item.get("reason", "")
            lines.append(f"- `{path}`{': ' + reason if reason else ''}")
        lines.append("")

    lines.extend([t(spec, "collaboration_pattern"), "", f"- `{pattern}`", ""])
    lines.extend([t(spec, "skills"), ""])

    for skill in skills:
        lines.append(f"- `{skill['name']}`: {skill['description']}")

    lines.extend(["", t(spec, "subagent_roles"), ""])
    for agent in agents:
        lines.append(f"- `{agent['name']}`: {agent['description']}")

    lines.extend(
        [
            "",
            t(spec, "usage"),
            "",
            t(spec, "ask_codex", name=orchestrator["name"]),
            t(spec, "recommended_start", name=orchestrator["name"]),
            f"- `web_search` default: `{web_search}`",
            t(spec, "workspace_root", value=workspace_root),
        ]
    )

    if outputs:
        lines.extend(["", t(spec, "outputs"), ""])
        for item in outputs:
            lines.append(f"- `{item}`")

    if modes:
        lines.extend(["", t(spec, "mode_matrix"), ""])
        for item in modes:
            request = item.get("request", "default")
            roles = ", ".join(f"`{role}`" for role in ensure_list(item.get("roles")))
            notes = item.get("notes", "")
            line = f"- `{request}` -> {roles or t(spec, 'orchestrator_only')}"
            if notes:
                line += f": {notes}"
            lines.append(line)

    lines.extend(
        [
            "",
            t(spec, "validation_checklist"),
            "",
            t(spec, "check_config"),
            t(spec, "check_toml"),
            t(spec, "remove_placeholders"),
        ]
    )

    lines.append("")
    return "\n".join(lines)


def render_config_toml(spec: dict) -> str:
    lines = [
        "#:schema https://developers.openai.com/codex/config-schema.json",
        "",
        f'web_search = "{spec.get("web_search", "disabled")}"',
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
    lang_spec = {"language": agent.get("language", "en")}

    lines = [
        f"# {title}",
        "",
        t(lang_spec, "use_role"),
        "",
        f"{agent['description']}",
        "",
        t(lang_spec, "core_responsibilities"),
        "",
        t(lang_spec, "resp_1"),
        t(lang_spec, "resp_2"),
        t(lang_spec, "resp_3"),
        t(lang_spec, "resp_4"),
    ]

    if focus_areas:
        lines.extend(["", t(lang_spec, "focus_areas"), ""])
        for item in focus_areas:
            lines.append(f"- {item}")

    lines.extend(
        [
            "",
            t(lang_spec, "working_principles"),
            "",
            t(lang_spec, "principle_1"),
            t(lang_spec, "principle_2"),
            t(lang_spec, "principle_3"),
            "",
            t(lang_spec, "deliverable_expectations"),
            "",
        ]
    )

    if output_path:
        lines.append(t(lang_spec, "write_output_to", path=output_path))
    else:
        lines.append(t(lang_spec, "write_output_default"))

    lines.extend(
        [
            t(lang_spec, "keep_structure"),
            t(lang_spec, "facts_risks"),
            "",
            t(lang_spec, "team_protocol"),
            "",
        ]
    )

    if receives_from:
        lines.append(t(lang_spec, "read_inputs", items=", ".join(f"`{item}`" for item in receives_from)))
    if reports_to:
        lines.append(t(lang_spec, "report_to", name=reports_to))
    lines.extend(
        [
            t(lang_spec, "report_blockers"),
            t(lang_spec, "call_out_overlaps"),
            "",
            t(lang_spec, "error_handling"),
            "",
        ]
    )

    if error_handling:
        for item in error_handling:
            lines.append(f"- {item}")
    else:
        lines.extend(
            [
                t(lang_spec, "error_default_1"),
                t(lang_spec, "error_default_2"),
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
            lines.extend([t(spec, "activation_examples"), ""])
            for item in activation_examples:
                lines.append(f"- `{item}`")
            lines.append("")

        modes = ensure_list(spec.get("mode_matrix"))
        if modes:
            lines.extend([t(spec, "mode_switching"), ""])
            for item in modes:
                request = item.get("request", "default")
                roles = ", ".join(f"`{role}`" for role in ensure_list(item.get("roles")))
                notes = item.get("notes", "")
                line = f"- `{request}` -> {roles or t(spec, 'orchestrator_only')}"
                if notes:
                    line += f": {notes}"
                lines.append(line)
            lines.append("")

        phases = ensure_list(spec.get("phases"))
        if phases:
            lines.extend([t(spec, "workflow"), ""])
            for phase in phases:
                lines.append(f"### {phase.get('name', t(spec, 'phase_default'))}")
                lines.append("")
                for index, step in enumerate(ensure_list(phase.get("steps")), start=1):
                    lines.append(f"{index}. {step}")
                lines.append("")
        else:
            lines.extend(
                [
                    t(spec, "workflow"),
                    "",
                    t(spec, "workflow_1"),
                    t(spec, "workflow_2"),
                    t(spec, "workflow_3"),
                    t(spec, "workflow_4"),
                    t(spec, "workflow_5"),
                    t(spec, "workflow_6"),
                    t(spec, "workflow_7"),
                    "",
                ]
            )

        workspace_root = spec.get("workspace_root", "_workspace")
        outputs = ensure_list(spec.get("workspace_outputs"))
        lines.extend([t(spec, "workspace_contract"), "", t(spec, "primary_workspace_root", value=workspace_root)])
        for item in outputs:
            lines.append(t(spec, "expected_artifact", value=item))
        lines.extend(
            [
                "",
                t(spec, "validation"),
                "",
                t(spec, "validation_1"),
                t(spec, "validation_2"),
                t(spec, "validation_3"),
                t(spec, "validation_4"),
                "",
            ]
        )
        return "\n".join(lines)

    return (
        header
        + t(spec, "specialist_skill")
        + "\n\n"
        + t(spec, "usage")
        + "\n\n"
        + t(spec, "load_only_when_needed")
        + "\n"
        + t(spec, "avoid_duplicating")
        + "\n"
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
