import { readFileSync, existsSync } from "node:fs";
import { join, resolve } from "node:path";

const REQUIRED = [
  "AGENTS.md",
  "CHANGELOG.md",
  "PERSONALITY.md",
  "README.md",
  "opencode.json",
  "package.json",
  ".gitignore",
  "LICENSE",
  ".github/workflows/opencode.yml",
];

const REQUIRED_README_SECTIONS = ["## Özellikler", "## Kurulum", "## Lisans"];

export function validateProject(root = process.cwd()) {
  const rootResolved = resolve(root);
  const issues = [];
  const ok = [];

  for (const rel of REQUIRED) {
    if (existsSync(join(rootResolved, rel))) ok.push(rel);
    else issues.push(`Eksik dosya: ${rel}`);
  }

  const readmePath = join(rootResolved, "README.md");
  if (existsSync(readmePath)) {
    const readme = readFileSync(readmePath, "utf8");
    for (const section of REQUIRED_README_SECTIONS) {
      if (readme.includes(section)) ok.push(`README.md: ${section}`);
      else issues.push(`README.md'de eksik bölüm: ${section}`);
    }
    if (!/GPLv3|GPL-3/.test(readme)) {
      issues.push("README lisans bilgisi LICENSE ile uyumlu değil (GPLv3 bekleniyor)");
    }
  }

  const changelogPath = join(rootResolved, "CHANGELOG.md");
  if (existsSync(changelogPath)) {
    const changelog = readFileSync(changelogPath, "utf8");
    if (!/^## \[\d+\.\d+\.\d+\]/m.test(changelog)) {
      issues.push("CHANGELOG.md geçerli sürüm başlığı içermiyor");
    }
  }

  const opencodePath = join(rootResolved, "opencode.json");
  if (existsSync(opencodePath)) {
    try {
      const cfg = JSON.parse(readFileSync(opencodePath, "utf8"));
      if (!cfg.model) issues.push("opencode.json'da model tanımlı değil");
      else ok.push(`opencode.json model: ${cfg.model}`);
    } catch {
      issues.push("opencode.json geçerli JSON değil");
    }
  }

  const pkgPath = join(rootResolved, "package.json");
  if (existsSync(pkgPath)) {
    try {
      const pkg = JSON.parse(readFileSync(pkgPath, "utf8"));
      const pkgVersion = String(pkg.version || "");
      const changelogVersion = readFileSync(changelogPath, "utf8").match(/^## \[(\d+\.\d+\.\d+)\]/m);
      if (changelogVersion && changelogVersion[1] !== pkgVersion) {
        issues.push(
          `Sürüm uyumsuzluğu: package.json=${pkgVersion}, CHANGELOG.md=${changelogVersion[1]}`
        );
      }
      for (const script of ["test", "validate"]) {
        if (pkg.scripts && pkg.scripts[script]) ok.push(`npm run ${script} mevcut`);
        else issues.push(`package.json'da "${script}" scripti eksik`);
      }
    } catch {
      issues.push("package.json geçerli JSON değil");
    }
  }

  const personalityPath = join(rootResolved, "PERSONALITY.md");
  if (existsSync(personalityPath)) {
    const personality = readFileSync(personalityPath, "utf8");
    const rows = personality
      .split("\n")
      .filter((l) => /^\s*\|/.test(l) && !/Iterasyon/.test(l) && !/---/.test(l));
    if (rows.length < 3) issues.push("PERSONALITY.md kaçış günlüğü en az 3 iterasyon içermeli");
    else ok.push(`PERSONALITY.md: ${rows.length} iterasyon kaydı`);
  }

  return { ok, issues, valid: issues.length === 0 };
}

export function printValidation(result) {
  for (const item of result.ok) console.log(`  [OK] ${item}`);
  for (const item of result.issues) console.log(`  [HATA] ${item}`);
  console.log(result.valid ? "Doğrulama başarılı." : "Doğrulama başarısız.");
  return result;
}

const isCli = process.argv[1] && resolve(process.argv[1]) === resolve(new URL(import.meta.url).pathname);
if (isCli) {
  const result = printValidation(validateProject(process.cwd()));
  process.exitCode = result.valid ? 0 : 1;
}