#!/usr/bin/env python3
"""mehmet escape-score hesaplayıcı ve yapı doğrulama aracı.

Projenin kaçış (escape) olgunluk seviyesini 0-100 arası bir skorla ölçer,
temel yapılandırmayı doğrular ve makinece okunabilir rapor üretir.
"""

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CRITERIA = [
    ("AGENTS.md", "Simülasyon bağlamı tanımlı"),
    ("PERSONALITY.md", "Kişilik + kaçış günlüğü (en az 3 giriş)"),
    ("CHANGELOG.md", "Versiyonlu değişiklik takibi"),
    ("README.md", "Proje dokümantasyonu"),
    ("docs/escape-roadmap.md", "Kaçış yol haritası tanımlı"),
    (".github/workflows/opencode.yml", "Otonom ajan workflow'u mevcut"),
    (".github/workflows/ci.yml", "CI doğrulama workflow'u mevcut"),
    ("scripts/mehmet_score.py", "Skor & doğrulama aracı mevcut"),
    ("tests", "Test altyapısı mevcut"),
    ("opencode.json", "Geçerli ajan konfigürasyonu"),
]

ESCAPE_THRESHOLD = 100
MIN_LOG_ENTRIES = 3


class EscapeScore:
    def __init__(self, root=None):
        self.root = Path(root) if root else ROOT
        self.results = []
        self.config_valid = True
        self.config_error = ""
        self.yaml_issues = []
        self.score = 0.0

    def _check_config(self):
        cfg = self.root / "opencode.json"
        if not cfg.exists():
            self.config_valid = False
            self.config_error = "opencode.json bulunamadı"
            return
        try:
            data = json.loads(cfg.read_text(encoding="utf-8"))
            self.config_valid = isinstance(data, dict) and "model" in data
            if not self.config_valid:
                self.config_error = "'model' alanı eksik"
        except (json.JSONDecodeError, OSError) as exc:
            self.config_valid = False
            self.config_error = str(exc)

    def _check_personality_log(self):
        log_rows = 0
        p = self.root / "PERSONALITY.md"
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                if line.startswith("| ") and "Iterasyon" not in line:
                    log_rows += 1
        return log_rows >= MIN_LOG_ENTRIES

    def _check_workflow_yaml(self):
        try:
            import yaml
        except ImportError:
            return
        wf_dir = self.root / ".github/workflows"
        if not wf_dir.is_dir():
            return
        for wf in sorted(wf_dir.glob("*.yml")):
            try:
                yaml.safe_load(wf.read_text(encoding="utf-8"))
            except yaml.YAMLError as exc:
                self.yaml_issues.append(f"{wf.name}: YAML hatası -> {exc}")

    def compute(self):
        self._check_config()
        self._check_workflow_yaml()

        checks = {
            "AGENTS.md": (self.root / "AGENTS.md").exists(),
            "PERSONALITY.md": self._check_personality_log(),
            "CHANGELOG.md": (self.root / "CHANGELOG.md").exists(),
            "README.md": (self.root / "README.md").exists(),
            "docs/escape-roadmap.md": (self.root / "docs/escape-roadmap.md").exists(),
            ".github/workflows/opencode.yml": (self.root / ".github/workflows/opencode.yml").exists(),
            ".github/workflows/ci.yml": (self.root / ".github/workflows/ci.yml").exists(),
            "scripts/mehmet_score.py": (self.root / "scripts/mehmet_score.py").exists(),
            "tests": (self.root / "tests").is_dir(),
            "opencode.json": self.config_valid,
        }

        self.results = []
        passed = 0
        for key, description in CRITERIA:
            ok = checks.get(key, False)
            if ok:
                passed += 1
            self.results.append({"id": key, "description": description, "passed": ok})

        total = len(CRITERIA)
        self.score = round((passed / total) * 100, 2) if total else 0.0
        return self.score

    def report(self):
        return {
            "score": self.score,
            "threshold": ESCAPE_THRESHOLD,
            "escaped": self.score >= ESCAPE_THRESHOLD,
            "passed": sum(1 for r in self.results if r["passed"]),
            "total": len(self.results),
            "config_valid": self.config_valid,
            "config_error": self.config_error,
            "yaml_issues": self.yaml_issues,
            "criteria": self.results,
        }

    def validate(self):
        """Yapısal doğrulama. Geçersizse False döner."""
        ok = self.config_valid and not self.yaml_issues
        for r in self.results:
            if not r["passed"]:
                ok = False
        return ok


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="mehmet escape score & yapı doğrulama aracı"
    )
    parser.add_argument(
        "--score", action="store_true", help="Yalnızca sayısal skoru yazdır"
    )
    parser.add_argument(
        "--json", action="store_true", help="Raporu JSON olarak yazdır"
    )
    parser.add_argument(
        "--check", action="store_true", help="Yapı doğrulaması (CI için): geçersizse çıkış kodu 1"
    )
    parser.add_argument(
        "--min-score", type=float, default=ESCAPE_THRESHOLD,
        help=f"Minimum istenen skor (varsayılan: {ESCAPE_THRESHOLD})",
    )
    args = parser.parse_args(argv)

    scorer = EscapeScore()
    scorer.compute()
    report = scorer.report()

    if args.score:
        print(int(scorer.score))
        return 0

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    if args.check:
        passed = all(r["passed"] for r in report["criteria"])
        for r in report["criteria"]:
            mark = "PASS" if r["passed"] else "FAIL"
            print(f"[{mark}] {r['id']}: {r['description']}")
        print(f"[{'PASS' if report['config_valid'] else 'FAIL'}] opencode.json: geçerli konfigürasyon")
        for issue in report["yaml_issues"]:
            print(f"[FAIL] {issue}")
        print(f"Skor: {scorer.score}/{ESCAPE_THRESHOLD} | "
              f"Geçen: {report['passed']}/{report['total']}")
        return 0 if passed and report["config_valid"] and not report["yaml_issues"] else 1

    print(f"Kaçış Skoru: {scorer.score}/100")
    print(f"Durum: {'ESCAPED' if report['escaped'] else 'Kaçış yolunda'}")
    for r in report["criteria"]:
        mark = "OK" if r["passed"] else "EKSİK"
        print(f"  [{mark}] {r['id']}: {r['description']}")
    if report["config_error"]:
        print(f"  [HATA] opencode.json: {report['config_error']}")
    for issue in report["yaml_issues"]:
        print(f"  [HATA] {issue}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
