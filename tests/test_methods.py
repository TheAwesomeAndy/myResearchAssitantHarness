# SPDX-License-Identifier: Apache-2.0
import unittest

from tests.helpers import check_ids, make_context

from papercheck.checks import methods

GOOD = r"""
\documentclass{article}
\begin{document}
\section{Introduction}
We study affective decoding from wearable sensors.
\section{Methods}
Twenty participants completed the recording protocol.
We evaluated every model with leave-one-subject-out cross-validation.
Performance was compared against a logistic regression baseline.
We fixed the random seed to 7 and report all hyperparameters.
An ablation study mapped where accuracy degraded under channel dropout.
\section{Results}
The proposed model outperformed the baseline.
\end{document}
"""


class PresentTests(unittest.TestCase):
    def test_methods_section_passes(self):
        self.assertEqual(methods.methods_present(make_context(GOOD)), [])

    def test_sections_without_methods_warns(self):
        tex = r"""
\documentclass{article}
\begin{document}
\section{Introduction}
We study wearable sensing.
\section{Results}
Accuracy was high.
\end{document}
"""
        self.assertIn("methods.present", check_ids(methods.methods_present(make_context(tex))))

    def test_unsectioned_document_is_ignored(self):
        tex = r"\begin{document}Just prose, no sections at all.\end{document}"
        self.assertEqual(methods.methods_present(make_context(tex)), [])

    def test_materials_title_counts_as_methods(self):
        tex = r"\begin{document}\section{Materials and Procedure}We recorded data.\end{document}"
        self.assertEqual(methods.methods_present(make_context(tex)), [])


class BaselineTests(unittest.TestCase):
    def test_baseline_language_passes(self):
        self.assertEqual(methods.methods_baseline(make_context(GOOD)), [])

    def test_missing_baseline_is_error(self):
        tex = r"\begin{document}\section{Methods}We trained a network and reported accuracy.\end{document}"
        findings = methods.methods_baseline(make_context(tex))
        self.assertIn("methods.baseline", check_ids(findings))
        self.assertIn("explicit baselines", findings[0].message)


class LeakageTests(unittest.TestCase):
    def test_loso_suppresses_warning(self):
        self.assertEqual(methods.methods_leakage(make_context(GOOD)), [])

    def test_pooled_cv_with_participants_warns(self):
        tex = (
            r"\begin{document}\section{Methods}Thirty participants completed the protocol. "
            r"We evaluated the classifier with 10-fold cross-validation.\end{document}"
        )
        findings = methods.methods_leakage(make_context(tex))
        self.assertIn("methods.leakage", check_ids(findings))
        self.assertIn("leakage", findings[0].message)
        self.assertIn("leave-one-subject-out", findings[0].suggestion)
        self.assertGreater(findings[0].line, 0)

    def test_no_human_subjects_passes(self):
        tex = r"\begin{document}\section{Methods}We used 10-fold cross-validation over synthetic traces.\end{document}"
        self.assertEqual(methods.methods_leakage(make_context(tex)), [])

    def test_config_flag_enables_check_without_subject_words(self):
        tex = r"\begin{document}\section{Methods}We used 10-fold cross-validation over the recordings.\end{document}"
        ctx = make_context(tex, {"venue": {"human_subjects": True}})
        self.assertIn("methods.leakage", check_ids(methods.methods_leakage(ctx)))

    def test_no_cross_validation_passes(self):
        tex = r"\begin{document}\section{Methods}Participants completed a held-out test split.\end{document}"
        self.assertEqual(methods.methods_leakage(make_context(tex)), [])


class ReproducibilityTests(unittest.TestCase):
    def test_seed_language_passes(self):
        self.assertEqual(methods.methods_reproducibility(make_context(GOOD)), [])

    def test_missing_details_warns(self):
        tex = r"\begin{document}\section{Methods}We trained the model on held-out recordings.\end{document}"
        findings = methods.methods_reproducibility(make_context(tex))
        self.assertIn("methods.reproducibility", check_ids(findings))
        self.assertIn("seeds", findings[0].message)


class RobustnessTests(unittest.TestCase):
    def test_ablation_language_passes(self):
        self.assertEqual(methods.methods_robustness(make_context(GOOD)), [])

    def test_missing_robustness_warns(self):
        tex = r"\begin{document}\section{Methods}We reported the mean accuracy over five runs.\end{document}"
        findings = methods.methods_robustness(make_context(tex))
        self.assertIn("methods.robustness", check_ids(findings))
        self.assertIn("ablations", findings[0].message)


class FutureTenseTests(unittest.TestCase):
    def test_past_tense_methods_pass(self):
        self.assertEqual(methods.methods_future_tense(make_context(GOOD)), [])

    def test_future_tense_in_methods_warns(self):
        tex = (
            r"\begin{document}\section{Methods}We will record thirty sessions and "
            r"we plan to measure heart rate variability.\end{document}"
        )
        findings = methods.methods_future_tense(make_context(tex))
        self.assertIn("methods.future-tense", check_ids(findings))
        self.assertEqual(len(findings), 2)
        self.assertIn("past tense", findings[0].message)

    def test_future_tense_outside_methods_is_ignored(self):
        tex = r"\begin{document}\section{Methods}We recorded data.\section{Future Plans}We will extend this.\end{document}"
        self.assertEqual(methods.methods_future_tense(make_context(tex)), [])

    def test_no_methods_section_returns_nothing(self):
        tex = r"\begin{document}\section{Introduction}We will do things later.\end{document}"
        self.assertEqual(methods.methods_future_tense(make_context(tex)), [])


if __name__ == "__main__":
    unittest.main()
