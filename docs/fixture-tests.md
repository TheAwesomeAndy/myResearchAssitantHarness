# Fixture Tests

The fixture suite checks whether the harness catches known failure modes.

Run it with:

```bash
make -f makefiles/ManuscriptHarness.mk harness-fixtures
```

Included cases:

- good manifest should pass
- bad table value should fail
- bad citation log should fail
- forbidden phrase should fail
- path marker should fail
- LaTeX build fixtures run only when a LaTeX engine is installed

Academic quality checks now include:

- `scripts/qgate.py` for roadmap filler and overclaim checks
- `scripts/check_heading.py` for title length and question-title checks
- `scripts/check_summary.py` for abstract length and sentence-count checks
- `scripts/check_signals.py` for baseline, limitation, ethics, and availability signals
- `makefiles/AcademicHarness.mk` for running those checks together

The fixture runner writes a JSON report to `harness/reports/fixture_report.json`.
