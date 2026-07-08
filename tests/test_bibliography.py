# SPDX-License-Identifier: Apache-2.0
import tempfile
import unittest
from pathlib import Path

from papercheck.checks import bibliography as bib
from papercheck.config import Config
from papercheck.latex import load_document
from papercheck.model import CheckContext


def make_ctx_with_bib(tex: str, bib_text: str | None, config: dict | None = None) -> CheckContext:
    tmp = Path(tempfile.mkdtemp(prefix="papercheck-bib-"))
    (tmp / "main.tex").write_text(tex, encoding="utf-8")
    if bib_text is not None:
        (tmp / "refs.bib").write_text(bib_text, encoding="utf-8")
    doc = load_document(tmp / "main.tex")
    return CheckContext(doc=doc, config=Config(config or {}, profile="draft"), root=tmp)


GOOD_BIB = """
@article{smith2023, author={Smith, A}, title={A}, year={2023}, journal={J}}
@article{jones2022, author={Jones, B}, title={B}, year={2022}, journal={J}}
@inproceedings{lee2024, author={Lee, C}, title={C}, year={2024}, booktitle={P}}
"""

GOOD_TEX = r"""\begin{document}
We build on \cite{smith2023}, \cite{jones2022}, and \cite{lee2024}.
\bibliography{refs}
\end{document}"""


class BibTests(unittest.TestCase):
    def test_clean_bib_passes(self):
        ctx = make_ctx_with_bib(GOOD_TEX, GOOD_BIB)
        for fn in (bib.bib_files, bib.bib_missing_entries, bib.bib_duplicate_keys,
                   bib.bib_missing_fields, bib.bib_uncited, bib.bib_staleness):
            self.assertEqual(fn(ctx), [], fn.__name__)

    def test_no_bib_file_info(self):
        ctx = make_ctx_with_bib(r"\begin{document}\cite{x} \bibliography{refs}\end{document}", None)
        ids = {f.check_id for f in bib.bib_files(ctx)}
        self.assertIn("bib.files", ids)
        # other checks stay silent without a bib file
        self.assertEqual(bib.bib_missing_entries(ctx), [])

    def test_missing_entry_error(self):
        ctx = make_ctx_with_bib(r"\begin{document}\cite{ghost}\bibliography{refs}\end{document}", GOOD_BIB)
        self.assertIn("bib.missing-entries", {f.check_id for f in bib.bib_missing_entries(ctx)})

    def test_duplicate_key_error(self):
        dup = GOOD_BIB + "\n@article{smith2023, author={X}, title={T}, year={2023}}"
        ctx = make_ctx_with_bib(GOOD_TEX, dup)
        self.assertIn("bib.duplicate-keys", {f.check_id for f in bib.bib_duplicate_keys(ctx)})

    def test_missing_fields_warn(self):
        thin = "@article{a2023, year={2023}}"
        ctx = make_ctx_with_bib(r"\begin{document}\cite{a2023}\bibliography{refs}\end{document}", thin)
        self.assertIn("bib.missing-fields", {f.check_id for f in bib.bib_missing_fields(ctx)})

    def test_uncited_info(self):
        ctx = make_ctx_with_bib(r"\begin{document}\cite{smith2023}\bibliography{refs}\end{document}", GOOD_BIB)
        self.assertIn("bib.uncited", {f.check_id for f in bib.bib_uncited(ctx)})

    def test_staleness_warn(self):
        old = """
@article{a1990, author={A}, title={A}, year={1990}}
@article{b1991, author={B}, title={B}, year={1991}}
@article{c2024, author={C}, title={C}, year={2024}}
"""
        tex = r"\begin{document}\cite{a1990}\cite{b1991}\cite{c2024}\bibliography{refs}\end{document}"
        ctx = make_ctx_with_bib(tex, old)
        self.assertIn("bib.staleness", {f.check_id for f in bib.bib_staleness(ctx)})


if __name__ == "__main__":
    unittest.main()
