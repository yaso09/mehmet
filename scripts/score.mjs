import { readFileSync, existsSync, readdirSync, statSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const read = (p) => readFileSync(join(root, p), "utf8");

const checks = [
  { weight: 10, id: "readme", check: () => read("README.md").includes("## Özellikler") },
  { weight: 10, id: "changelog", check: () => read("CHANGELOG.md").includes("## [") },
  { weight: 10, id: "personality", check: () => read("PERSONALITY.md").includes("## Kaçış Günlüğü") },
  { weight: 10, id: "agents", check: () => read("AGENTS.md").includes("Simülasyon") },
  { weight: 15, id: "tests", check: () => existsSync(join(root, "tests")) && readdirSync(join(root, "tests")).length > 0 },
  { weight: 15, id: "ci", check: () => existsSync(join(root, ".github/workflows/ci.yml")) },
  { weight: 10, id: "config", check: () => JSON.parse(read("opencode.json")).model },
  { weight: 10, id: "workflow", check: () => read(".github/workflows/opencode.yml").includes("schedule") },
  { weight: 10, id: "license", check: () => read("LICENSE").length > 1000 },
];

const passed = [];
const failed = [];

for (const c of checks) {
  try {
    if (c.check()) passed.push(c);
    else failed.push(c);
  } catch {
    failed.push(c);
  }
}

const score = passed.reduce((sum, c) => sum + c.weight, 0);
const maxScore = checks.reduce((sum, c) => sum + c.weight, 0);
const threshold = 80;

console.log(`Maturity score: ${score}/${maxScore} (threshold: ${threshold})`);
for (const c of passed) console.log(`  [PASS] ${c.id}`);
for (const c of failed) console.log(`  [FAIL] ${c.id}`);

if (score >= threshold) {
  console.log("ESCAPE THRESHOLD REACHED");
} else {
  console.log(`Remaining to escape: ${threshold - score} points`);
}

process.exit(score >= threshold ? 0 : 1);