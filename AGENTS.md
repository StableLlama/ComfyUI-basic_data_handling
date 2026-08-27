# AGENTS.md

Guidance for AI coding assistants working in this repository.

## Project overview

`basic_data_handling` is a **ComfyUI custom-node pack**: lightweight Python nodes for common data
manipulation (boolean logic, casting, comparison, control flow, lists, dicts, sets, strings, math,
paths, regex, tensors, time). It has no runtime dependencies beyond ComfyUI itself.

## Repository layout

- `src/basic_data_handling/` — node implementations; each `*_nodes.py` module registers its nodes.
- `tests/` — pytest suite mirroring the `src/` modules.
- `web/` — frontend assets (icon, JS).
- `pyproject.toml` — package metadata, Comfy registry config (`[tool.comfy]`), and tool config
  (ruff / mypy / pytest).
- `CHANGELOG.md` — release notes in Keep-a-Changelog format; the publish workflow reads the section
  matching the current version.
- `.github/workflows/` — CI (`build-pipeline.yml`, `validate.yml`) and registry publishing
  (`publish_node.yml`).

## Versioning & releases (IMPORTANT)

- **Single source of truth:** `[project] version` in `pyproject.toml`. There is intentionally **no**
  `bump-my-version` config — do **not** re-add one; it only duplicates the version string and causes drift.
- To release a new version:
  1. Bump `[project] version` in `pyproject.toml` (semver: MAJOR = breaking, MINOR = feature, PATCH = fix).
  2. Add a `## [X.Y.Z] - YYYY-MM-DD` section to `CHANGELOG.md` (Keep-a-Changelog format).
  3. Push to `main`. `.github/workflows/publish_node.yml` auto-triggers on any push touching
     `pyproject.toml` and publishes to the Comfy registry.
- **Changelog → registry:** the publish workflow extracts the `## [X.Y.Z]` section from `CHANGELOG.md`
  and sends it via `comfy node publish --changelog-file`. That text is what shows under
  **Version history** on the registry page. Published versions are immutable, so the changelog only
  appears for the newly published version.
- Registry metadata lives in `[tool.comfy]` (`PublisherId = "stablellama"`, `DisplayName`, `Icon`).
  The `name` and `Repository` URL must stay stable — they are the registry node ID.

## Tooling

Python venv (repo lives under `ComfyUI/custom_nodes`): `<repo>/../../venv/bin/python`

- Lint: `python -m ruff check .`
- Format: `python -m ruff format .`
- Type check: `python -m mypy .` (strict)
- Tests: `python -m pytest tests/`
- Pre-commit: `python -m pre_commit run --all-files`

## Workflow / commit policy

- The human reviews and commits all changes (commits are GPG-signed). Do **not** run `git commit`
  yourself; make the changes, optionally stage them, and hand off to the user.
