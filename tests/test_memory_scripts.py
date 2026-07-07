# SPDX-License-Identifier: Apache-2.0
"""Subprocess tests for the Module 7 memory tooling."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(script: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), *args],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=str(ROOT),
    )


class MemoryJournalTests(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp(prefix="papercheck-mem-"))
        self.file = str(self.dir / "memory.jsonl")

    def test_add_list_search_resolve_digest(self):
        add = run("memory.py", "add", "decision", "Target venue is JRMI", "--tags", "venue", "--file", self.file)
        self.assertEqual(add.returncode, 0, add.stderr)
        self.assertEqual(add.stdout.strip(), "1")

        run("memory.py", "add", "lesson", "LOSO avoids leakage", "--tags", "methods", "--file", self.file)

        listed = run("memory.py", "list", "--kind", "lesson", "--file", self.file)
        self.assertIn("LOSO", listed.stdout)
        self.assertNotIn("JRMI", listed.stdout)

        found = run("memory.py", "search", "venue", "--file", self.file)
        self.assertIn("JRMI", found.stdout)

        resolved = run("memory.py", "resolve", "2", "Adopted in Section 3", "--file", self.file)
        self.assertEqual(resolved.returncode, 0)
        entries = [json.loads(line) for line in Path(self.file).read_text().splitlines()]
        self.assertEqual(entries[1]["status"], "resolved")

        digest = run("memory.py", "digest", "--file", self.file)
        self.assertIn("project memory digest", digest.stdout)

    def test_resolve_unknown_id_fails(self):
        run("memory.py", "add", "decision", "x", "--file", self.file)
        proc = run("memory.py", "resolve", "99", "nope", "--file", self.file)
        self.assertEqual(proc.returncode, 1)

    def test_bad_kind_rejected(self):
        proc = run("memory.py", "add", "nonsense", "text", "--file", self.file)
        self.assertNotEqual(proc.returncode, 0)

    def test_malformed_line_skipped(self):
        Path(self.file).write_text('{"id": 1, "kind": "decision", "text": "ok", "status": "open"}\nNOT JSON\n')
        proc = run("memory.py", "digest", "--file", self.file)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("malformed", proc.stderr)


class SelfImproveTests(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp(prefix="papercheck-imp-"))
        self.history = self.dir / "history.jsonl"
        self.memory = self.dir / "memory.jsonl"
        self.report = self.dir / "report.md"

    def _write_regressing_history(self):
        rows = []
        # older half low, newer half high -> regressing; lang.hype recurs
        for warnings in (1, 1, 1, 5, 6, 7):
            rows.append(json.dumps({
                "timestamp": f"2026-06-0{len(rows)+1}T09:00:00+0000",
                "summary": {"errors": 1, "warnings": warnings, "infos": 0},
                "check_ids": ["lang.hype", "methods.baseline"],
            }))
        self.history.write_text("\n".join(rows) + "\n")

    def test_empty_state_message(self):
        proc = run("self_improve.py", "--history", str(self.history), "--memory", str(self.memory))
        self.assertEqual(proc.returncode, 0)
        self.assertIn("no history or memory yet", proc.stdout)

    def test_recurring_trend_and_suggestions(self):
        self._write_regressing_history()
        proc = run("self_improve.py", "--history", str(self.history), "--memory", str(self.memory),
                   "--report", str(self.report))
        self.assertEqual(proc.returncode, 0)
        self.assertIn("lang.hype", proc.stdout)
        self.assertIn("regressing", proc.stdout)
        self.assertIn("forbidden_phrases", proc.stdout)
        self.assertTrue(self.report.exists())

    def test_strict_fails_on_regression(self):
        self._write_regressing_history()
        proc = run("self_improve.py", "--history", str(self.history), "--memory", str(self.memory),
                   "--report", str(self.report), "--strict")
        self.assertEqual(proc.returncode, 1)


if __name__ == "__main__":
    unittest.main()
