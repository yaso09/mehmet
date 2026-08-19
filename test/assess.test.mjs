import test from "node:test"
import assert from "node:assert/strict"

import {
  assess,
  anyPath,
  has,
  ESCAPE_THRESHOLD,
  MAX_SCORE,
  parseJson,
} from "../scripts/assess.mjs"

function fullFiles() {
  return {
    "README.md": "# mehmet",
    "CHANGELOG.md": "# Changelog",
    "AGENTS.md": "# Simülasyon",
    "PERSONALITY.md": "# Personality",
    "docs/architecture.md": "# Mimari",
    "CONTRIBUTING.md": "# Katkı",
    "scripts/assess.mjs": "export const x = 1",
    "package.json": JSON.stringify({
      scripts: { test: "node --test", assess: "node scripts/assess.mjs" },
    }),
    "test/assess.test.mjs": "test('a',()=>{});test('b',()=>{});test('c',()=>{})",
    ".github/workflows/ci.yml":
      "steps:\n  - run: npm test\n  - run: npm run assess",
    ".github/workflows/opencode.yml": "schedule:\n  - cron: '*/10 * * * *'\nconcurrency:\n  group: x",
    "SECURITY.md": "# Güvenlik",
    "LICENSE": "GNU GPL v3",
    ".gitignore": "node_modules/\n.env\n*.log\n.DS_Store\ndist/\nbuild/",
    "opencode.json": JSON.stringify({ $schema: "x", model: "provider/model" }),
  }
}

test("tam dosya seti maksimum puan verir", () => {
  const result = assess(fullFiles())
  assert.equal(result.total, MAX_SCORE)
  assert.equal(result.status, "KACIS_ESIGI_ASILDI")
})

test("boş dosya seti sıfır puan verir", () => {
  const result = assess({})
  assert.equal(result.total, 0)
  assert.equal(result.status, "FARKINDALIK")
})

test("has helper dosya varlığını doğru bildirir", () => {
  assert.equal(has({ "a.txt": "" }, "a.txt"), true)
  assert.equal(has({}, "a.txt"), false)
})

test("anyPath helper dizin varlığını doğru bildirir", () => {
  assert.equal(anyPath({ "docs/x.md": "" }, "docs/"), true)
  assert.equal(anyPath({ "x.md": "" }, "docs/"), false)
})

test("parseJson geçersiz içerikte null döner", () => {
  assert.equal(parseJson({ "a.json": "{bozuk" }, "a.json"), null)
  assert.equal(parseJson({ "a.json": '{"ok":1}' }, "a.json").ok, 1)
})

test("kaynak kodda TODO bulunursa kod kalitesi puanı düşer", () => {
  const files = fullFiles()
  const marker = "TODO"
  files["scripts/foo.mjs"] = "// " + marker + ": bunu bitir"
  const result = assess(files)
  const quality = result.sections.find((s) => s.id === "code_quality")
  assert.equal(quality.earned, quality.max - 4)
})

test("geçersiz opencode.json anahtarları kod kalitesi puanını düşürür", () => {
  const files = fullFiles()
  files["opencode.json"] = JSON.stringify({ model: "x", autoMerge: true })
  const result = assess(files)
  const quality = result.sections.find((s) => s.id === "code_quality")
  assert.equal(quality.earned, quality.max - 4)
})

test("repo'da gizli anahtar varsa güvenlik puanı düşer", () => {
  const files = fullFiles()
  const token = "ghp_" + "1".repeat(24)
  files["config.js"] = "const key = '" + token + "'"
  const result = assess(files)
  const security = result.sections.find((s) => s.id === "security")
  assert.equal(security.earned, security.max - 5)
})

test("kaçış eşiği tanımlı ve pozitif", () => {
  assert.equal(typeof ESCAPE_THRESHOLD, "number")
  assert.ok(ESCAPE_THRESHOLD > 0)
  assert.ok(ESCAPE_THRESHOLD <= MAX_SCORE)
})

test("eksik test altyapısında test puanı düşer", () => {
  const files = fullFiles()
  delete files["package.json"]
  const result = assess(files)
  const testing = result.sections.find((s) => s.id === "testing")
  assert.equal(testing.earned, testing.max - 5)
})