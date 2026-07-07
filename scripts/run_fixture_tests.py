#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Run synthetic fixture tests for the research AI harness."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FixtureCase:
    name: str
    command: list[str]
    expect_success: bool


def run_case(case: FixtureCase) -> dict[str, object]:
    proc = subprocess.run(case.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    success = proc.returncode == 0
    passed = success == case.expect_success
    print(f"[{'PASS' if passed else 'FAIL'}] {case.name}")
    if not passed:
        print(proc.stdout)
    return {
        "name": case.name,
        "expected_success": case.expect_success,
        "actual_success": success,
        "passed": passed,
        "returncode": proc.returncode,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", default="harness/reports/fixture_report.json")
    args = parser.parse_args()
    python = sys.executable
    has_latex = shutil.which("latexmk") or shutil.which("pdflatex")

    cases = [
        FixtureCase("good_manifest", [python, "scripts/check_table_manifest.py", "fixtures/good_manuscript/harness/table_manifest.yaml"], True),
        FixtureCase("bad_table_value", [python, "scripts/check_table_manifest.py", "fixtures/bad_table_value/harness/table_manifest.yaml"], False),
        FixtureCase("bad_citation_log", [python, "scripts/check_citations.py", "fixtures/bad_citation/manuscript/main.log"], False),
        FixtureCase("forbidden_phrase", [python, "scripts/check_forbidden_phrases.py", "fixtures/forbidden_phrase", "--phrase-file", "harness/forbidden_phrases.txt"], False),
        FixtureCase("path_marker", [python, "tools/check_path_markers.py", "fixtures/path_marker"], False),
    ]

    if has_latex:
        cases.append(FixtureCase("good_latex_build", [python, "scripts/verify_latex.py", "fixtures/good_manuscript/manuscript/main.tex"], True))
        cases.append(FixtureCase("bad_latex_build", [python, "scripts/verify_latex.py", "fixtures/bad_latex/manuscript/main.tex"], False))
    else:
        print("[SKIP] LaTeX build fixtures require latexmk or pdflatex")

    results = [run_case(case) for case in cases]
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps({"results": results}, indent=2), encoding="utf-8")

    if any(not item["passed"] for item in results):
        print("fixture suite failed")
        return 1
    print("fixture suite passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
