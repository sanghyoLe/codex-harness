<p align="center">
  <img src="harness_banner.png" alt="Harness Banner" width="600">
</p>

# Codex Harness

**Workflow-Architecture Factory for Codex**

Project-specific harness generator for `AGENTS.md` pointers, repo-local skills, reusable Codex custom agent roles, validation gates, and harness evolution history.

**English** | [Korean](README_KO.md)  
[Publishing Guide](PUBLISHING.md) | [Korean Publishing Guide](PUBLISHING_KO.md)

This repository adapts the upstream `harness` project into a Codex-native plugin and meta skill. The goal is the same: when a user says "set up a harness" or "build a harness for this project", Codex should analyze the domain, choose a workflow-architecture pattern, define specialist roles, and scaffold a reusable harness for the current repository.

## Origin

This repository adapts [revfactory/harness](https://github.com/revfactory/harness) for Codex.

The original idea and overall structure came from that project, while this repository focuses on Codex-native outputs such as `AGENTS.md`, `.agents/skills/`, `.codex/agents/`, and `.codex/config.toml`.

## Ask Codex To Reference This Repo

The intended usage is not "clone this repo and manually copy files." The simpler workflow is to ask Codex to build a new harness while using `codex-harness` as the reference repository.

Tell Codex to inspect this repo, look at the included examples, and generate a harness for your target domain in the same style.

Example prompt:

```text
Use `codex-harness` as a reference and build a harness for a web service that helps users plan trips in Japan.
```

That is the core pattern: ask Codex to use `codex-harness` as the reference, then describe the product or workflow you want the new harness to support.

## Quick Install

Today, the practical install paths are `repo marketplace` or `personal marketplace`. Official self-serve publishing to the public Codex Plugin Directory is not available yet.

### Option 1: Install into one repo

Use this when a group wants `codex-harness` only inside one project.

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
- project-scoped custom agent files under `.codex/agents/`
- Codex configuration in `.codex/config.toml`

Generated harnesses commonly also use a repo-local `_workspace/` directory for intermediate artifacts, handoff notes, per-run working files, and harness change history. That folder is local scratch state for the current repository, not a source directory or shared package, so in most projects it should be treated as disposable and added to `.gitignore`.

`AGENTS.md` is now treated as a pointer, not the source of truth. The detailed agent and skill instructions live in `.codex/agents/` and `.agents/skills/`; `AGENTS.md` should keep trigger rules, key paths, and change history short enough to stay useful across sessions.

When the sibling repository `codex-harness-100` is available (see the search script for candidate paths), this plugin should treat that catalog as its primary reference library instead of inventing structures from scratch.

## Category — Where Harness Sits

This repository is the Codex runtime port of the original workflow-architecture factory. It sits at the meta-factory layer: a harness that generates other project harnesses.

| Layer | What it does | Codex output |
|-------|--------------|--------------|
| Meta-factory | Domain request -> architecture pattern + roles + skills | `AGENTS.md`, `.agents/skills/`, `.codex/agents/` |
| Project harness | Reusable workflow for one repository | Orchestrator skill + custom agent roles |
| Runtime config | Local Codex behavior and search/agent policy | `.codex/config.toml` |

The upstream project uses a different runtime vocabulary. This port keeps the architecture patterns and evolution workflow, but emits Codex-native files and explicit subagent workflow instructions.

## Key Features

- **Workflow Architecture Design**: choose among pipeline, fan-out/fan-in, expert pool, producer-reviewer, supervisor, hierarchical delegation, and hybrid execution
- **Existing Harness Audit**: detect whether the request is a new build, extension, or maintenance/sync task before writing files
- **Reference-First Generation**: search `codex-harness-100`, inspect nearby examples, then adapt deliberately
- **Codex-Native Output**: generate `AGENTS.md`, repo-local skills, and `.codex` custom agent configs using Codex project instructions, skills, and custom agents
- **Reusable Scaffolding**: bundled scripts help search references and scaffold a new harness from a JSON spec
- **Validation and Evolution**: generated harnesses include role boundaries, workflow phases, output expectations, checks for unresolved placeholders, and a feedback loop for future updates

## Workflow

```text
Phase 0: Existing Harness Audit + Reference Search
    ↓
Phase 1: Domain Analysis
    ↓
Phase 2: Workflow Architecture Design
    ↓
Phase 3: Harness Spec Definition
    ↓
Phase 4: Subagent Role Definition (.codex/agents/)
    ↓
Phase 5: Skill Generation + Orchestration
    ↓
Phase 6: Validation
    ↓
Phase 7: Harness Evolution / Maintenance
```

## Relationship To `codex-harness-100`

These two repositories serve different roles:

- `codex-harness`: generator plugin and meta skill
- `codex-harness-100`: companion reference library of completed harness examples

Recommended workflow:

1. Ask Codex to build a harness for the current repo.
2. If `codex-harness-100` is available, let the `harness` skill search it for the closest existing patterns. If not, `codex-harness` should still generate a harness without the reference library.
3. Inspect the top 1 to 3 matching harnesses.
4. Adapt the workflow shape, outputs, and skill structure to the current project.
5. Scaffold and refine the new local harness.

## Installation

The official Codex plugin docs support three relevant surfaces for this project:

1. the curated Plugin Directory inside Codex
2. a repo marketplace at `$REPO_ROOT/.agents/plugins/marketplace.json`
3. a personal marketplace at `~/.agents/plugins/marketplace.json`

Today, `codex-harness` is ready for repo and personal marketplace distribution. Official self-serve public publishing to the Codex Plugin Directory is still coming soon.

### Repo marketplace

Use this when a group wants the plugin available inside a single repository.

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

## Quickstart

See [docs/quickstart.md](docs/quickstart.md) for a short local workflow. For deterministic smoke testing, run:

```bash
python3 plugins/harness/skills/harness/scripts/scaffold_harness.py \
  --spec examples/code-reviewer/spec.json \
  --target /tmp/codex-harness-demo
```

See [docs/experimental-dependency.md](docs/experimental-dependency.md) for the Codex runtime assumptions behind the generated files.

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
│               │   ├── agent-design-patterns.md
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
├── docs/
│   ├── quickstart.md
│   └── experimental-dependency.md
├── examples/
│   ├── code-reviewer/
│   │   ├── spec.json
│   │   ├── AGENTS.md
│   │   ├── .agents/...
│   │   └── .codex/...
│   └── fullstack-webapp/
│   │   ├── spec.json
│   │   ├── AGENTS.md
│   │   ├── .agents/...
│   │   └── .codex/...
└── README.md
```

## Usage

Trigger the plugin or skill with prompts like:

```text
Set up a harness for this repository.
Design a Codex subagent workflow for this project.
Build a research harness.
Build a code review harness.
Design a fullstack webapp harness.
```

### Workflow Patterns

| Pattern | Best For |
|--------|----------|
| Pipeline | Sequential dependent stages |
| Fan-out / Fan-in | Parallel analysis followed by synthesis |
| Expert Pool | Conditional specialist routing |
| Producer-Reviewer | Producer plus reviewer |
| Supervisor | Dynamic orchestration based on findings |
| Hierarchical Delegation | Large, multi-layer work trees |
| Hybrid | Different execution modes by phase |

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

Add `"language": "ko"` to `spec.json` if you want the built-in template copy rendered in Korean. If omitted, the default remains English (`"en"`).
If you set `"web_search"`, use only `"cached"`, `"live"`, or `"disabled"`. If omitted, the default is `"disabled"`.

The scaffold script creates:

- `AGENTS.md`
- `.agents/skills/<skill>/SKILL.md`
- `.codex/config.toml`
- `.codex/agents/<role>.toml`

Each generated `.codex/agents/<role>.toml` follows the current Codex custom agent schema and defines `name`, `description`, and `developer_instructions` directly in the TOML file.

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
Build a harness for deep research. I need a Codex subagent workflow that can investigate any topic
from multiple angles, cross-check sources, and produce a structured report.
```

**Website Development**

```text
Build a harness for full-stack website development. I need a structure that
coordinates design, frontend, backend, and QA from wireframes through deployment.
```

**Code Review**

```text
Build a comprehensive code review harness. It should check architecture,
security, performance, and code style in parallel, then merge the results into one report.
```

**Content Production**

```text
Build a harness for YouTube content production. The workflow should research topics,
write scripts, optimize SEO, and plan thumbnails with a clear review step.
```

## Scope

This repository is the harness generator. The prebuilt harness catalog belongs in `codex-harness-100`.

## Official References

- [Codex Plugins](https://developers.openai.com/codex/plugins/)
- [Build plugins](https://developers.openai.com/codex/plugins/build)
- [Codex Subagents](https://developers.openai.com/codex/subagents)
- [Codex Skills](https://developers.openai.com/codex/skills)
- [Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md)
- [Config reference](https://developers.openai.com/codex/config-reference/#configtoml)

## License

Apache 2.0
