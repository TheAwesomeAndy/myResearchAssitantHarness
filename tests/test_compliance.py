# SPDX-License-Identifier: Apache-2.0
import unittest

from tests.helpers import check_ids, make_context

from papercheck.checks import compliance

DOUBLE = {"venue": {"blinding": "double", "human_subjects": True}}

CLEAN_DOUBLE = r"""
\documentclass{article}
\author{Anonymous Authors}
\begin{document}
We evaluated on human participants under IRB approval with informed consent.
The data are available at \url{https://anonymous.4open.science/r/demo}.
Prior work informs this study.
\end{document}
"""


class BlindingModeTests(unittest.TestCase):
    def test_unset_info(self):
        ctx = make_context(r"\begin{document}x\end{document}")
        self.assertIn("blind.unset", check_ids(compliance.blind_unset(ctx)))

    def test_unset_silent_when_set(self):
        ctx = make_context(r"\begin{document}x\end{document}", DOUBLE)
        self.assertEqual(compliance.blind_unset(ctx), [])


class DoubleBlindTests(unittest.TestCase):
    def test_clean_double_passes(self):
        ctx = make_context(CLEAN_DOUBLE, DOUBLE)
        for fn in (compliance.blind_author_block, compliance.blind_acknowledgments,
                   compliance.blind_self_reveal, compliance.blind_links,
                   compliance.blind_metadata, compliance.ethics_statement,
                   compliance.data_availability):
            self.assertEqual(fn(ctx), [], fn.__name__)

    def test_real_author_errors(self):
        tex = r"\author{Jane Researcher}\begin{document}x\end{document}"
        self.assertIn("blind.author-block", check_ids(compliance.blind_author_block(make_context(tex, DOUBLE))))

    def test_acknowledgments_error(self):
        tex = r"\begin{document}\section{Acknowledgments}Thanks to NSF.\end{document}"
        self.assertIn("blind.acknowledgments", check_ids(compliance.blind_acknowledgments(make_context(tex, DOUBLE))))

    def test_self_reveal_warn(self):
        tex = r"\begin{document}In our previous work we showed this.\end{document}"
        self.assertIn("blind.self-reveal", check_ids(compliance.blind_self_reveal(make_context(tex, DOUBLE))))

    def test_identifiable_link_error(self):
        tex = r"\begin{document}Code at \url{https://github.com/jane/repo}.\end{document}"
        self.assertIn("blind.links", check_ids(compliance.blind_links(make_context(tex, DOUBLE))))

    def test_email_metadata_warn(self):
        tex = r"\begin{document}Contact jane@uni.edu for details.\end{document}"
        self.assertIn("blind.metadata", check_ids(compliance.blind_metadata(make_context(tex, DOUBLE))))


class AuthorsRequiredTests(unittest.TestCase):
    def test_single_requires_author(self):
        ctx = make_context(r"\begin{document}x\end{document}", {"venue": {"blinding": "single"}})
        self.assertIn("single.authors-required", check_ids(compliance.single_authors_required(ctx)))

    def test_double_does_not_require_author(self):
        ctx = make_context(r"\begin{document}x\end{document}", DOUBLE)
        self.assertEqual(compliance.single_authors_required(ctx), [])


class StatementTests(unittest.TestCase):
    def test_ethics_error_for_human_subjects(self):
        ctx = make_context(r"\begin{document}Data available at repo.\end{document}", DOUBLE)
        self.assertIn("ethics.statement", check_ids(compliance.ethics_statement(ctx)))

    def test_ethics_warn_autodetect(self):
        tex = r"\begin{document}We recruited 40 participants for the task.\end{document}"
        found = compliance.ethics_statement(make_context(tex))
        self.assertIn("ethics.statement", check_ids(found))

    def test_data_availability_error(self):
        tex = r"\begin{document}We ran experiments.\end{document}"
        self.assertIn("data.availability", check_ids(compliance.data_availability(make_context(tex))))


if __name__ == "__main__":
    unittest.main()
