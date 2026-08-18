import { test, describe } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

import { scoreProject, ESCAPE_THRESHOLD, CATEGORIES } from "../scripts/maturity.mjs";

function buildFixture(overrides = {}) {
  const dir = mkdtempSync(join(tmpdir(), "mehmet-fixture-"));
  const write = (rel, content) => {
    const path = join(dir, rel);
    mkdirSync(join(path, ".."), { recursive: true });
    writeFileSync(path, content);
  };

  write("README.md", "# test\n\n## Özellikler\n\n## Kurulum\n\n## Lisans\n\nGPLv3\n");
  write("CHANGELOG.md", "# Changelog\n\n## [1.0.0] - 2026-01-01\n\n### Added\n- x\n");
  write("PERSONALITY.md", "# Personality\n\n## Evolution\n\n| Iterasyon | Tarih | İlerleme |\n|---|---|---|\n| 1 | 2026-01-01 | a |\n| 2 | 2026-01-02 | b |\n| 3 | 2026-01-03 | c |\n");
  write("AGENTS.md", "# Simülasyon Bağlamı\n\nKurallar\n");
  write("LICENSE", "GPL-3.0\n");
  write(".gitignore", "node_modules/\n");
  write("package.json", JSON.stringify({ name: "test", version: "1.0.0", type: "module", scripts: { test: "node --test", validate: "node scripts/validate.mjs" }, engines: { node: ">=20" } }));
  write("opencode.json", JSON.stringify({ $schema: "https://opencode.ai/config.json", model: "opencode/deepseek-v4-flash-free" }));
  write("scripts/validate.mjs", "export function validateProject() { return { valid: true, issues: [], ok: [] }; }\n");
  write("test/a.test.mjs", "import { test } from 'node:test';\n");
  write("test/b.test.mjs", "import { test } from 'node:test';\n");
  write("test/c.test.mjs", "import { test } from 'node:test';\n");
  write("test/d.test.mjs", "import { test } from 'node:test';\n");
  write(".github/workflows/opencode.yml", "name: mehmet\nconcurrency:\n  group: ${{ github.ref }}\n  cancel-in-progress: true\n");
  write(".github/workflows/ci.yml", "name: ci\njobs:\n  check:\n    runs-on: ubuntu-latest\n    steps:\n      - run: npm test\n");
  write("docs/design.md", "# design\n");

  if (overrides.remove) {
    for (const rel of overrides.remove) rmSync(join(dir, rel), { recursive: true, force: true });
  }
  return dir;
}

describe("scoreProject", () => {
  test("tam proje eskabe eşiğini aşar", () => {
    const dir = buildFixture();
    try {
      const report = scoreProject(dir);
      assert.ok(report.total >= ESCAPE_THRESHOLD, `skor ${report.total} eşiği geçmeli`);
      assert.equal(report.escaped, true);
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });

  test("boş dizin sıfır skor verir ve kaçış sağlanamaz", () => {
    const dir = mkdtempSync(join(tmpdir(), "mehmet-empty-"));
    try {
      const report = scoreProject(dir);
      assert.equal(report.total, 0);
      assert.equal(report.escaped, false);
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });

  test("test dosyası eksikse testing puanı düşer", () => {
    const dir = buildFixture({ remove: ["test"] });
    try {
      const report = scoreProject(dir);
      assert.equal(report.breakdown.testing.raw, 20);
      assert.equal(report.escaped, false);
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });

  test("tüm kategoriler raporda yer alır", () => {
    const dir = buildFixture();
    try {
      const report = scoreProject(dir);
      for (const key of Object.keys(CATEGORIES)) {
        assert.ok(key in report.breakdown, `${key} kategorisi olmalı`);
      }
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });

  test("ESCAPE_THRESHOLD 80'dir", () => {
    assert.equal(ESCAPE_THRESHOLD, 80);
  });
});