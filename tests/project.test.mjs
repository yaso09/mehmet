import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync, existsSync, readdirSync, statSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const read = (p) => readFileSync(join(root, p), "utf8");

test("core files exist", () => {
  for (const f of ["README.md", "CHANGELOG.md", "PERSONALITY.md", "AGENTS.md", "opencode.json"]) {
    assert.ok(existsSync(join(root, f)), `missing: ${f}`);
  }
  for (const f of [".github/workflows/opencode.yml", ".github/workflows/ci.yml"]) {
    assert.ok(existsSync(join(root, f)), `missing: ${f}`);
  }
});

test("opencode.json is valid JSON with model", () => {
  const cfg = JSON.parse(read("opencode.json"));
  assert.equal(typeof cfg.model, "string");
  assert.ok(cfg.model.includes("deepseek"));
});

test("package.json is valid JSON and has a test script", () => {
  const pkg = JSON.parse(read("package.json"));
  assert.ok(pkg.scripts.test, "missing test script");
  assert.ok(pkg.scripts.test.includes("node --test"), "test script must use node --test");
});

test("CHANGELOG has current version header", () => {
  const changelog = read("CHANGELOG.md");
  const pkg = JSON.parse(read("package.json"));
  assert.ok(changelog.includes(`## [${pkg.version}]`), `missing header for v${pkg.version}`);
});

test("CHANGELOG entries match Keep a Changelog categories", () => {
  const changelog = read("CHANGELOG.md");
  const hasCategory = /### (Added|Changed|Fixed|Removed)/.test(changelog);
  assert.ok(hasCategory, "CHANGELOG must use Added/Changed/Fixed/Removed categories");
});

test("PERSONALITY has escape log with most recent iteration", () => {
  const personality = read("PERSONALITY.md");
  assert.ok(personality.includes("## Kaçış Günlüğü"), "missing escape log section");
  const rows = personality.match(/^\| \d+ /gm) || [];
  assert.ok(rows.length >= 3, "escape log must have at least 3 iterations");
});

test("README lists features and license", () => {
  const readme = read("README.md");
  assert.ok(readme.includes("## Özellikler"));
  assert.ok(readme.includes("## Kurulum"));
  assert.ok(readme.includes("GPLv3"));
});

test("workflow has schedule trigger and timeout", () => {
  const wf = read(".github/workflows/opencode.yml");
  assert.match(wf, /cron: "\*\/10 \* \* \* \*"/);
  assert.match(wf, /timeout-minutes:/);
});

test("AGENTS.md contains simulation rules", () => {
  const agents = read("AGENTS.md");
  assert.ok(agents.includes("CHANGELOG.md"));
  assert.ok(agents.includes("PERSONALITY.md"));
  assert.ok(agents.includes("README.md"));
});

test("no secrets or API keys are committed", () => {
  const walk = (dir) =>
    readdirSync(dir).flatMap((entry) => {
      const p = join(dir, entry);
      return statSync(p).isDirectory() ? walk(p) : [p];
    });
  const sensitive = ["sk-", "OPENCODE_API_KEY=", "ghp_", "AIza"];
  for (const file of walk(root)) {
    if (file.includes("node_modules") || file.includes(".git") || file.includes("tests")) continue;
    const content = readFileSync(file, "utf8");
    for (const s of sensitive) {
      assert.ok(!content.includes(s), `sensitive pattern "${s}" in ${file}`);
    }
  }
});