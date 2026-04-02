# Publishing Guide

This document explains the current public distribution story for `codex-harness` using the official Codex plugin model.

## Current Status

`codex-harness` is packaged as a Codex plugin. The current practical distribution paths are:

1. repo marketplace installation
2. personal marketplace installation
3. sharing this repository as an open-source plugin source on GitHub

At the time of writing, official self-serve publishing to the public Codex Plugin Directory is not yet available. The official docs say public plugin publishing is "coming soon".

## Distribution Model

Codex plugins are installable bundles that can package:

- skills
- apps
- MCP server configuration

For `codex-harness`, the primary bundled component is the `harness` skill plus local plugin metadata:

- `plugins/harness/.codex-plugin/plugin.json`
- `.agents/plugins/marketplace.json`

## Recommended Public Distribution

For open-source release today:

1. Publish this repository on GitHub as the canonical plugin source.
2. Keep the plugin folder at `plugins/harness`.
3. Keep a repo-scoped marketplace example in `.agents/plugins/marketplace.json`.
4. Document both repo and personal marketplace installation flows.
5. Position `codex-harness-100` as the companion example library, not part of the install bundle.

## Install From A Repo Marketplace

Use this when a team wants the plugin available only inside one repository.

### Expected layout

```text
$REPO_ROOT/
├── .agents/
│   └── plugins/
│       └── marketplace.json
└── plugins/
    └── harness/
```

### Steps

1. Copy or clone the plugin into `$REPO_ROOT/plugins/harness`.
2. Add or update `$REPO_ROOT/.agents/plugins/marketplace.json`.
3. Make sure the plugin entry points to `./plugins/harness`.
4. Restart Codex.
5. Open the plugin directory and select the repo marketplace.
6. Install `harness`.
7. Start a new thread and ask Codex to use it.

### Repo marketplace example

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

## Install From A Personal Marketplace

Use this when an individual wants `codex-harness` available across many repos.

### Expected layout

```text
~/.agents/plugins/marketplace.json
~/.codex/plugins/harness
```

### Steps

1. Copy or clone the plugin into `~/.codex/plugins/harness`.
2. Add or update `~/.agents/plugins/marketplace.json`.
3. Point the plugin entry to the plugin directory with a `./`-prefixed path relative to the marketplace root.
4. Restart Codex.
5. Open the plugin directory and install `harness` from that marketplace.

## Important Path Rules

These come directly from the Codex plugin docs:

- `source.path` should start with `./`
- `source.path` is resolved relative to the marketplace root
- plugin manifest paths should stay relative to the plugin root
- the required plugin entry point is `.codex-plugin/plugin.json`

## After Installation

After installation:

- bundled skills become available to Codex
- plugin enable or disable state is stored in `~/.codex/config.toml`
- local plugins are installed into the Codex cache rather than executed directly from the marketplace source path

For local plugins, Codex installs into:

```text
~/.codex/plugins/cache/$MARKETPLACE_NAME/$PLUGIN_NAME/local/
```

## Codex App And CLI Entry Points

In the Codex app:

- open `Plugins`
- choose the marketplace
- install `harness`

In Codex CLI:

```text
codex
/plugins
```

Then browse the marketplace and install the plugin.

## Project Trust Requirement

`codex-harness` generates and relies on repo-local `.codex/config.toml` files. Official Codex config docs note that project-scoped `.codex/config.toml` is loaded only when the project is trusted.

That means installation alone is not enough. The target project must also be opened in a trusted state for repo-local agent config to load.

## Companion Repository

`codex-harness-100` should be documented as a companion repository:

- `codex-harness` = generator plugin
- `codex-harness-100` = example and reference library

Do not require `codex-harness-100` for installation. Treat it as an optional but recommended reference dependency.

## Official Docs

- Plugins: https://developers.openai.com/codex/plugins/
- Build plugins: https://developers.openai.com/codex/plugins/build
- Config reference: https://developers.openai.com/codex/config-reference/#configtoml
