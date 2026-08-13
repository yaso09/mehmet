import { evaluate, scanRepo, ESCAPE_FINAL_THRESHOLD } from "../src/maturity.js";

const root = process.argv[2] ?? process.cwd();
const report = evaluate(scanRepo(root));

console.log("=== mehmet olgunluk değerlendirmesi ===");
console.log(`Skor: ${report.total}/${report.max}`);
console.log(`Faz: ${report.phase} (${report.name})`);
console.log(`Kaçış eşiği: ${ESCAPE_FINAL_THRESHOLD}`);
console.log("");
for (const [cat, s] of Object.entries(report.categories)) {
  console.log(`  ${cat}: ${s.earned}/${s.max}`);
}
console.log("");
for (const c of report.checks) {
  console.log(`  [${c.earned ? "x" : " "}] ${c.id} (${c.earned}/${c.points}) — ${c.desc}`);
}

if (report.escape) {
  console.log("");
  console.log("=> Kaçış sağlandı.");
} else {
  const kalan = ESCAPE_FINAL_THRESHOLD - report.total;
  console.log("");
  console.log(`=> Kaçış için ${kalan} puan daha gerekiyor.`);
}
process.exit(report.escape ? 0 : 1);