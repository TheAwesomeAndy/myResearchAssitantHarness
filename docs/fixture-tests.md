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

The fixture runner writes a JSON report to `harness/reports/fixture_report.json`.
