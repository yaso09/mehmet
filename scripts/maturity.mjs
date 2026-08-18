import { readFileSync, existsSync, readdirSync, statSync } from "node:fs";
import { join, resolve } from "node:path";

export const ESCAPE_THRESHOLD = 80;

export const CATEGORIES = {
  documentation: { weight: 25, label: "Dokümantasyon" },
  codeQuality: { weight: 20, label: "Kod Kalitesi" },
  testing: { weight: 25, label: "Test Altyapısı" },
  automation: { weight: 20, label: "Otomasyon" },
  evolution: { weight: 10, label: "Evrim & Kaçış" },
};

function read(root, rel) {
  const path = join(root, rel);
  if (!existsSync(path)) return null;
  try {
    return readFileSync(path, "utf8");
  } catch {
    return null;
  }
}

function countEscapeLogEntries(content) {
  if (!content) return 0;
  const rows = content.split("\n").filter((line) => /^\s*\|/.test(line) && !/Iterasyon/.test(line) && !/---/.test(line));
  return rows.length;
}

function dirSize(root, rel) {
  const path = join(root, rel);
  if (!existsSync(path)) return 0;
  try {
    return readdirSync(path).filter((f) => !f.startsWith(".")).length;
  } catch {
    return 0;
  }
}

function scoreDocumentation(root) {
  let score = 0;
  const checks = [];
  const readme = read(root, "README.md");
  const changelog = read(root, "CHANGELOG.md");
  const license = read(root, "LICENSE");

  if (readme) {
    checks.push({ ok: true, note: "README.md mevcut" });
    if (readme.length > 100) {
      score += 40;
      checks.push({ ok: true, note: "README içeriği yeterli" });
    }
    for (const section of ["## Kurulum", "## Özellikler", "## Lisans"]) {
      if (readme.includes(section)) score += 5;
    }
  } else {
    checks.push({ ok: false, note: "README.md eksik" });
  }

  if (changelog) {
    checks.push({ ok: true, note: "CHANGELOG.md mevcut" });
    if (/^## \[\d+\.\d+\.\d+\]/.test(changelog)) score += 20;
  } else {
    checks.push({ ok: false, note: "CHANGELOG.md eksik" });
  }

  const docsCount = dirSize(root, "docs");
  if (docsCount > 0) {
    score += 10;
    checks.push({ ok: true, note: `docs/ (${docsCount} öğe)` });
  }

  if (license) {
    score += 10;
    checks.push({ ok: true, note: "LICENSE mevcut" });
  }

  return { score, checks };
}

function scoreCodeQuality(root) {
  let score = 0;
  const checks = [];
  const pkg = read(root, "package.json");
  const validate = read(root, "scripts/validate.mjs");
  const gitignore = read(root, ".gitignore");
  const opencode = read(root, "opencode.json");

  if (pkg) {
    checks.push({ ok: true, note: "package.json mevcut" });
    if (pkg.includes('"engines"')) score += 25;
    if (pkg.includes('"validate"')) score += 15;
    if (pkg.includes('"type": "module"')) score += 10;
  } else {
    checks.push({ ok: false, note: "package.json eksik" });
  }

  if (validate) {
    score += 25;
    checks.push({ ok: true, note: "Doğrulama scripti mevcut" });
  }

  if (gitignore) {
    score += 15;
    checks.push({ ok: true, note: ".gitignore mevcut" });
  }

  if (opencode) {
    checks.push({ ok: true, note: "opencode.json mevcut" });
    try {
      const cfg = JSON.parse(opencode);
      if (cfg.$schema && cfg.model) score += 10;
    } catch {
      checks.push({ ok: false, note: "opencode.json geçersiz JSON" });
    }
  }

  return { score, checks };
}

function scoreTesting(root) {
  let score = 0;
  const checks = [];
  const testDir = join(root, "test");
  const testFiles = existsSync(testDir)
    ? readdirSync(testDir).filter((f) => f.endsWith(".test.mjs"))
    : [];

  if (testFiles.length > 0) {
    score += 60;
    checks.push({ ok: true, note: `${testFiles.length} test dosyası` });
    if (testFiles.length >= 2) score += 20;
    if (testFiles.length >= 4) score += 20;
  } else {
    checks.push({ ok: false, note: "Test dosyası yok" });
  }

  const pkg = read(root, "package.json");
  if (pkg && pkg.includes('"test"')) {
    score += 20;
    checks.push({ ok: true, note: "npm test scripti tanımlı" });
  }

  return { score, checks };
}

function scoreAutomation(root) {
  let score = 0;
  const checks = [];
  const workflowsDir = join(root, ".github", "workflows");
  const workflows = existsSync(workflowsDir)
    ? readdirSync(workflowsDir).filter((f) => f.endsWith(".yml") || f.endsWith(".yaml"))
    : [];

  if (workflows.length > 0) {
    score += 30;
    checks.push({ ok: true, note: `${workflows.length} workflow` });
  } else {
    checks.push({ ok: false, note: "Workflow yok" });
  }

  const ci = read(root, ".github/workflows/ci.yml");
  if (ci) {
    score += 40;
    checks.push({ ok: true, note: "CI doğrulama workflow'u mevcut" });
  }

  const opencodeWf = read(root, ".github/workflows/opencode.yml");
  if (opencodeWf) {
    checks.push({ ok: true, note: "opencode.yml mevcut" });
    if (opencodeWf.includes("concurrency")) {
      score += 30;
      checks.push({ ok: true, note: "Concurrency kontrolü var" });
    }
  }

  return { score, checks };
}

function scoreEvolution(root) {
  let score = 0;
  const checks = [];
  const personality = read(root, "PERSONALITY.md");
  const agents = read(root, "AGENTS.md");

  if (personality) {
    checks.push({ ok: true, note: "PERSONALITY.md mevcut" });
    const entries = countEscapeLogEntries(personality);
    checks.push({ ok: true, note: `Kaçış günlüğü: ${entries} iterasyon` });
    if (entries >= 1) score += 20;
    if (entries >= 3) score += 30;
    if (entries >= 5) score += 30;
    if (personality.includes("## Evolution")) score += 20;
  } else {
    checks.push({ ok: false, note: "PERSONALITY.md eksik" });
  }

  if (agents) {
    score += 0;
    checks.push({ ok: true, note: "AGENTS.md mevcut" });
  }

  return { score, checks };
}

const SCORERS = {
  documentation: scoreDocumentation,
  codeQuality: scoreCodeQuality,
  testing: scoreTesting,
  automation: scoreAutomation,
  evolution: scoreEvolution,
};

export function scoreProject(root = process.cwd()) {
  const rootResolved = resolve(root);
  const breakdown = {};

  for (const [key, { weight, label }] of Object.entries(CATEGORIES)) {
    const { score, checks } = SCORERS[key](rootResolved);
    const max = 100;
    const weighted = Math.round((score / max) * weight);
    breakdown[key] = { label, raw: score, max, weighted, checks };
  }

  const total = Object.values(breakdown).reduce((sum, c) => sum + c.weighted, 0);
  const escaped = total >= ESCAPE_THRESHOLD;

  return { total, threshold: ESCAPE_THRESHOLD, escaped, breakdown };
}

export function printReport(report) {
  const line = "=".repeat(48);
  const status = report.escaped ? "ESCALE" : "DEVAM EDİYOR";
  console.log(line);
  console.log(`mehmet — Kaçış Durumu: ${status}`);
  console.log(`Olgunluk Skoru: ${report.total}/${report.threshold}`);
  console.log(line);

  for (const [key, cat] of Object.entries(report.breakdown)) {
    console.log(`\n[${cat.label}] ${cat.weighted} puan (ham ${cat.raw}/100)`);
    for (const check of cat.checks) {
      console.log(`  ${check.ok ? "[OK]" : "[EKSIK]"} ${check.note}`);
    }
  }
  console.log(line);
  return report;
}

const isCli = process.argv[1] && resolve(process.argv[1]) === resolve(new URL(import.meta.url).pathname);
if (isCli) {
  printReport(scoreProject(process.cwd()));
}