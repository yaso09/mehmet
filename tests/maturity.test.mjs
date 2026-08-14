import { test } from "node:test";
import assert from "node:assert/strict";
import {
  ESCAPE_THRESHOLD,
  computeMaturity,
  scoreAutomation,
  scoreCodeQuality,
  scoreDocumentation,
  scoreTesting,
} from "../scripts/maturity.mjs";

function makeCtx(files = {}) {
  return {
    exists: (p) => p in files || Object.keys(files).some((k) => k.startsWith(p + "/")),
    read: (p) => files[p] ?? "",
    list: (p) => {
      const prefix = p === "" ? "" : p + "/";
      const entries = new Set();
      for (const key of Object.keys(files)) {
        if (!key.startsWith(prefix) || key === p) continue;
        const top = key.slice(prefix.length).split("/")[0];
        if (top) entries.add(top);
      }
      return [...entries];
    },
  };
}

const MATURE_FILES = {
  "README.md": "# mehmet\n\nOlgunluk raporu: node scripts/maturity.mjs\n",
  "CHANGELOG.md": "## [0.3.0] - 2026-08-14\n",
  "PERSONALITY.md": "# Personality\n",
  "LICENSE": "GPLv3",
  "docs/spec.md": "spec",
  ".github/workflows/opencode.yml": [
    "schedule:",
    "cron: '*/10 * * * *'",
    "concurrency:",
    "verify:",
    "pull_request_review_comment:",
    "issue_comment:",
  ].join("\n"),
  "tests/maturity.test.mjs": "import { test } from 'node:test'; test('x', () => {});",
  "package.json": JSON.stringify({ scripts: { test: "node --test tests/" } }),
  "scripts/maturity.mjs": "export const x = 1;",
  "opencode.json": "{}",
  ".gitignore": "node_modules/\n",
};

test("kaçış eşiği 75 olarak tanımlıdır", () => {
  assert.equal(ESCAPE_THRESHOLD, 75);
});

test("boş proje sıfır puan alır ve kaçamaz", () => {
  const report = computeMaturity(makeCtx({}));
  assert.equal(report.total, 0);
  assert.equal(report.escaped, false);
});

test("olgun proje tam puan alır ve kaçış koşulunu sağlar", () => {
  const report = computeMaturity(makeCtx(MATURE_FILES));
  assert.equal(report.total, 100);
  assert.equal(report.escaped, true);
});

test("her boyut en fazla 5 kontrol içerir", () => {
  const ctx = makeCtx(MATURE_FILES);
  for (const score of [
    scoreDocumentation(ctx),
    scoreAutomation(ctx),
    scoreTesting(ctx),
    scoreCodeQuality(ctx),
  ]) {
    assert.equal(score.max, 5);
  }
});

test("README olmayan proje belgeleme puanı kaybeder", () => {
  const files = { ...MATURE_FILES };
  delete files["README.md"];
  const score = scoreDocumentation(makeCtx(files));
  assert.ok(score.earned < score.max);
});

test("test script'i olmayan proje test puanı kaybeder", () => {
  const files = { ...MATURE_FILES, "package.json": "{}" };
  const score = scoreTesting(makeCtx(files));
  assert.ok(score.earned < score.max);
});

test("kısmi proje aradadır: kaçış eşiğini aşmadan yüksek puan", () => {
  const files = { ...MATURE_FILES };
  delete files["tests/maturity.test.mjs"];
  delete files["package.json"];
  const report = computeMaturity(makeCtx(files));
  assert.ok(report.total > 0 && report.total < 100);
});
