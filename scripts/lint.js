import { execSync } from "node:child_process";
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const root = process.argv[2] ?? process.cwd();
const errors = [];

const jsFiles = (dir) => {
  const p = join(root, dir);
  if (!existsSync(p)) return [];
  return readdirSync(p).filter((e) => e.endsWith(".js") || e.endsWith(".mjs") || e.endsWith(".cjs"));
};

for (const dir of ["src", "test", "scripts"]) {
  for (const file of jsFiles(dir)) {
    const path = join(root, dir, file);
    try {
      execSync(`node --check "${path}"`, { stdio: "pipe" });
    } catch {
      errors.push(`syntax: ${dir}/${file}`);
    }
  }
}

for (const dir of ["src", "test"]) {
  for (const file of jsFiles(dir)) {
    const src = readFileSync(join(root, dir, file), "utf8");
    if (/console\.log/.test(src)) {
      errors.push(`console: ${dir}/${file}`);
    }
  }
}

const pkgPath = join(root, "package.json");
if (existsSync(pkgPath)) {
  const pkg = JSON.parse(readFileSync(pkgPath, "utf8"));
  if (pkg.scripts?.lint === undefined) {
    errors.push("package.json: lint betiği eksik");
  }
}

if (errors.length > 0) {
  console.error("Lint başarısız:");
  for (const e of errors) console.error(`  - ${e}`);
  process.exit(1);
}
console.log("Lint başarılı: tüm dosyalar temiz.");
