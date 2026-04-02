# Codex Harness

**Harness Architect for Codex**  
Project-specific harness generator for `AGENTS.md`, repo-local skills, and reusable Codex subagent roles.

**English** | [한국어](README_KO.md)  
[Publishing Guide](PUBLISHING.md) | [공개 배포 가이드](PUBLISHING_KO.md)

This repository adapts the original Claude-oriented `harness` project into a Codex-native plugin and meta skill. The goal is the same: when a user says "하네스 구성해줘" or "build a harness for this project", Codex should analyze the domain, choose a coordination pattern, define specialist roles, and scaffold a reusable harness for the current repository.

## Ask Codex To Reference This Repo

The intended usage is not "clone this repo and manually copy files." The simpler workflow is to ask Codex to build a new harness while using `codex-harness` as the reference repository.

Tell Codex to inspect this repo, look at the included examples, and generate a harness for your target domain in the same style.

Example prompt:

```text
codex-harness를 참고해서 일본 여행 길라잡이 웹 서비스 하네스 만들어줘
```

That is the core pattern: ask Codex to use `codex-harness` as the reference, then describe the product or workflow you want the new harness to support.

## Quick Install

Today, the practical install paths are `repo marketplace` or `personal marketplace`. Official self-serve publishing to the public Codex Plugin Directory is not available yet.

### Option 1: Install into one repo

Use this when a team wants `codex-harness` only inside one project.

1. Copy this plugin into `$REPO_ROOT/plugins/harness`.
2. Copy this marketplace file into `$REPO_ROOT/.agents/plugins/marketplace.json`:
   - `./.agents/plugins/marketplace.json`
3. Restart Codex.
4. Open `Plugins` in the Codex app, or run:

```text
codex
/plugins
```

5. Choose the repo marketplace and install `harness`.

Repo marketplace file:

```json
{
  "name": "codex-harness-local",
  "interface": {
    "displayName": "Codex Harness Local"
  },
  "plugins": [
    {
      "name": "harness",
      "source": {
        "source": "local",
        "path": "./plugins/harness"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

### Option 2: Install for one user across many repos

1. Copy `plugins/harness` into `~/.codex/plugins/harness`.
2. Add a personal marketplace file at `~/.agents/plugins/marketplace.json`.
3. Point its `source.path` to the installed plugin with a `./`-prefixed relative path.
4. Restart Codex and install `harness` from that marketplace.

Personal marketplace file:

```json
{
  "name": "codex-harness-personal",
  "interface": {
    "displayName": "Codex Harness Personal"
  },
  "plugins": [
    {
      "name": "harness",
      "source": {
        "source": "local",
        "path": "./.codex/plugins/harness"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

See [PUBLISHING.md](PUBLISHING.md) for full examples and file contents.

## Overview

`codex-harness` is the generator. It does not ship 100 finished harnesses. Instead, it creates a harness tailored to the current project by combining:

- a repo guide in `AGENTS.md`
- one orchestrator skill under `.agents/skills/`
- optional supporting skills
- reusable subagent role configs under `.codex/agents/`
- Codex configuration in `.codex/config.toml`

When the sibling repository `/Users/isanghyo/Desktop/harness/codex-harness-100` is available, this plugin should treat that catalog as its primary reference library instead of inventing structures from scratch.

## Key Features

- **Harness Architecture Design**: choose among pipeline, fan-out/fan-in, expert pool, generate-critique, supervisor, and hierarchical delegation
- **Reference-First Generation**: search `codex-harness-100`, inspect nearby examples, then adapt deliberately
- **Codex-Native Output**: generate `AGENTS.md`, repo-local skills, and `.codex` subagent configs rather than Claude-only `.claude/` files
- **Reusable Scaffolding**: bundled scripts help search references and scaffold a new harness from a JSON spec
- **Validation Mindset**: generated harnesses include role boundaries, workflow phases, output expectations, and checks for unresolved placeholders

## Workflow

```text
Phase 1: Domain Analysis
    ↓
Phase 2: Collaboration Pattern Design
    ↓
Phase 3: Subagent Role Definition (.codex/agents/)
    ↓
Phase 4: Skill Generation (.agents/skills/)
    ↓
Phase 5: Orchestration & Workspace Contract
    ↓
Phase 6: Validation & Refinement
```

## Relationship To `codex-harness-100`

These two repositories serve different roles:

- `codex-harness`: generator plugin and meta skill
- `codex-harness-100`: companion reference library of completed harness examples

Recommended workflow:

1. Ask Codex to build a harness for the current repo.
2. If `codex-harness-100` is available, let the `harness` skill search it for the closest existing patterns. If not, `codex-harness` should still generate a harness without the reference library.
3. Inspect the top 1 to 3 matching harnesses.
4. Adapt the team shape, outputs, and skill structure to the current project.
5. Scaffold and refine the new local harness.

## Installation

The official Codex plugin docs support three relevant surfaces for this project:

1. the curated Plugin Directory inside Codex
2. a repo marketplace at `$REPO_ROOT/.agents/plugins/marketplace.json`
3. a personal marketplace at `~/.agents/plugins/marketplace.json`

Today, `codex-harness` is ready for repo and personal marketplace distribution. Official self-serve public publishing to the Codex Plugin Directory is still coming soon.

### Repo marketplace

Use this when a team wants the plugin available inside a single repository.

1. Put the plugin folder at `$REPO_ROOT/plugins/harness`.
2. Add or update `$REPO_ROOT/.agents/plugins/marketplace.json`.
3. Ensure the plugin entry points to `./plugins/harness`.
4. Restart Codex.
5. Open the plugin directory and install `harness`.

This repository already ships the needed local metadata:

- `.agents/plugins/marketplace.json`
- `plugins/harness/.codex-plugin/plugin.json`

### Personal marketplace

Use this when one person wants the plugin across many repositories.

1. Copy the plugin to `~/.codex/plugins/harness`.
2. Add or update `~/.agents/plugins/marketplace.json`.
3. Point the marketplace entry at the plugin with a `./`-prefixed relative path.
4. Restart Codex and install `harness` from that marketplace.

### Direct local iteration

If you are still editing the plugin before installation:

1. Open this repository in Codex.
2. Reuse `plugins/harness/skills/harness/` as the source skill.
3. Run the bundled scripts against the current project to search references and scaffold outputs.

See [PUBLISHING.md](PUBLISHING.md) for the full repo marketplace, personal marketplace, and public release guidance.

## Repo Layout

```text
codex-harness/
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── plugins/
│   └── harness/
│       ├── .codex-plugin/
│       │   └── plugin.json
│       └── skills/
│           └── harness/
│               ├── SKILL.md
│               ├── agents/openai.yaml
│               ├── references/
│               │   ├── architecture-patterns.md
│               │   ├── reference-library.md
│               │   ├── orchestrator-template.md
│               │   ├── team-examples.md
│               │   ├── skill-writing-guide.md
│               │   ├── skill-testing-guide.md
│               │   └── qa-agent-guide.md
│               └── scripts/
│                   ├── find_reference_harness.py
│                   └── scaffold_harness.py
├── examples/
│   └── code-reviewer/
│       ├── spec.json
│       ├── AGENTS.md
│       ├── .agents/...
│       └── .codex/...
│   └── fullstack-webapp/
│       ├── spec.json
│       ├── AGENTS.md
│       ├── .agents/...
│       └── .codex/...
└── README.md
```

## Usage

Trigger the plugin or skill with prompts like:

```text
하네스 구성해줘
이 프로젝트에 맞는 에이전트 팀 설계해줘
research harness 만들어줘
코드 리뷰 하네스 만들어줘
fullstack-webapp 하네스 설계해줘
```

### Collaboration Patterns

| Pattern | Best For |
|--------|----------|
| Pipeline | Sequential dependent stages |
| Fan-out / Fan-in | Parallel analysis followed by synthesis |
| Expert Pool | Conditional specialist routing |
| Generate-Critique | Producer plus reviewer |
| Supervisor | Dynamic orchestration based on findings |
| Hierarchical Delegation | Large, multi-layer work trees |

### Typical Output

Generated files for a target project should look like:

```text
your-project/
├── AGENTS.md
├── .agents/
│   └── skills/
│       ├── orchestrator/
│       │   └── SKILL.md
│       └── supporting-skill/
│           └── SKILL.md
└── .codex/
    ├── config.toml
    └── agents/
        ├── researcher.toml
        ├── researcher.md
        ├── reviewer.toml
        └── reviewer.md
```

## Reference Search

Use the bundled search script before designing a harness from scratch:

```bash
python3 plugins/harness/skills/harness/scripts/find_reference_harness.py "code review" --limit 5
python3 plugins/harness/skills/harness/scripts/find_reference_harness.py "youtube seo thumbnail" --language ko
```

This scans `codex-harness-100` and returns the closest harnesses to inspect.

## Scaffolding

Generate a new harness from a JSON spec:

```bash
python3 plugins/harness/skills/harness/scripts/scaffold_harness.py \
  --spec /tmp/harness-spec.json \
  --target .
```

The scaffold script creates:

- `AGENTS.md`
- `.agents/skills/<skill>/SKILL.md`
- `.codex/config.toml`
- `.codex/agents/<role>.toml`
- `.codex/agents/<role>.md`

It also normalizes names into Codex-friendly slugs so the generated config and file paths stay aligned.

## Example Output

A generated sample harness lives at `examples/code-reviewer/`. It includes:

- the input scaffold spec in `examples/code-reviewer/spec.json`
- generated `AGENTS.md`
- generated `.agents/skills/`
- generated `.codex/` role configs

Another generated sample lives at `examples/fullstack-webapp/` and exercises a more sequential delivery workflow with architecture, frontend, backend, QA, and deployment roles.

## Example Use Cases

**Deep Research**

```text
Build a harness for deep research. I need a team that can investigate any topic
from multiple angles, cross-check sources, and produce a structured report.
```

**Website Development**

```text
풀스택 웹사이트 개발 하네스를 구성해줘. 디자인, 프론트엔드, 백엔드, QA를
와이어프레임부터 배포까지 조율하는 구조가 필요해.
```

**Code Review**

```text
종합 코드 리뷰 하네스를 구성해줘. 아키텍처, 보안, 성능, 코드 스타일을 병렬로
점검하고 마지막에 결과를 하나의 보고서로 통합해줘.
```

**Content Production**

```text
Build a harness for YouTube content production. The team should research topics,
write scripts, optimize SEO, and plan thumbnails with a clear review step.
```

## Scope

This repository is the harness generator. The prebuilt harness catalog belongs in `codex-harness-100`.

## Official References

- [Codex Plugins](https://developers.openai.com/codex/plugins/)
- [Build plugins](https://developers.openai.com/codex/plugins/build)
- [Config reference](https://developers.openai.com/codex/config-reference/#configtoml)

## License

Apache 2.0
