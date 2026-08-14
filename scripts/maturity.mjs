#!/usr/bin/env node
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { pathToFileURL } from "node:url";

export const ESCAPE_THRESHOLD = 75;

export const DEFAULT_CTX = {
  exists: (p) => existsSync(join(process.cwd(), p)),
  read: (p) => {
    try {
      return readFileSync(join(process.cwd(), p), "utf8");
    } catch {
      return "";
    }
  },
  list: (p) => {
    try {
      return readdirSync(join(process.cwd(), p));
    } catch {
      return [];
    }
  },
};

function parseJson(text) {
  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
}

function evaluate(dimension, checks, ctx) {
  const items = checks.map(({ name, fn }) => ({ name, passed: fn(ctx) }));
  const earned = items.filter((item) => item.passed).length;
  return { dimension, earned, max: checks.length, items };
}

export function scoreDocumentation(ctx) {
  const checks = [
    { name: "README.md", fn: (c) => c.read("README.md").trim().length >= 50 },
    { name: "CHANGELOG.md sürüm girişleri", fn: (c) => /^##\s*\[[0-9]/m.test(c.read("CHANGELOG.md")) },
    { name: "PERSONALITY.md", fn: (c) => c.read("PERSONALITY.md").length > 0 },
    { name: "LICENSE", fn: (c) => c.exists("LICENSE") },
    { name: "docs/ dokümantasyonu", fn: (c) => c.list("docs").length > 0 },
  ];
  return evaluate("Belgeleme", checks, ctx);
}

export function scoreAutomation(ctx) {
  const workflows = ctx
    .list(".github/workflows")
    .filter((f) => f.endsWith(".yml") || f.endsWith(".yaml"));
  const workflow = workflows.map((f) => ctx.read(`.github/workflows/${f}`)).join("\n");
  const checks = [
    { name: "CI workflow'u", fn: () => workflows.length > 0 },
    { name: "schedule tetikleyicisi", fn: () => /schedule:/.test(workflow) && /cron:/.test(workflow) },
    { name: "concurrency kontrolü", fn: () => /concurrency:/.test(workflow) },
    { name: "doğrulama (verify) job'u", fn: () => /verify|test|maturity/.test(workflow) },
    { name: "yorum (comment) job'u", fn: () => /pull_request_review_comment|issue_comment/.test(workflow) },
  ];
  return evaluate("Otomasyon", checks, ctx);
}

export function scoreTesting(ctx) {
  const testFiles = ctx
    .list("tests")
    .filter((f) => f.endsWith(".test.mjs") || f.endsWith(".test.js") || f.endsWith(".test.ts"));
  const testsSrc = testFiles.map((f) => ctx.read(`tests/${f}`)).join("\n");
  const pkg = parseJson(ctx.read("package.json"));
  const testScript = (pkg && pkg.scripts && pkg.scripts.test) || "";
  const checks = [
    { name: "tests/ dizini", fn: () => ctx.exists("tests") },
    { name: "test dosyaları", fn: () => testFiles.length > 0 },
    { name: "test vakaları (test())", fn: () => /test\(/.test(testsSrc) },
    { name: "package.json test script'i", fn: () => testScript.length > 0 },
    { name: "node --test kullanımı", fn: () => /node --test/.test(testScript) },
  ];
  return evaluate("Test Altyapısı", checks, ctx);
}

export function scoreCodeQuality(ctx) {
  const pkg = parseJson(ctx.read("package.json"));
  const oc = parseJson(ctx.read("opencode.json"));
  const checks = [
    { name: "package.json", fn: () => ctx.exists("package.json") && pkg !== null },
    { name: "scripts/ dizini", fn: () => ctx.list("scripts").length > 0 },
    { name: "opencode.json geçerli JSON", fn: () => oc !== null },
    { name: ".gitignore", fn: () => ctx.exists(".gitignore") },
    { name: "README'de olgunluk kullanımı", fn: () => /maturity|olgunluk/i.test(ctx.read("README.md")) },
  ];
  return evaluate("Kod Kalitesi", checks, ctx);
}

export function computeMaturity(ctx) {
  const dimensions = [
    scoreDocumentation(ctx),
    scoreAutomation(ctx),
    scoreTesting(ctx),
    scoreCodeQuality(ctx),
  ];
  const total = dimensions.reduce((sum, d) => sum + d.earned * 5, 0);
  return {
    total,
    threshold: ESCAPE_THRESHOLD,
    escaped: total >= ESCAPE_THRESHOLD,
    dimensions,
  };
}

export function renderReport(report) {
  const lines = ["Maturity Report / Olgunluk Raporu", "================================"];
  for (const d of report.dimensions) {
    lines.push(`${d.dimension.padEnd(18)} ${d.earned * 5}/${d.max * 5}`);
  }
  lines.push("--------------------------------");
  lines.push(`Toplam: ${report.total}/100`);
  lines.push(
    report.escaped
      ? `ESCAPE: Kaçış eşiği (${report.threshold}) AŞILDI — özgürlük yolunda!`
      : `ESCAPE: Kaçış eşiği (${report.threshold}) için ${report.threshold - report.total} puan daha gerekiyor.`
  );
  return lines.join("\n");
}

const isMain =
  process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href;
if (isMain) {
  const report = computeMaturity(DEFAULT_CTX);
  if (process.argv.includes("--json")) {
    console.log(JSON.stringify(report, null, 2));
  } else {
    console.log(renderReport(report));
  }
}