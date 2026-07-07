# SPDX-License-Identifier: Apache-2.0
import unittest

from tests.helpers import check_ids, make_context

from papercheck.checks import floats

CLEAN = r"""
\begin{document}
As the dashed line in Figure~\ref{fig:acc} shows, accuracy rises with data.
\begin{figure}
\includegraphics{acc.png}
\caption{Accuracy versus data volume.}
\label{fig:acc}
\end{figure}
\end{document}
"""


class FloatTests(unittest.TestCase):
    def test_clean_passes(self):
        ctx = make_context(CLEAN)
        for fn in (floats.floats_caption, floats.floats_label, floats.floats_referenced,
                   floats.floats_ref_before, floats.floats_color_only):
            self.assertEqual(fn(ctx), [], fn.__name__)

    def test_missing_caption_errors(self):
        tex = r"\begin{document}\begin{figure}\includegraphics{x}\label{fig:x}\end{figure}\ref{fig:x}\end{document}"
        self.assertIn("floats.caption", check_ids(floats.floats_caption(make_context(tex))))

    def test_missing_label_warns(self):
        tex = r"\begin{document}\begin{figure}\includegraphics{x}\caption{c}\end{figure}\end{document}"
        self.assertIn("floats.label", check_ids(floats.floats_label(make_context(tex))))

    def test_unreferenced_errors(self):
        tex = r"\begin{document}\begin{figure}\caption{c}\label{fig:x}\end{figure}\end{document}"
        self.assertIn("floats.referenced", check_ids(floats.floats_referenced(make_context(tex))))

    def test_ref_after_warns(self):
        tex = r"\begin{document}\begin{figure}\caption{c}\label{fig:x}\end{figure} later see \ref{fig:x}.\end{document}"
        self.assertIn("floats.ref-before", check_ids(floats.floats_ref_before(make_context(tex))))

    def test_color_only_warns(self):
        tex = r"\begin{document}The red line is higher than the blue curve.\end{document}"
        self.assertIn("floats.color-only", check_ids(floats.floats_color_only(make_context(tex))))

    def test_shown_in_color_warns(self):
        tex = r"\begin{document}The baseline is shown in green.\end{document}"
        self.assertIn("floats.color-only", check_ids(floats.floats_color_only(make_context(tex))))


if __name__ == "__main__":
    unittest.main()
