#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "==> Validating JSON configs"
jq empty opencode.json
jq -e '.model == "opencode/deepseek-v4-flash-free"' opencode.json > /dev/null
jq -e '.instructions | index("PERSONALITY.md") != null' opencode.json > /dev/null

echo "==> Validating YAML workflows"
python3 - <<'PY'
import glob
import sys

try:
    import yaml
except ImportError:
    print("PyYAML not available; skipping YAML validation", file=sys.stderr)
    sys.exit(0)

for path in glob.glob(".github/workflows/*.yml"):
    with open(path) as fh:
        yaml.safe_load(fh)
    print("OK", path)
PY

echo "==> Verifying version consistency"
VERSION="$(cat VERSION)"
CHANGELOG_VERSION="$(grep -m1 -oP '(?<=^## \[)[^\]]+' CHANGELOG.md)"
test "$VERSION" = "$CHANGELOG_VERSION"
echo "Version $VERSION matches CHANGELOG."

echo "All checks passed."