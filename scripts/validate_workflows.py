#!/usr/bin/env python3
"""Workflow YAML dosyalarını doğrular."""

import glob
import sys

try:
    import yaml
except ImportError:
    print("[FAIL] PyYAML kurulu değil. Kur: pip install pyyaml")
    sys.exit(1)


def main():
    failed = False
    paths = sorted(glob.glob(".github/workflows/*.yml"))
    if not paths:
        print("[FAIL] workflow dosyası bulunamadı")
        return 1
    for path in paths:
        with open(path, encoding="utf-8") as fh:
            try:
                yaml.safe_load(fh)
                print(f"[OK] {path}")
            except yaml.YAMLError as exc:
                failed = True
                print(f"[FAIL] {path}: {exc}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())