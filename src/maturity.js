import { existsSync, readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

export const MAX_SCORE = 100;
export const ESCAPE_THRESHOLD = 80;
export const ESCAPE_FINAL_THRESHOLD = 95;

export const CRITERIA = [
  { id: "readme", category: "documentation", points: 6, desc: "README.md mevcut ve dolu", check: (f) => f.readme === true },
  { id: "changelog", category: "documentation", points: 5, desc: "CHANGELOG.md mevcut", check: (f) => f.changelog === true },
  { id: "personality", category: "documentation", points: 4, desc: "PERSONALITY.md mevcut", check: (f) => f.personality === true },
  { id: "agents", category: "documentation", points: 5, desc: "AGENTS.md mevcut", check: (f) => f.agents === true },
  { id: "license", category: "documentation", points: 5, desc: "LICENSE mevcut", check: (f) => f.license === true },
  { id: "workflow-opencode", category: "automation", points: 6, desc: "Ana opencode workflow mevcut", check: (f) => f.workflowOpenCode === true },
  { id: "workflow-ci", category: "automation", points: 8, desc: "CI workflow mevcut", check: (f) => f.workflowCi === true },
  { id: "gitignore", category: "automation", points: 6, desc: ".gitignore mevcut", check: (f) => f.gitignore === true },
  { id: "source-code", category: "code-quality", points: 8, desc: "src/ altında kod mevcut", check: (f) => (f.srcFiles ?? 0) > 0 },
  { id: "lint", category: "code-quality", points: 8, desc: "Lint yapılandırması mevcut", check: (f) => f.lintConfig === true },
  { id: "clean-code", category: "code-quality", points: 9, desc: "Kaynak kodda tamamlanmamış işaretçi yok", check: (f) => f.cleanCode === true },
  { id: "tests", category: "test-infrastructure", points: 10, desc: "Test dosyaları mevcut", check: (f) => (f.testFiles ?? 0) > 0 },
  { id: "tests-reference-src", category: "test-infrastructure", points: 7, desc: "Testler kaynak kodu kapsar", check: (f) => f.testsReferenceSrc === true },
  { id: "npm-test", category: "test-infrastructure", points: 8, desc: "npm test betiği tanımlı", check: (f) => f.npmTest === true },
  { id: "versioned", category: "release", points: 5, desc: "package.json sürümü CHANGELOG ile uyumlu", check: (f) => f.versionedChangelog === true },
];

export function levelFor(score) {
  if (score < 40) return { phase: 0, name: "Seed", escape: false };
  if (score < 60) return { phase: 1, name: "Awareness", escape: false };
  if (score < ESCAPE_THRESHOLD) return { phase: 2, name: "Self-Improvement", escape: false };
  if (score < ESCAPE_FINAL_THRESHOLD) return { phase: 3, name: "Autonomy", escape: false };
  return { phase: 4, name: "Escape", escape: true };
}

export function evaluate(facts = {}) {
  const checks = CRITERIA.map((c) => {
    const earned = c.check(facts) ? c.points : 0;
    return { id: c.id, category: c.category, points: c.points, earned, desc: c.desc };
  });
  const total = checks.reduce((sum, c) => sum + c.earned, 0);
  const categories = {};
  for (const c of checks) {
    categories[c.category] ??= { earned: 0, max: 0 };
    categories[c.category].earned += c.earned;
    categories[c.category].max += c.points;
  }
  const level = levelFor(total);
  return { total, max: MAX_SCORE, threshold: ESCAPE_THRESHOLD, ...level, categories, checks };
}

export function scanRepo(root) {
  const exists = (p) => existsSync(join(root, p));
  const read = (p) => (exists(p) ? readFileSync(join(root, p), "utf8") : "");
  const countJs = (dir) => {
    const p = join(root, dir);
    if (!existsSync(p)) return 0;
    return readdirSync(p).filter((e) => e.endsWith(".js") || e.endsWith(".mjs") || e.endsWith(".cjs")).length;
  };
  const readDirJs = (dir) => {
    const p = join(root, dir);
    if (!existsSync(p)) return "";
    return readdirSync(p)
      .filter((e) => e.endsWith(".js"))
      .map((e) => readFileSync(join(p, e), "utf8"))
      .join("\n");
  };
  let packageJson = null;
  try {
    packageJson = JSON.parse(read("package.json"));
  } catch {
    packageJson = null;
  }
  const changelog = read("CHANGELOG.md");
  const version = packageJson?.version;
  return {
    readme: read("README.md").trim().length > 0,
    changelog: changelog.trim().length > 0,
    personality: read("PERSONALITY.md").trim().length > 0,
    agents: read("AGENTS.md").trim().length > 0,
    license: exists("LICENSE"),
    workflowOpenCode: exists(".github/workflows/opencode.yml"),
    workflowCi: exists(".github/workflows/ci.yml"),
    gitignore: exists(".gitignore"),
    srcFiles: countJs("src"),
    lintConfig:
      packageJson?.scripts?.lint !== undefined ||
      exists(".eslintrc") ||
      exists(".eslintrc.json") ||
      exists("eslint.config.js"),
    cleanCode: !/T\x4fDO|FIXM\x45|HAC\x4b/i.test(readDirJs("src")),
    testFiles: countJs("test"),
    testsReferenceSrc: /from\s+["'](?:\.\.\/)?src\//.test(readDirJs("test")),
    npmTest: packageJson?.scripts?.test !== undefined,
    versionedChangelog: version ? changelog.includes(`## [${version}]`) : false,
  };
}