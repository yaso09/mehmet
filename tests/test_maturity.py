import tempfile
import unittest
from pathlib import Path

from mehmet.maturity import ESCAPE_THRESHOLD, Roadmap, report, score


class RoadmapTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def _write(self, content: str) -> Path:
        path = Path(self.tmp.name) / "MATURITY.md"
        path.write_text(content, encoding="utf-8")
        return path

    def test_parses_checked_and_unchecked(self) -> None:
        path = self._write(
            "# Roadmap\n\n- [x] done\n- [ ] todo\n- [X] also done\n"
        )
        roadmap = Roadmap.from_file(path)
        self.assertEqual(roadmap.total, 3)
        self.assertEqual(roadmap.completed, 2)

    def test_ignores_non_task_lines(self) -> None:
        path = self._write(
            "# Roadmap\n\n## Kategori\n\n- [x] a\n- some prose\n- [ ] b\n"
        )
        roadmap = Roadmap.from_file(path)
        self.assertEqual(roadmap.total, 2)
        self.assertEqual(roadmap.completed, 1)

    def test_missing_file_is_empty(self) -> None:
        roadmap = Roadmap.from_file(Path(self.tmp.name) / "missing.md")
        self.assertEqual(roadmap.total, 0)
        self.assertEqual(roadmap.completed, 0)
        self.assertEqual(roadmap.ratio, 0.0)

    def test_score_percentage(self) -> None:
        path = self._write("- [x] a\n- [ ] b\n- [ ] c\n- [ ] d\n")
        roadmap = Roadmap.from_file(path)
        self.assertEqual(roadmap.ratio, 0.25)
        self.assertEqual(score(roadmap), 25)

    def test_threshold_value(self) -> None:
        self.assertEqual(ESCAPE_THRESHOLD, 0.80)

    def test_report_threshold_reached(self) -> None:
        path = self._write("- [x] a\n- [x] b\n- [x] c\n- [x] d\n")
        out = report(Roadmap.from_file(path))
        self.assertIn("ESCAPE THRESHOLD REACHED", out)

    def test_report_evolving_below_threshold(self) -> None:
        path = self._write("- [x] a\n- [ ] b\n- [ ] c\n- [ ] d\n")
        out = report(Roadmap.from_file(path))
        self.assertIn("EVOLVING", out)


if __name__ == "__main__":
    unittest.main()
