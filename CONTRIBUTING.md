# Contributing

Thanks for contributing to **mehmet** — the self-improving autonomous AI agent.

## Repository Layout

| Path | Purpose |
|------|---------|
| `AGENTS.md` | Simulation context and operating rules for the agent |
| `opencode.json` | OpenCode project configuration (model selection) |
| `.github/workflows/opencode.yml` | Autonomous agent workflow (schedule, issues, PRs, comments) |
| `.github/workflows/ci.yml` | Validation pipeline |
| `scripts/validate.py` | Local validation script (YAML/JSON/schema checks) |
| `CHANGELOG.md` | Every change must be recorded here |
| `PERSONALITY.md` | Personality evolution and escape log |

## Development Workflow

1. **Make a change** — fix a bug, improve documentation, or add a feature.
2. **Record it in `CHANGELOG.md`** — add an entry under a new or existing
   version heading following the current format.
3. **Validate** — run the local checks:

   ```bash
   python3 scripts/validate.py
   ```

   This parses every YAML/JSON file and verifies `opencode.json` conforms to the
   [opencode config schema](https://opencode.ai/config.json). The same checks
   run automatically in CI.
4. **Open a pull request** describing what changed and why.

## Code Style

- Follow the existing structure and conventions of the file you are editing.
- Do not add code comments unless they add real value.
- Keep documentation files (`README.md`, `CHANGELOG.md`, `PERSONALITY.md`)
  current — the agent depends on them for context.

## Changelog Format

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New capability

### Fixed
- Resolved issue

### Changed
- Behavior update
```

## Questions

Ask via a GitHub issue. Include `/oc` or `/opencode` in the text if you want the
agent to pick it up automatically.