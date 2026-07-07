# SPDX-License-Identifier: Apache-2.0
import unittest

from tests.helpers import make_context

from papercheck import latex


class StripCommentsTests(unittest.TestCase):
    def test_strips_comment_preserving_offsets(self):
        text = "alpha % hidden\nbeta"
        stripped = latex.strip_comments(text)
        self.assertEqual(len(stripped), len(text))
        self.assertNotIn("hidden", stripped)
        self.assertIn("beta", stripped)

    def test_escaped_percent_kept(self):
        stripped = latex.strip_comments(r"accuracy of 95\% held")
        self.assertIn(r"95\%", stripped)


class SectionTests(unittest.TestCase):
    def test_section_bodies(self):
        ctx = make_context(
            r"""\begin{document}
\section{Introduction}
intro text
\section{Methods}
methods text
\subsection{Data}
data text
\section{Results}
results text
\end{document}"""
        )
        found = latex.sections(ctx.doc.text)
        titles = [section.title for section in found]
        self.assertEqual(titles, ["Introduction", "Methods", "Data", "Results"])
        methods = latex.find_section(found, "method")
        self.assertIn("methods text", methods.body)
        self.assertIn("data text", methods.body)
        self.assertNotIn("results text", methods.body)


class SentenceTests(unittest.TestCase):
    def test_abbreviations_do_not_split(self):
        parts = latex.sentences("We used e.g. filters and Fig. 2 shows results. It worked.")
        self.assertEqual(len(parts), 2)

    def test_decimal_points_do_not_split(self):
        parts = latex.sentences("Accuracy reached 0.71 on average. Recall was lower.")
        self.assertEqual(len(parts), 2)


class DetexTests(unittest.TestCase):
    def test_commands_removed_words_kept(self):
        plain = latex.detex(r"We \emph{show} that $x^2$ holds \cite{a} in Section~\ref{sec:x}.")
        self.assertIn("show", plain)
        self.assertNotIn("cite", plain)
        self.assertNotIn("$", plain)


class InputExpansionTests(unittest.TestCase):
    def test_input_expanded_with_source_map(self):
        import tempfile
        from pathlib import Path

        tmp = Path(tempfile.mkdtemp(prefix="papercheck-test-"))
        (tmp / "child.tex").write_text("child body text\n", encoding="utf-8")
        main = tmp / "main.tex"
        main.write_text("\\begin{document}\n\\input{child}\nafter\n\\end{document}\n", encoding="utf-8")
        doc = latex.load_document(main)
        self.assertIn("child body text", doc.text)
        pos = doc.text.find("child body text")
        path, line = doc.location(pos)
        self.assertTrue(path.endswith("child.tex"))
        self.assertEqual(line, 1)


class CiteTests(unittest.TestCase):
    def test_cite_variants(self):
        keys = [key for key, _ in latex.cite_keys(r"\cite{a} \citep[p.~3]{b,c} \citet{d}")]
        self.assertEqual(keys, ["a", "b", "c", "d"])


if __name__ == "__main__":
    unittest.main()
