# Reference Library

`codex-harness-100` is the reference library for this skill.

## Expected Location

By default, assume the library exists at:

`/Users/isanghyo/Desktop/harness/codex-harness-100`

The bundled search script also falls back to a few common sibling locations automatically. If the library exists somewhere else, pass `--root` explicitly.

## How To Use It

1. Search for the closest harness by domain and workflow.
2. Inspect the top 1 to 3 matches.
3. Reuse the pattern, not necessarily the exact wording.
4. Preserve strong structural ideas:
   - role boundaries
   - orchestration order
   - mode switching
   - output contract
5. Change what is domain-specific:
   - skill descriptions
   - agent instructions
   - output file names
   - web-search requirements

## Search Script

Use:

```bash
python3 plugins/harness/skills/harness/scripts/find_reference_harness.py "fullstack webapp" --limit 5
```

Useful variants:

```bash
python3 plugins/harness/skills/harness/scripts/find_reference_harness.py "code review security performance" --language ko
python3 plugins/harness/skills/harness/scripts/find_reference_harness.py "youtube seo thumbnail" --language en
```

## High-Value Seed Templates

These are usually strong starting points:

- `ko/16-fullstack-webapp`
- `ko/21-code-reviewer`
- `ko/27-data-pipeline`
- `ko/41-llm-app-builder`
- `ko/01-youtube-production`
- `ko/81-technical-writer`

Use English variants when the target project is primarily English-facing.

## What To Read From A Match

At minimum:

- `AGENTS.md`

Usually also:

- the main orchestrator skill under `.agents/skills/<name>/SKILL.md`
- one or two role files under `.codex/agents/`

## Adaptation Rule

Do not blindly copy a reference harness.

Instead:

- keep the structural strengths
- rename roles when the domain changes
- shrink the team when the target scope is smaller
- add review roles only when the quality bar requires them
