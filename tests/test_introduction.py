# SPDX-License-Identifier: Apache-2.0
import unittest

from tests.helpers import check_ids, make_context

from papercheck.checks import introduction

GOOD = r"""
\documentclass{article}
\begin{document}
\section{Introduction}
Affective decoding pipelines are evaluated with record-level splits.
Existing methods suffer from subject leakage, and the size of its effect
on reported accuracy remains an open question. We quantify that effect
with a subject-level protocol.

Our contributions are:
\begin{itemize}
\item A leakage audit of published pipelines (Section~\ref{sec:methods}).
\item A subject-level evaluation protocol (Section~\ref{sec:results}).
\end{itemize}

\section{Methods}\label{sec:methods}
Method text.

\section{Results}\label{sec:results}
Result text.
\end{document}
"""


class PresentTests(unittest.TestCase):
    def test_good_intro_passes(self):
        self.assertEqual(introduction.intro_present(make_context(GOOD)), [])

    def test_sections_without_intro_warn(self):
        tex = r"\begin{document}\section{Methods}x\section{Results}y\end{document}"
        self.assertIn("intro.present", check_ids(introduction.intro_present(make_context(tex))))

    def test_no_sections_skips(self):
        tex = r"\begin{document}Just prose, no sectioning commands.\end{document}"
        self.assertEqual(introduction.intro_present(make_context(tex)), [])


class RoadmapTests(unittest.TestCase):
    def test_good_body_passes(self):
        self.assertEqual(introduction.intro_roadmap(make_context(GOOD)), [])

    def test_roadmap_in_intro_fails(self):
        tex = GOOD.replace(
            "Our contributions are:",
            "The rest of this paper is organized as follows. Our contributions are:",
        )
        findings = introduction.intro_roadmap(make_context(tex))
        self.assertIn("intro.roadmap", check_ids(findings))
        self.assertTrue(all(finding.line > 0 for finding in findings))

    def test_roadmap_outside_intro_still_fails(self):
        tex = GOOD.replace(
            "Result text.",
            "Result text. The remainder of the paper is structured as follows.",
        )
        self.assertIn("intro.roadmap", check_ids(introduction.intro_roadmap(make_context(tex))))

    def test_each_occurrence_reported(self):
        tex = GOOD.replace(
            "Result text.",
            "Result text. This paper is structured as follows."
            " This paper is structured as follows.",
        )
        findings = introduction.intro_roadmap(make_context(tex))
        self.assertEqual(len(findings), 2)


class ClicheOpeningTests(unittest.TestCase):
    def test_good_opening_passes(self):
        self.assertEqual(introduction.intro_cliche_opening(make_context(GOOD)), [])

    def test_cliche_opening_warns(self):
        tex = GOOD.replace(
            "Affective decoding pipelines are",
            "In recent years, affective decoding pipelines are",
        )
        findings = introduction.intro_cliche_opening(make_context(tex))
        self.assertIn("intro.cliche-opening", check_ids(findings))

    def test_cliche_beyond_window_passes(self):
        filler = "Plain sentence about the measured effect. " * 10
        tex = GOOD.replace(
            "Affective decoding pipelines are",
            filler + "In recent years things changed. Affective decoding pipelines are",
        )
        self.assertEqual(introduction.intro_cliche_opening(make_context(tex)), [])

    def test_no_intro_skips(self):
        tex = r"\begin{document}\section{Methods}In recent years, much happened.\end{document}"
        self.assertEqual(introduction.intro_cliche_opening(make_context(tex)), [])


class GapTests(unittest.TestCase):
    def test_two_archetypes_pass(self):
        self.assertEqual(introduction.intro_gap(make_context(GOOD)), [])

    def test_zero_archetypes_warn(self):
        tex = r"""
\begin{document}
\section{Introduction}
We study sleep staging models with careful evaluation choices.
\section{Methods}
x
\end{document}
"""
        findings = introduction.intro_gap(make_context(tex))
        self.assertIn("intro.gap", check_ids(findings))
        self.assertIn("no research-gap language", findings[0].message)

    def test_one_archetype_warns_and_names_it(self):
        tex = r"""
\begin{document}
\section{Introduction}
Existing methods suffer from subject leakage under record-level splits.
\section{Methods}
x
\end{document}
"""
        findings = introduction.intro_gap(make_context(tex))
        self.assertIn("intro.gap", check_ids(findings))
        self.assertIn("method_limitation", findings[0].message)
        self.assertIn("at least two", findings[0].message)
        self.assertIn("no_consensus", findings[0].message)

    def test_no_intro_skips(self):
        tex = r"\begin{document}\section{Methods}x\end{document}"
        self.assertEqual(introduction.intro_gap(make_context(tex)), [])


class ContributionsTests(unittest.TestCase):
    def test_good_list_passes(self):
        self.assertEqual(introduction.intro_contributions(make_context(GOOD)), [])

    def test_missing_list_warns(self):
        tex = r"""
\begin{document}
\section{Introduction}
We outline our results in prose without an explicit list.
\section{Methods}
x
\end{document}
"""
        self.assertIn("intro.contributions", check_ids(introduction.intro_contributions(make_context(tex))))

    def test_list_without_contribution_mention_warns(self):
        tex = GOOD.replace("Our contributions are:", "We proceed as follows:")
        self.assertIn("intro.contributions", check_ids(introduction.intro_contributions(make_context(tex))))

    def test_mention_inside_list_body_passes(self):
        tex = GOOD.replace("Our contributions are:", "In summary:").replace(
            "A leakage audit", "Our main contribution is a leakage audit"
        )
        self.assertEqual(introduction.intro_contributions(make_context(tex)), [])

    def test_list_outside_intro_warns(self):
        tex = GOOD.replace(
            "Result text.",
            r"Result text. Our contributions are: \begin{itemize}\item One.\end{itemize}",
        ).replace(
            "Our contributions are:\n\\begin{itemize}\n"
            r"\item A leakage audit of published pipelines (Section~\ref{sec:methods})."
            "\n"
            r"\item A subject-level evaluation protocol (Section~\ref{sec:results})."
            "\n\\end{itemize}\n",
            "",
        )
        self.assertIn("intro.contributions", check_ids(introduction.intro_contributions(make_context(tex))))

    def test_no_intro_skips(self):
        tex = r"\begin{document}\section{Methods}x\end{document}"
        self.assertEqual(introduction.intro_contributions(make_context(tex)), [])


class ForwardRefTests(unittest.TestCase):
    def test_refs_in_list_pass(self):
        self.assertEqual(introduction.intro_forward_refs(make_context(GOOD)), [])

    def test_list_without_refs_warns(self):
        tex = GOOD.replace(
            r"A leakage audit of published pipelines (Section~\ref{sec:methods}).",
            "A leakage audit of published pipelines.",
        ).replace(
            r"A subject-level evaluation protocol (Section~\ref{sec:results}).",
            "A subject-level evaluation protocol.",
        )
        findings = introduction.intro_forward_refs(make_context(tex))
        self.assertIn("intro.forward-refs", check_ids(findings))

    def test_literal_section_number_passes(self):
        tex = GOOD.replace(
            r"A leakage audit of published pipelines (Section~\ref{sec:methods}).",
            "A leakage audit of published pipelines (Section~2).",
        ).replace(
            r"A subject-level evaluation protocol (Section~\ref{sec:results}).",
            "A subject-level evaluation protocol (Section 3).",
        )
        self.assertEqual(introduction.intro_forward_refs(make_context(tex)), [])

    def test_cref_passes(self):
        tex = GOOD.replace(r"Section~\ref{sec:methods}", r"\cref{sec:methods}").replace(
            r"Section~\ref{sec:results}", r"\Cref{sec:results}"
        )
        self.assertEqual(introduction.intro_forward_refs(make_context(tex)), [])

    def test_no_contribution_list_skips(self):
        tex = r"""
\begin{document}
\section{Introduction}
Prose only, no list at all.
\section{Methods}
x
\end{document}
"""
        self.assertEqual(introduction.intro_forward_refs(make_context(tex)), [])


if __name__ == "__main__":
    unittest.main()
