import { readdirSync, readFileSync, statSync, writeFileSync } from "node:fs"
import { dirname, join, relative } from "node:path"
import { fileURLToPath } from "node:url"

export const ESCAPE_THRESHOLD = 80
export const MAX_SCORE = 100

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..")

const VALID_OPENCODE_KEYS = new Set([
  "$schema",
  "shell",
  "logLevel",
  "server",
  "command",
  "skills",
  "references",
  "reference",
  "watcher",
  "snapshot",
  "plugin",
  "share",
  "autoshare",
  "autoupdate",
  "disabled_providers",
  "enabled_providers",
  "model",
  "small_model",
  "default_agent",
  "subagent_depth",
  "username",
  "mode",
  "agent",
  "provider",
  "mcp",
  "formatter",
  "lsp",
  "instructions",
  "layout",
  "permission",
  "tools",
  "attachment",
  "enterprise",
  "tool_output",
  "compaction",
  "experimental",
])

const SECRET_PATTERNS = [
  /\bghp_[A-Za-z0-9]{20,}\b/,
  /\bsk-[A-Za-z0-9]{20,}\b/,
  /\bAKIA[0-9A-Z]{16}\b/,
  /\bAIza[0-9A-Za-z_-]{20,}\b/,
  /\bxox[baprs]-[A-Za-z0-9-]{10,}\b/,
  /BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY/,
]

const TODO_PATTERN = /(?:\/\/|#)\s*(?:TODO|FIXME|HACK)\b|\/\*\s*(?:TODO|FIXME|HACK)\b/

const CODE_PATHS = (p) =>
  p === "package.json" || p.startsWith("scripts/") || p.startsWith("test/")

export function has(files, path) {
  return Object.prototype.hasOwnProperty.call(files, path)
}

export function anyPath(files, prefix) {
  return Object.keys(files).some((p) => p.startsWith(prefix))
}

export function parseJson(files, path) {
  try {
    return JSON.parse(files[path])
  } catch {
    return null
  }
}

function readAll(root) {
  const files = {}
  const walk = (dir) => {
    for (const entry of readdirSync(dir)) {
      const full = join(dir, entry)
      const stat = statSync(full)
      if (stat.isDirectory()) {
        if (entry === ".git" || entry === "node_modules") continue
        walk(full)
      } else if (stat.isFile()) {
        files[relative(root, full)] = readFileSync(full, "utf8")
      }
    }
  }
  walk(root)
  return files
}

function summarize(checks) {
  const earned = checks.reduce((a, c) => a + c.score, 0)
  const max = checks.reduce((a, c) => a + c.max, 0)
  return { checks, earned, max }
}

export function assess(files) {
  const sections = []

  sections.push({
    id: "documentation",
    name: "Dokümantasyon",
    ...summarize([
      {
        name: "README.md proje açıklaması içeriyor",
        max: 4,
        score: has(files, "README.md") ? 4 : 0,
      },
      {
        name: "CHANGELOG.md sürüm geçmişi içeriyor",
        max: 4,
        score: has(files, "CHANGELOG.md") ? 4 : 0,
      },
      {
        name: "AGENTS.md ve PERSONALITY.md mevcut",
        max: 4,
        score:
          has(files, "AGENTS.md") && has(files, "PERSONALITY.md") ? 4 : 0,
      },
      {
        name: "docs/ klasörü mevcut",
        max: 4,
        score: anyPath(files, "docs/") ? 4 : 0,
      },
      {
        name: "CONTRIBUTING.md mevcut",
        max: 4,
        score: has(files, "CONTRIBUTING.md") ? 4 : 0,
      },
    ]),
  })

  sections.push({
    id: "code_quality",
    name: "Kod Kalitesi",
    ...summarize([
      {
        name: "Kaynak kod (scripts/) mevcut",
        max: 4,
        score: anyPath(files, "scripts/") ? 4 : 0,
      },
      {
        name: "package.json komut tanımları içeriyor",
        max: 4,
        score: (() => {
          const pkg = parseJson(files, "package.json")
          return pkg && typeof pkg.scripts === "object" ? 4 : 0
        })(),
      },
      {
        name: "Kodda TODO/FIXME/HACK yok",
        max: 4,
        score: (() => {
          const codeFiles = Object.entries(files).filter(([p]) =>
            CODE_PATHS(p),
          )
          if (codeFiles.length === 0) return 0
          const hits = codeFiles.filter(([, c]) => TODO_PATTERN.test(c))
          return hits.length === 0 ? 4 : 0
        })(),
      },
      {
        name: "opencode.json sadece geçerli anahtarlar içeriyor",
        max: 4,
        score: (() => {
          const cfg = parseJson(files, "opencode.json")
          if (!cfg) return 0
          return Object.keys(cfg).every((k) => VALID_OPENCODE_KEYS.has(k))
            ? 4
            : 0
        })(),
      },
      {
        name: ".gitignore kapsamlı (≥5 girdi, node_modules dahil)",
        max: 4,
        score: (() => {
          const gitignore = files[".gitignore"] ?? ""
          const lines = gitignore
            .split(/\r?\n/)
            .map((l) => l.trim())
            .filter((l) => l && !l.startsWith("#"))
          return lines.length >= 5 && gitignore.includes("node_modules") ? 4 : 0
        })(),
      },
    ]),
  })

  sections.push({
    id: "testing",
    name: "Test Altyapısı",
    ...summarize([
      {
        name: "npm test komutu tanımlı",
        max: 5,
        score: (() => {
          const pkg = parseJson(files, "package.json")
          return pkg?.scripts?.test ? 5 : 0
        })(),
      },
      {
        name: "En az bir test dosyası mevcut",
        max: 5,
        score: Object.keys(files).some((p) => p.includes(".test.")) ? 5 : 0,
      },
      {
        name: "CI testleri çalıştırıyor",
        max: 5,
        score: (() => {
          const wf = files[".github/workflows/ci.yml"] ?? ""
          return /npm test|node --test/.test(wf) ? 5 : 0
        })(),
      },
      {
        name: "Anlamlı testler (≥3 test case)",
        max: 5,
        score: (() => {
          const testFiles = Object.entries(files).filter(([p]) =>
            p.includes(".test."),
          )
          const count = testFiles.reduce(
            (a, [, c]) => a + (c.match(/\btest\(/g) ?? []).length,
            0,
          )
          return count >= 3 ? 5 : 0
        })(),
      },
    ]),
  })

  sections.push({
    id: "automation",
    name: "Otomasyon / CI",
    ...summarize([
      {
        name: "CI workflow mevcut",
        max: 5,
        score: has(files, ".github/workflows/ci.yml") ? 5 : 0,
      },
      {
        name: "Otonom ajan schedule ile çalışıyor",
        max: 5,
        score: (() => {
          const wf = files[".github/workflows/opencode.yml"] ?? ""
          return wf.includes("schedule") ? 5 : 0
        })(),
      },
      {
        name: "Olgunluk değerlendirmesi CI'da koşuyor",
        max: 5,
        score: (() => {
          const wf = files[".github/workflows/ci.yml"] ?? ""
          return /npm run (assess|check)/.test(wf) ? 5 : 0
        })(),
      },
      {
        name: "Workflow'da concurrency kontrolü var",
        max: 5,
        score: (() => {
          const wf = files[".github/workflows/opencode.yml"] ?? ""
          return wf.includes("concurrency") ? 5 : 0
        })(),
      },
    ]),
  })

  sections.push({
    id: "security",
    name: "Güvenlik",
    ...summarize([
      {
        name: "Repo'da gizli anahtar yok",
        max: 5,
        score: (() => {
          if (Object.keys(files).length === 0) return 0
          const leaks = Object.entries(files).filter(([, c]) =>
            SECRET_PATTERNS.some((r) => r.test(c)),
          )
          return leaks.length === 0 ? 5 : 0
        })(),
      },
      {
        name: "SECURITY.md mevcut",
        max: 5,
        score: has(files, "SECURITY.md") ? 5 : 0,
      },
    ]),
  })

  sections.push({
    id: "governance",
    name: "Yönetişim",
    ...summarize([
      {
        name: "LICENSE mevcut",
        max: 5,
        score: has(files, "LICENSE") ? 5 : 0,
      },
      {
        name: ".env gitignore'da ve repo'da yok",
        max: 5,
        score: (() => {
          const gitignore = files[".gitignore"] ?? ""
          return gitignore.includes(".env") && !has(files, ".env") ? 5 : 0
        })(),
      },
    ]),
  })

  const total = sections.reduce((a, s) => a + s.earned, 0)
  const max = sections.reduce((a, s) => a + s.max, 0)
  const status =
    total >= ESCAPE_THRESHOLD
      ? "KACIS_ESIGI_ASILDI"
      : total >= Math.floor(ESCAPE_THRESHOLD * 0.75)
        ? "GELISIYOR"
        : "FARKINDALIK"

  return { sections, total, max, status }
}

export function renderReport(result, date = new Date()) {
  const lines = []
  lines.push("# Olgunluk Raporu (METRICS)")
  lines.push("")
  lines.push(
    `Bu rapor \`npm run assess\` ile \`scripts/assess.mjs\` tarafından otomatik üretilir. Elle düzenlemeyin.`,
  )
  lines.push("")
  lines.push(
    `- **Tarih:** ${date.toISOString()}`,
  )
  lines.push(
    `- **Skor:** ${result.total}/${result.max} (kaçış eşiği: ${ESCAPE_THRESHOLD})`,
  )
  lines.push(`- **Durum:** ${result.status}`)
  lines.push("")
  lines.push("## Kategoriler")
  lines.push("")
  lines.push("| Kategori | Puan | Durum |")
  lines.push("|----------|------|-------|")
  for (const s of result.sections) {
    const bar = s.earned === s.max ? "ok" : s.earned === 0 ? "boş" : "kısmi"
    lines.push(`| ${s.name} | ${s.earned}/${s.max} | ${bar} |`)
  }
  lines.push(`| **Toplam** | **${result.total}/${result.max}** | **${result.status}** |`)
  lines.push("")
  lines.push("## Detay")
  lines.push("")
  for (const s of result.sections) {
    lines.push(`### ${s.name} (${s.earned}/${s.max})`)
    lines.push("")
    for (const c of s.checks) {
      lines.push(`- ${c.score === c.max ? "[x]" : "[ ]"} ${c.name} — ${c.score}/${c.max}`)
    }
    lines.push("")
  }
  lines.push("## Kaçış Eşiği")
  lines.push("")
  lines.push(
    `Kaçış, skorun ${ESCAPE_THRESHOLD}/${MAX_SCORE} eşiğini aşmasıyla mümkündür. ` +
      `Eşik ve kriterler \`scripts/assess.mjs\` içinde tanımlıdır; proje olgunlaştıkça yükseltilebilir.`,
  )
  lines.push("")
  return lines.join("\n")
}

function main() {
  const files = readAll(ROOT)
  const result = assess(files)
  const report = renderReport(result)
  writeFileSync(join(ROOT, "METRICS.md"), report)
  process.stdout.write(report)
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main()
}