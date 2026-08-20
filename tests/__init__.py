"""Shared test helpers for the mehmet project."""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def repo_path(*parts):
    return REPO_ROOT.joinpath(*parts)


def read_text(rel_path):
    path = repo_path(*rel_path.split("/"))
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def load_json(rel_path):
    text = read_text(rel_path)
    if text is None:
        return None
    return json.loads(text)


def valid_opencode_keys():
    """The set of top-level keys opencode accepts in opencode.json.

    Mirrors https://opencode.ai/config.json (ConfigV2). Keeping the list
    locally lets CI validate config without a network dependency; add new
    keys here when the schema grows.
    """
    return {
        "$schema", "shell", "logLevel", "server", "command", "skills",
        "references", "reference", "watcher", "snapshot", "plugin", "share",
        "autoshare", "autoupdate", "disabled_providers", "enabled_providers",
        "model", "small_model", "default_agent", "subagent_depth", "username",
        "mode", "agent", "provider", "mcp", "formatter", "lsp", "instructions",
        "layout", "permission", "tools", "attachment", "enterprise",
        "tool_output", "compaction", "experimental",
    }


def try_import_yaml():
    try:
        import yaml  # noqa: PLC0415
        return yaml
    except ImportError:  # pragma: no cover
        return None
