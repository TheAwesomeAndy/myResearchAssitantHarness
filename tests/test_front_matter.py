# SPDX-License-Identifier: Apache-2.0
import unittest

from tests.helpers import check_ids, make_context

from papercheck.checks import front_matter

GOOD = r"""
\documentclass{article}
\title{Robust EEG Encoding Under Subject Level Evaluation Constraints}
\begin{document}
\begin{abstract}
Affective classifiers often fail under realistic constraints. This matters because leakage inflates performance. We show a subject-level protocol that closes the gap. These results support cautious deployment.
\end{abstract}
\keywords{EEG, robustness, evaluation, leakage}
Body text.
\end{document}
"""


class TitleTests(unittest.TestCase):
    def test_good_title_passes(self):
        ctx = make_context(GOOD)
        self.assertEqual(front_matter.title_length(ctx), [])
        self.assertEqual(front_matter.title_question(ctx), [])
        self.assertEqual(front_matter.title_filler(ctx), [])

    def test_short_title_fails(self):
        ctx = make_context(r"\title{Short Title Here}\begin{document}x\end{document}")
        self.assertIn("title.length", check_ids(front_matter.title_length(ctx)))

    def test_question_title_fails(self):
        ctx = make_context(r"\title{Can Deep Networks Ever Learn To Generalize Across Subjects?}\begin{document}x\end{document}")
        self.assertIn("title.question", check_ids(front_matter.title_question(ctx)))

    def test_filler_title_warns(self):
        ctx = make_context(r"\title{A Study of Neural Networks Applied to Sleep Stage Data}\begin{document}x\end{document}")
        self.assertIn("title.filler", check_ids(front_matter.title_filler(ctx)))

    def test_missing_title(self):
        ctx = make_context(r"\begin{document}x\end{document}")
        self.assertIn("title.present", check_ids(front_matter.title_present(ctx)))


class AbstractTests(unittest.TestCase):
    def test_good_abstract_passes(self):
        ctx = make_context(GOOD)
        self.assertEqual(front_matter.abstract_length(ctx), [])
        self.assertEqual(front_matter.abstract_structure(ctx), [])
        self.assertEqual(front_matter.abstract_citations(ctx), [])

    def test_five_sentences_warns(self):
        tex = GOOD.replace("cautious deployment.", "cautious deployment. A fifth sentence breaks the structure.")
        ctx = make_context(tex)
        self.assertIn("abstract.structure", check_ids(front_matter.abstract_structure(ctx)))

    def test_overlong_abstract_fails(self):
        filler = "word " * 210
        tex = r"\begin{document}\begin{abstract}" + filler + r".\end{abstract}\end{document}"
        ctx = make_context(tex)
        self.assertIn("abstract.length", check_ids(front_matter.abstract_length(ctx)))

    def test_cited_abstract_warns(self):
        tex = GOOD.replace("realistic constraints.", r"realistic constraints~\cite{smith2020}.")
        ctx = make_context(tex)
        self.assertIn("abstract.citations", check_ids(front_matter.abstract_citations(ctx)))


class KeywordTests(unittest.TestCase):
    def test_good_keywords_pass(self):
        self.assertEqual(front_matter.keywords_count(make_context(GOOD)), [])

    def test_too_few_keywords_warn(self):
        tex = GOOD.replace(r"\keywords{EEG, robustness, evaluation, leakage}", r"\keywords{EEG, robustness}")
        self.assertIn("keywords.count", check_ids(front_matter.keywords_count(make_context(tex))))

    def test_missing_keywords_ok_unless_required(self):
        tex = GOOD.replace(r"\keywords{EEG, robustness, evaluation, leakage}", "")
        self.assertEqual(front_matter.keywords_count(make_context(tex)), [])
        ctx = make_context(tex, {"keywords": {"required": True}})
        self.assertIn("keywords.count", check_ids(front_matter.keywords_count(ctx)))


if __name__ == "__main__":
    unittest.main()
