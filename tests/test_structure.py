# SPDX-License-Identifier: Apache-2.0
import unittest

from tests.helpers import check_ids, make_context

from papercheck.checks import structure

CLEAN = r"""
\begin{document}
\begin{abstract}
We present a subject-level protocol that closes an evaluation gap. It matters
for deployment. Our method holds under stress. The work supports cautious use.
\end{abstract}
\section{Introduction}
Intro.
\section{Methods}
We used a leave-one-subject-out protocol.
\section{Results}
Accuracy was 0.71.
\section{Discussion}
The finding is consistent with \cite{a} and may generalize.
\section{Conclusion}
A limitation is the small sample; future work will scale the study to more sites.
\section{Related Work}
Several efforts inform this study. Building on that line, our protocol differs by design.
\end{document}
"""


class StructureTests(unittest.TestCase):
    def test_clean_passes(self):
        ctx = make_context(CLEAN)
        self.assertEqual(structure.structure_sections(ctx), [])
        self.assertEqual(structure.limits_present(ctx), [])
        self.assertEqual(structure.limits_pivot(ctx), [])
        self.assertEqual(structure.conclusion_abstract_copy(ctx), [])
        self.assertEqual(structure.related_position(ctx, ) if False else structure.related_position(ctx), [])
        self.assertEqual(structure.related_hostile(ctx), [])
        self.assertEqual(structure.related_laundry_list(ctx), [])

    def test_missing_sections_warn(self):
        tex = r"\begin{document}\section{Intro}a\section{Methods}b\end{document}"
        found = structure.structure_sections(make_context(tex))
        self.assertIn("structure.sections", check_ids(found))

    def test_no_limitations_errors(self):
        tex = r"\begin{document}\section{Results}Accuracy was high.\end{document}"
        self.assertIn("limits.present", check_ids(structure.limits_present(make_context(tex))))

    def test_limitation_without_pivot_warns(self):
        tex = r"\begin{document}A key limitation is the sample size and nothing else is said here.\end{document}"
        self.assertIn("limits.pivot", check_ids(structure.limits_pivot(make_context(tex))))

    def test_abstract_copy_errors(self):
        tex = r"""\begin{document}
\begin{abstract}
We prove a bound. The bound is tight. It matters a lot for practice today.
\end{abstract}
\section{Conclusion}
We prove a bound. The bound is tight.
\end{document}"""
        # add a limitation so only the copy check is exercised in isolation
        self.assertIn("conclusion.abstract-copy", check_ids(structure.conclusion_abstract_copy(make_context(tex))))

    def test_related_before_methods_warns(self):
        tex = r"\begin{document}\section{Related Work}Prior art.\section{Methods}Our method.\end{document}"
        self.assertIn("related.position", check_ids(structure.related_position(make_context(tex))))

    def test_hostile_related_warns(self):
        tex = r"\begin{document}\section{Related Work}Their naive approach fails to scale.\end{document}"
        self.assertIn("related.hostile", check_ids(structure.related_hostile(make_context(tex))))

    def test_laundry_list_warns(self):
        tex = (r"\begin{document}\section{Related Work}"
               r"\cite{a} did X. \cite{b} did Y. \cite{c} did Z. \cite{d} did W."
               r"\end{document}")
        self.assertIn("related.laundry-list", check_ids(structure.related_laundry_list(make_context(tex))))


if __name__ == "__main__":
    unittest.main()
