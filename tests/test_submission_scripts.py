# SPDX-License-Identifier: Apache-2.0
"""Subprocess tests for the standalone submission gates."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(script: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), *args],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd=str(ROOT),
    )


def write(text: str, suffix: str = ".md") -> str:
    tmp = Path(tempfile.mkdtemp(prefix="papercheck-sub-")) / f"f{suffix}"
    tmp.write_text(text, encoding="utf-8")
    return str(tmp)


class CoverLetterTests(unittest.TestCase):
    def test_good_letter_passes(self):
        proc = run("check_cover_letter.py", "fixtures/submission/cover_letter_good.md",
                   "--journal", "Journal of Robust Machine Intelligence")
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_bad_letter_fails(self):
        proc = run("check_cover_letter.py", "fixtures/submission/cover_letter_bad.md")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("hype", proc.stdout)

    def test_journal_absence_fails(self):
        path = write("Para one has plenty of words to be a substantive paragraph about the work here.\n\n"
                     "Para two also has more than fifteen words describing why this matters for the field.\n\n"
                     "Para three explains the fit with more than fifteen words for the venue conversation here.")
        proc = run("check_cover_letter.py", path, "--journal", "Nature")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("Nature", proc.stdout)

    def test_paragraph_count_enforced(self):
        path = write("Only one substantive paragraph here with clearly more than fifteen words in the body.")
        proc = run("check_cover_letter.py", path)
        self.assertEqual(proc.returncode, 1)


class RebuttalTests(unittest.TestCase):
    def test_good_rebuttal_passes(self):
        proc = run("check_rebuttal.py", "fixtures/submission/rebuttal_good.md")
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_bad_rebuttal_fails(self):
        proc = run("check_rebuttal.py", "fixtures/submission/rebuttal_bad.md")
        self.assertEqual(proc.returncode, 1)

    def test_missing_response_fails(self):
        path = write("Reviewer 1, Comment 1: Weak baseline.\n\nReviewer 1, Comment 2: Unclear.\nResponse: Fixed on page 3 line 4.")
        proc = run("check_rebuttal.py", path)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("no response", proc.stdout)

    def test_no_markers_fails(self):
        path = write("We thank the reviewer and changed page 3 line 5 accordingly.")
        proc = run("check_rebuttal.py", path)
        self.assertEqual(proc.returncode, 1)

    def test_strict_flags_missing_locator(self):
        path = write("We thank the reviewers.\n\nReviewer 1, Comment 1: Weak baseline.\nResponse: We added a Transformer baseline.")
        normal = run("check_rebuttal.py", path)
        strict = run("check_rebuttal.py", path, "--strict")
        self.assertEqual(normal.returncode, 0, normal.stdout)
        self.assertEqual(strict.returncode, 1)


class WallTests(unittest.TestCase):
    def test_wall_good_passes(self):
        proc = run("phase_gate.py", "fixtures/wall/good/manuscript/main.tex")
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_wall_violation_fails(self):
        proc = run("phase_gate.py", "fixtures/wall/violation/manuscript/main.tex")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("drafted before", proc.stdout)

    def test_declared_phase_violation(self):
        status = write('[wall]\ndeclared_phase = "conclusion"\n', suffix=".toml")
        proc = run("phase_gate.py", "fixtures/wall/good/manuscript/main.tex", "--status", status)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("declared phase", proc.stdout)


if __name__ == "__main__":
    unittest.main()
