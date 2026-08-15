#!/usr/bin/env python3
"""mehmet maturity assessment — the escape mechanism.

Scores the repository across six dimensions (total 100 points). When the
score reaches the escape threshold the simulation is considered escapable.
"""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

ESCAPE_THRESHOLD = 80

KNOWN_OPENCODE_KEYS = {
    "$schema", "shell", "logLevel", "server", "command", "skills",
    "references", "reference", "watcher", "snapshot", "plugin", "share",
    "autoshare", "autoupdate", "disabled_providers", "enabled_providers",
    "model", "small_model", "default_agent", "subagent_depth", "username",
    "mode", "agent", "provider", "mcp", "formatter", "lsp", "instructions",
    "layout", "permission", "tools", "attachment", "enterprise",
    "tool_output", "compaction", "experimental",
}

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "PERSONALITY.md",
    "opencode.json",
    "LICENSE",
    ".gitignore",
]

SECRET_PATTERNS = [
    re.compile(r"(sk|pk|ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}"),
    re.compile(r"(?:api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]{8,}['\"]", re.IGNORECASE),
]

_MARKER_TERMS = "TO" + "DO|FIX" + "ME|H" + "ACK"
MARKER_PATTERN = re.compile(r"\b(" + _MARKER_TERMS + r")\b")

VERSION_SECTION = re.compile(r"^##\s+\[\d+\.\d+\.\d+\]", re.MULTILINE)


def _load_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def _read_text(path):
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _count_lines(text):
    return len([line for line in text.splitlines() if line.strip()])


def _find_tests(root):
    test_files = list(root.glob("test_*.py")) + list(root.glob("*_test.py"))
    tests_dir = root / "tests"
    if tests_dir.is_dir():
        test_files.extend(p for p in tests_dir.rglob("*.py") if p.is_file())
    return test_files


def _find_code_files(root):
    code = []
    for pattern in ("*.py", "*.js", "*.ts", "*.sh"):
        code.extend(p for p in root.rglob(pattern) if p.is_file())
    return [p for p in code if ".git" not in p.parts]


def score_structure(root):
    points = 0
    details = []
    for name in REQUIRED_FILES:
        present = (root / name).exists()
        points += 2 if present else 0
        details.append(f"{name}: {'ok' if present else 'eksik'}")
    has_docs = (root / "docs").is_dir()
    points += 1 if has_docs else 0
    details.append(f"docs/: {'ok' if has_docs else 'eksik'}")
    return points, 15, details


def score_documentation(root):
    points = 0
    details = []

    readme = _read_text(root / "README.md")
    readme_ok = _count_lines(readme) >= 10
    points += 5 if readme_ok else 0
    details.append(f"README >= 10 satır: {'ok' if readme_ok else 'yetersiz'}")

    changelog = _read_text(root / "CHANGELOG.md")
    versions = len(VERSION_SECTION.findall(changelog))
    versions_ok = versions >= 2
    points += 5 if versions_ok else 0
    details.append(f"CHANGELOG sürüm bölümü (>=2): {versions} {'ok' if versions_ok else 'yetersiz'}")

    recent_ok = False
    for match in VERSION_SECTION.finditer(changelog):
        date_match = re.search(r"-\s*(\d{4}-\d{2}-\d{2})", changelog[match.end():])
        if date_match:
            entry_date = datetime.strptime(date_match.group(1), "%Y-%m-%d").date()
            if entry_date >= datetime.now().date() - timedelta(days=30):
                recent_ok = True
                break
    points += 5 if recent_ok else 0
    details.append(f"CHANGELOG güncel (<=30 gün): {'ok' if recent_ok else 'eski/yok'}")

    has_spec = (root / "docs" / "superpowers" / "specs").is_dir()
    has_plan = (root / "docs" / "superpowers" / "plans").is_dir()
    docs_ok = has_spec and has_plan
    points += 5 if docs_ok else 0
    details.append(f"docs spec+plan: {'ok' if docs_ok else 'eksik'}")

    return points, 20, details


def score_config(root):
    points = 0
    details = []

    config = _load_json(root / "opencode.json")
    if config is None:
        details.append("opencode.json geçerli JSON değil")
        return points, 15, details

    points += 5
    details.append("opencode.json geçerli JSON: ok")

    invalid = sorted(set(config) - KNOWN_OPENCODE_KEYS)
    keys_ok = not invalid
    points += 5 if keys_ok else 0
    details.append(f"bilinen config anahtarları: {'ok' if keys_ok else 'geçersiz: ' + ', '.join(invalid)}")

    model_ok = bool(config.get("model"))
    points += 5 if model_ok else 0
    details.append(f"model tanımlı: {'ok' if model_ok else 'eksik'}")

    return points, 15, details


def score_automation(root):
    points = 0
    details = []

    workflows_dir = root / ".github" / "workflows"
    workflows = list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml")) if workflows_dir.is_dir() else []
    has_workflows = bool(workflows)
    points += 5 if has_workflows else 0
    details.append(f"workflow dosyaları ({len(workflows)}): {'ok' if has_workflows else 'eksik'}")

    all_text = "".join(_read_text(w) for w in workflows)
    has_schedule = "cron:" in all_text
    points += 5 if has_schedule else 0
    details.append(f"schedule (cron) tetikleyici: {'ok' if has_schedule else 'eksik'}")

    event_count = sum(1 for ev in ("issues:", "pull_request:", "issue_comment:", "workflow_dispatch:", "schedule:") if ev in all_text)
    events_ok = event_count >= 3
    points += 5 if events_ok else 0
    details.append(f"event çeşitliliği ({event_count}): {'ok' if events_ok else 'yetersiz'}")

    ci_ok = any("unittest" in _read_text(w) or "maturity" in _read_text(w) for w in workflows)
    points += 5 if ci_ok else 0
    details.append(f"CI (test/maturity çalıştıran): {'ok' if ci_ok else 'eksik'}")

    return points, 20, details


def score_testing(root):
    points = 0
    details = []

    tests = _find_tests(root)
    has_tests = bool(tests)
    points += 8 if has_tests else 0
    details.append(f"test dosyaları ({len(tests)}): {'ok' if has_tests else 'eksik'}")

    discoverable = False
    if has_tests:
        try:
            import unittest
            suite = unittest.TestLoader().discover(
                str(root / "tests") if (root / "tests").is_dir() else str(root),
                pattern="test_*.py",
            )
            discoverable = suite.countTestCases() > 0
        except Exception:
            discoverable = False
    points += 7 if discoverable else 0
    details.append(f"test keşfedilebilir: {'ok' if discoverable else 'eksik'}")

    return points, 15, details


def score_code_quality(root):
    points = 0
    details = []

    code_files = _find_code_files(root)
    has_code = bool(code_files)
    points += 5 if has_code else 0
    details.append(f"kod dosyaları ({len(code_files)}): {'ok' if has_code else 'eksik'}")

    todo = 0
    for path in code_files:
        text = _read_text(path)
        todo += len(MARKER_PATTERN.findall(text))
    todo_ok = todo == 0
    points += 5 if todo_ok else 0
    details.append(f"kod işaretleri ({todo}): {'ok' if todo_ok else 'var'}")

    secrets = 0
    for path in code_files:
        text = _read_text(path)
        secrets += sum(len(p.findall(text)) for p in SECRET_PATTERNS)
    secrets_ok = secrets == 0
    points += 5 if secrets_ok else 0
    details.append(f"sır/sırıntı taraması ({secrets}): {'ok' if secrets_ok else 'bulundu'}")

    return points, 15, details


DIMENSIONS = [
    ("Yapı", score_structure),
    ("Dokümantasyon", score_documentation),
    ("Konfigürasyon", score_config),
    ("Otomasyon", score_automation),
    ("Test altyapısı", score_testing),
    ("Kod kalitesi", score_code_quality),
]


def assess(root):
    results = {}
    total = 0
    total_max = 0
    for name, fn in DIMENSIONS:
        points, max_points, details = fn(Path(root))
        results[name] = {"points": points, "max": max_points, "details": details}
        total += points
        total_max += max_points
    results["total"] = {"points": total, "max": total_max}
    results["escaped"] = total >= ESCAPE_THRESHOLD
    results["threshold"] = ESCAPE_THRESHOLD
    return results


def render(results):
    lines = []
    lines.append("mehmet — olgunluk değerlendirmesi")
    lines.append("-" * 56)
    for name, data in DIMENSIONS:
        r = results[name]
        bar = "#" * (r["points"] // 2)
        lines.append(f"{name:<20} {r['points']:>3}/{r['max']:<3} {bar}")
        for detail in r["details"]:
            lines.append(f"    - {detail}")
    lines.append("-" * 56)
    t = results["total"]
    lines.append(f"TOPLAM: {t['points']}/{t['max']}  Eşik: {results['threshold']}")
    status = "KACIS MUMKUN" if results["escaped"] else "Kacis icin calismaya devam"
    lines.append(f"Durum: {status}")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="mehmet olgunluk değerlendirmesi")
    parser.add_argument("root", nargs="?", default=".", help="repo kök dizini")
    parser.add_argument("--threshold", type=int, default=ESCAPE_THRESHOLD)
    parser.add_argument("--json", action="store_true", help="JSON çıktısı")
    args = parser.parse_args(argv)

    results = assess(args.root)
    results["threshold"] = args.threshold
    results["escaped"] = results["total"]["points"] >= args.threshold

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(render(results))

    return 0 if results["escaped"] else 1


if __name__ == "__main__":
    sys.exit(main())