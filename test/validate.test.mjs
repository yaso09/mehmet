import { test, describe } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, writeFileSync, rmSync, mkdirSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

import { validateProject } from "../scripts/validate.mjs";

function writeTree(root, files) {
  for (const [rel, content] of Object.entries(files)) {
    const path = join(root, rel);
    mkdirSync(join(path, ".."), { recursive: true });
    writeFileSync(path, content);
  }
}

const COMPLETE = {
  "AGENTS.md": "# Simülasyon\n",
  "CHANGELOG.md": "# Changelog\n\n## [1.0.0] - 2026-01-01\n\n### Added\n- x\n",
  "PERSONALITY.md": "# Personality\n\n| Iterasyon | Tarih | İlerleme |\n|---|---|---|\n| 1 | 2026-01-01 | a |\n| 2 | 2026-01-02 | b |\n| 3 | 2026-01-03 | c |\n",
  "README.md": "# test\n\n## Özellikler\n\n## Kurulum\n\n## Lisans\n\nGPLv3\n",
  "opencode.json": JSON.stringify({ model: "opencode/deepseek-v4-flash-free" }),
  "package.json": JSON.stringify({ name: "test", version: "1.0.0", scripts: { test: "node --test", validate: "node scripts/validate.mjs" } }),
  ".gitignore": "node_modules/\n",
  "LICENSE": "GPL-3.0\n",
  ".github/workflows/opencode.yml": "name: mehmet\n",
};

describe("validateProject", () => {
  test("eksiksiz proje geçer", () => {
    const dir = mkdtempSync(join(tmpdir(), "mehmet-valid-"));
    try {
      writeTree(dir, COMPLETE);
      const result = validateProject(dir);
      assert.equal(result.valid, true);
      assert.deepEqual(result.issues, []);
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });

  test("eksik dosya tespit edilir", () => {
    const dir = mkdtempSync(join(tmpdir(), "mehmet-missing-"));
    try {
      const files = { ...COMPLETE };
      delete files.LICENSE;
      writeTree(dir, files);
      const result = validateProject(dir);
      assert.equal(result.valid, false);
      assert.ok(result.issues.some((i) => i.includes("LICENSE")));
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });

  test("sürüm uyumsuzluğu tespit edilir", () => {
    const dir = mkdtempSync(join(tmpdir(), "mehmet-version-"));
    try {
      writeTree(dir, {
        ...COMPLETE,
        "package.json": JSON.stringify({ name: "test", version: "2.0.0", scripts: { test: "node --test", validate: "node scripts/validate.mjs" } }),
      });
      const result = validateProject(dir);
      assert.equal(result.valid, false);
      assert.ok(result.issues.some((i) => i.includes("Sürüm uyumsuzluğu")));
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });

  test("README eksik bölüm tespit edilir", () => {
    const dir = mkdtempSync(join(tmpdir(), "mehmet-readme-"));
    try {
      writeTree(dir, { ...COMPLETE, "README.md": "# test\n" });
      const result = validateProject(dir);
      assert.equal(result.valid, false);
      assert.ok(result.issues.some((i) => i.includes("## Kurulum")));
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });
});