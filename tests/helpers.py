# SPDX-License-Identifier: Apache-2.0
"""Shared helpers for check unit tests."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from papercheck.config import Config  # noqa: E402
from papercheck.latex import load_document  # noqa: E402
from papercheck.model import CheckContext  # noqa: E402


def make_context(tex: str, config: dict | None = None, profile: str = "draft") -> CheckContext:
    """Build a CheckContext from an inline LaTeX string."""
    tmp = Path(tempfile.mkdtemp(prefix="papercheck-test-"))
    main = tmp / "main.tex"
    main.write_text(tex, encoding="utf-8")
    doc = load_document(main)
    return CheckContext(doc=doc, config=Config(config or {}, profile=profile), root=tmp)


def check_ids(findings) -> set[str]:
    return {finding.check_id for finding in findings}
