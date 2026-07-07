#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Scan text files for configured phrases."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

EXTENSIONS = {".tex", ".md", ".txt", ".rst"}
EXCLUDES = {".git", ".venv", "venv", "__pycache__", "node_modules"}


def load_phrases(path: Path) -> list[str]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]


def iter_files(root: Path):
    skip_fixture_examples = root == Path('.')
    for path in root.rglob("*"):
        if skip_fixture_examples and path.parts and path.parts[0] == "fixtures":
            continue
        if path.is_file() and path.suffix.lower() in EXTENSIONS and not any(part in EXCLUDES for part in path.parts):
            yield path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--phrase-file", default="harness/forbidden_phrases.txt")
    parser.add_argument("--allow-em-dash", action="store_true")
    args = parser.parse_args()

    root = Path(args.root)
    phrases = load_phrases(Path(args.phrase_file))
    findings = []
    files = [root] if root.is_file() else list(iter_files(root))

    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        lowered = text.lower()
        for phrase in phrases:
            if phrase.lower() in lowered:
                findings.append(f"{path}: phrase: {phrase}")
        if not args.allow_em_dash and "—" in text:
            findings.append(f"{path}: em dash")

    if findings:
        print("Phrase check failed:")
        print("\n".join(f"- {item}" for item in findings))
        return 1

    print("Phrase check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
