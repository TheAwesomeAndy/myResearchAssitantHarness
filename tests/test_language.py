# SPDX-License-Identifier: Apache-2.0
import unittest

from tests.helpers import check_ids, make_context

from papercheck.checks import language

CLEAN = r"""
\begin{document}
We report a subject-level protocol. Accuracy reached 0.71 on the held-out set.
The result is consistent with prior work and may generalize to related tasks.
\end{document}
"""


class LanguageTests(unittest.TestCase):
    def test_clean_passes(self):
        ctx = make_context(CLEAN)
        for fn in (language.lang_hype, language.lang_hype_claims, language.lang_cautious,
                   language.lang_ai_tells, language.lang_em_dash, language.lang_contractions,
                   language.lang_weasel, language.lang_significant):
            self.assertEqual(fn(ctx), [], fn.__name__)

    def test_hype_errors(self):
        tex = r"\begin{document}This is a groundbreaking, revolutionary result.\end{document}"
        self.assertIn("lang.hype", check_ids(language.lang_hype(make_context(tex))))

    def test_hype_claims_warn(self):
        tex = r"\begin{document}Our cutting-edge method shows unprecedented gains.\end{document}"
        self.assertIn("lang.hype-claims", check_ids(language.lang_hype_claims(make_context(tex))))

    def test_cautious_replacement_carries_suggestion(self):
        tex = r"\begin{document}This proves the approach works.\end{document}"
        found = language.lang_cautious(make_context(tex))
        self.assertIn("lang.cautious", check_ids(found))
        self.assertTrue(all(f.suggestion for f in found))

    def test_ai_tells_warn(self):
        tex = r"\begin{document}We delve into the rich tapestry of the problem.\end{document}"
        self.assertIn("lang.ai-tells", check_ids(language.lang_ai_tells(make_context(tex))))

    def test_em_dash_warn_and_optout(self):
        tex = "\\begin{document}The method—ours—is simple.\\end{document}"
        self.assertIn("lang.em-dash", check_ids(language.lang_em_dash(make_context(tex))))
        ctx = make_context(tex, {"language": {"allow_em_dash": True}})
        self.assertEqual(language.lang_em_dash(ctx), [])

    def test_contractions_warn_but_not_its(self):
        tex = r"\begin{document}It's clear that its design is sound.\end{document}"
        found = language.lang_contractions(make_context(tex))
        self.assertEqual(len(found), 1)

    def test_weasel_info(self):
        tex = r"\begin{document}This is a very large improvement.\end{document}"
        self.assertIn("lang.weasel", check_ids(language.lang_weasel(make_context(tex))))

    def test_significant_without_test_warns(self):
        tex = r"\begin{document}We observed a significant improvement in accuracy.\end{document}"
        self.assertIn("lang.significant", check_ids(language.lang_significant(make_context(tex))))

    def test_significant_with_test_passes(self):
        tex = r"\begin{document}The improvement was significant (p < 0.01).\end{document}"
        self.assertEqual(language.lang_significant(make_context(tex)), [])


if __name__ == "__main__":
    unittest.main()
