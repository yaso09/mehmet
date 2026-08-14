#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> Validating opencode.json..."
python3 -c "import json; json.load(open('opencode.json')); print('  opencode.json: valid')"

echo "==> Validating workflow YAML..."
python3 -c "
import sys
sys.path.insert(0, '.')
from tests.yaml_loader import load_github_workflow
wf = load_github_workflow('.github/workflows/opencode.yml')
assert 'jobs' in wf, 'workflow missing jobs'
assert 'on' in wf, 'workflow missing triggers'
print('  opencode.yml: valid')"

echo "==> Running integrity test suite..."
python3 -m unittest tests.test_project -v

echo "==> All validations passed."