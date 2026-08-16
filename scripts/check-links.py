#!/usr/bin/env python3
"""Check relative links inside markdown files resolve to existing paths.

Usage: check-links.py <root> [--include <glob>]

Skips external URLs (http/https/mailto), pure anchors (#...), and links that
point into ignored directories (node_modules, .git).
"""
import os
import re
import sys

LINK_RE = re.compile(r"(?P<alt>!)?\[[^\]]*\]\((?P<url>[^)\s]+)")
IGNORED_DIRS = {".git", "node_modules", "dist", "build"}


def is_external(url: str) -> bool:
    return bool(re.match(r"^(https?|mailto|ftp):", url)) or url.startswith("//")


def check_file(root: str, path: str, errors: list) -> None:
    base = os.path.dirname(path)
    with open(path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            for m in LINK_RE.finditer(line):
                url = m.group("url")
                if is_external(url) or url.startswith("#"):
                    continue
                # split off anchor/fragment
                target = url.split("#", 1)[0]
                if not target:
                    continue
                resolved = os.path.normpath(os.path.join(base, target))
                if any(part in IGNORED_DIRS for part in target.split("/")):
                    continue
                if not os.path.exists(resolved):
                    rel = os.path.relpath(resolved, root)
                    errors.append(f"{path}:{lineno}: broken link -> {url} (missing {rel})")


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print("usage: check-links.py <root>", file=sys.stderr)
        return 2
    root = args[0]
    errors = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        for name in filenames:
            if name.endswith(".md"):
                check_file(root, os.path.join(dirpath, name), errors)
    for e in errors:
        print(f"  [FAIL] {e}")
    if errors:
        print(f"FAIL: {len(errors)} broken link(s)")
        return 1
    print("  [PASS] all markdown links resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())