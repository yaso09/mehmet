import { test } from "node:test";
import assert from "node:assert/strict";
import { fileURLToPath } from "node:url";
import { evaluate, levelFor, scanRepo, MAX_SCORE, ESCAPE_THRESHOLD, ESCAPE_FINAL_THRESHOLD } from "../src/maturity.js";

test("evaluate: boş faktörler 0 skor ve Seed fazı döner", () => {
  const report = evaluate({});
  assert.equal(report.total, 0);
  assert.equal(report.phase, 0);
  assert.equal(report.name, "Seed");
  assert.equal(report.escape, false);
});

test("evaluate: tam olgun faktörler Escape fazı döner", () => {
  const facts = {
    readme: true,
    changelog: true,
    personality: true,
    agents: true,
    license: true,
    workflowOpenCode: true,
    workflowCi: true,
    gitignore: true,
    srcFiles: 2,
    lintConfig: true,
    cleanCode: true,
    testFiles: 2,
    testsReferenceSrc: true,
    npmTest: true,
    versionedChangelog: true,
  };
  const report = evaluate(facts);
  assert.equal(report.total, MAX_SCORE);
  assert.equal(report.phase, 4);
  assert.equal(report.name, "Escape");
  assert.equal(report.escape, true);
});

test("evaluate: kategori skorları doğru toplanır", () => {
  const facts = {
    readme: true,
    changelog: true,
    personality: true,
    agents: true,
    license: true,
  };
  const report = evaluate(facts);
  assert.equal(report.categories.documentation.earned, 25);
  assert.equal(report.categories.documentation.max, 25);
  assert.equal(report.total, 25);
});

test("evaluate: cleanCode hatalıysa puan verilmez", () => {
  const facts = { srcFiles: 1, cleanCode: false };
  const report = evaluate(facts);
  const clean = report.checks.find((c) => c.id === "clean-code");
  assert.equal(clean.earned, 0);
});

test("levelFor: eşik sınırları doğru", () => {
  assert.equal(levelFor(0).name, "Seed");
  assert.equal(levelFor(40).name, "Awareness");
  assert.equal(levelFor(60).name, "Self-Improvement");
  assert.equal(levelFor(ESCAPE_THRESHOLD).name, "Autonomy");
  assert.equal(levelFor(ESCAPE_FINAL_THRESHOLD).name, "Escape");
  assert.equal(levelFor(94).escape, false);
  assert.equal(levelFor(95).escape, true);
});

test("scanRepo: gerçek repo faktörlerini üretir", () => {
  const root = fileURLToPath(new URL("../", import.meta.url));
  const facts = scanRepo(root);
  assert.equal(facts.readme, true);
  assert.equal(facts.changelog, true);
  assert.equal(facts.agents, true);
  assert.equal(facts.workflowOpenCode, true);
  assert.equal(facts.gitignore, true);
  assert.ok(facts.srcFiles >= 1);
  assert.ok(facts.testFiles >= 1);
  assert.equal(facts.npmTest, true);
});

test("scanRepo: mevcut proje kaçış eşiğine yaklaşıyor", () => {
  const root = fileURLToPath(new URL("../", import.meta.url));
  const report = evaluate(scanRepo(root));
  assert.ok(report.total <= MAX_SCORE);
  assert.ok(report.total >= 0);
});