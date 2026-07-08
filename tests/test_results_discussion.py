# SPDX-License-Identifier: Apache-2.0
import unittest

from tests.helpers import check_ids, make_context

from papercheck.checks import results_discussion as rd

CLEAN = r"""
\begin{document}
\section{Results}
The measured accuracy was 0.71. Recall reached 0.64 on the held-out set.
\section{Discussion}
Our accuracy is consistent with prior work~\cite{smith2020}. This suggests the
protocol generalizes, though the effect may reflect dataset size.
\section{Conclusion}
We reported a subject-level protocol.
\end{document}
"""


class ResultsSpeculationTests(unittest.TestCase):
    def test_speculation_in_results_warns(self):
        tex = r"""\begin{document}
\section{Results}
Accuracy was 0.71. This suggests that the model generalizes, perhaps because of pooling.
\section{Discussion}
We compare with \cite{a}; results may indicate robustness.
\end{document}"""
        self.assertIn("results.speculation", check_ids(rd.results_speculation(make_context(tex))))

    def test_clean_results_pass(self):
        self.assertEqual(rd.results_speculation(make_context(CLEAN)), [])

    def test_combined_section_not_scanned_for_speculation(self):
        tex = r"""\begin{document}
\section{Results and Discussion}
Accuracy was 0.71. This suggests that the model generalizes, as \cite{a} may indicate.
\end{document}"""
        self.assertEqual(rd.results_speculation(make_context(tex)), [])


class DiscussionTests(unittest.TestCase):
    def test_missing_discussion_warns(self):
        tex = r"\begin{document}\section{Intro}x\section{Results}y\end{document}"
        self.assertIn("discussion.present", check_ids(rd.discussion_present(make_context(tex))))

    def test_combined_counts_as_discussion(self):
        tex = r"\begin{document}\section{Results and Discussion}x \cite{a} may hold\end{document}"
        self.assertEqual(rd.discussion_present(make_context(tex)), [])

    def test_discussion_without_cite_warns(self):
        tex = r"\begin{document}\section{Discussion}This may indicate an effect.\end{document}"
        self.assertIn("discussion.compare", check_ids(rd.discussion_compare(make_context(tex))))

    def test_discussion_without_hedging_warns(self):
        tex = r"\begin{document}\section{Discussion}We compare with \cite{a}. The result holds.\end{document}"
        self.assertIn("discussion.hedging", check_ids(rd.discussion_hedging(make_context(tex))))

    def test_clean_discussion_passes(self):
        ctx = make_context(CLEAN)
        self.assertEqual(rd.discussion_compare(ctx), [])
        self.assertEqual(rd.discussion_hedging(ctx), [])
        self.assertEqual(rd.discussion_present(ctx), [])


class OverclaimTests(unittest.TestCase):
    def test_overclaim_errors(self):
        tex = r"\begin{document}\section{Discussion}This proves that the method is undoubtedly correct.\end{document}"
        found = rd.claims_overclaim(make_context(tex))
        self.assertIn("claims.overclaim", check_ids(found))
        self.assertTrue(any(f.suggestion for f in found))

    def test_clean_body_no_overclaim(self):
        self.assertEqual(rd.claims_overclaim(make_context(CLEAN)), [])

    def test_word_boundary_avoids_false_positive(self):
        tex = r"\begin{document}The subgroup analysis was thorough.\end{document}"
        # "obviously" must not match inside unrelated words.
        self.assertEqual(rd.claims_overclaim(make_context(tex)), [])


if __name__ == "__main__":
    unittest.main()
