# osemosys-mathspec

OSeMOSYS with its formulation kept in one [mathspec](https://mathspec.readthedocs.io)
file, the model built and solved with [linopy](https://github.com/PyPSA/linopy),
and the data read and written in every OSeMOSYS format by
[otoole](https://github.com/OSeMOSYS/otoole).

```bash
uv sync
uv run osemosys run csv tests/fixtures/simplicity/data tests/fixtures/simplicity/config.yaml \
    --to-path results/ --solver highs
# optimal: objective 4497.31967   (GLPK on osemosys.txt: 4.497319670e+03)
```

From Python:

```python
from osemosys_mathspec import run

result = run('config.yaml', 'csv', 'data/', to_format='excel', to_path='results.xlsx')
result.objective, result.model  # the linopy model, solved
```

## How it fits together

```
otoole.read ──▶ bridge/inputs.py ──▶ engine/check.py ──▶ engine/build.py ──▶ linopy solve
  (csv, excel,    dense defaults,       spec assumptions      spec.program →          │
   datafile)      data prep             on the data           linopy model            ▼
otoole.write ◀── otoole ResultsPackage ◀── bridge/results.py ◀──────────── solution
```

| Path | What it holds |
|---|---|
| `src/osemosys_mathspec/osemosys.yaml` | The formulation — OSeMOSYS_2017_11_08, translated from `osemosys.txt`. `python -m mathspec check` it; `python -m mathspec latex` prints it |
| `bridge/inputs.py` | otoole's frames to dense xarray arrays, **every** parameter filled with its otoole default |
| `bridge/prep.py` | The parameters the spec marks as data prep: `YearsSinceStart`, `YearsUntilEnd`, `DailyTimeBracketCount`, `DiscountRateIdv` where otoole has none, and the `TradeReverse` relation |
| `engine/evaluate.py` | A generic evaluator of mathspec program nodes. It knows mathspec, not OSeMOSYS |
| `engine/build.py` | Variables, constraints and objective added to a linopy model |
| `engine/check.py` | The spec's `assumptions:` (the MathProg `check` statements), held against the data before the build |
| `bridge/results.py` | Solved variables as otoole results. otoole's ResultsPackage calculates any other result the config lists |

## Decisions worth knowing

- **Every otoole default is filled in.** In mathspec a missing parameter row is 0 in
  arithmetic and *false* in a `where:` comparison. OSeMOSYS reads the default
  instead, and in SIMPLICITY `OperationalLifeStorage` (default 0, no rows) decides
  which salvage-value rows exist.
- **Absence is tracked by the engine.** A masked variable, the vacated edge of a
  `shift` and a coordinate a relation does not map remove the row. Inside a sum
  they remove one summand. linopy has no such notion, so every evaluated value
  carries a `present` mask.
- **A non-finite coefficient is refused.** NaN from parameter arithmetic (such as
  0/0), and `±inf` next to a variable, are recorded as invalid. A constraint that
  keeps a row there, or an objective that reads one, raises an error rather than
  handing it to the solver. Elsewhere `±inf` is a value: an infinite bound leaves
  that side open. NaN in a parameter is refused when the data is attached.
- **A window of 0 is empty.** `sum_back(..., window=OperationalLife)` with a life of
  0 accumulates nothing, as MathProg's `sum{yy: 0 <= y-yy < 0}` does.
- **Years, seasons and day types must be consecutive integers**, because the spec
  reads the previous one by position. The bridge refuses a gap.

## What the engine does not build yet

`sum(by=)`, `shift` with `by=`, `edge='wrap'` or a named offset, `sum_back` with
`by=` or `edge='wrap'`, `at` joining on further key columns, `position(by=)`, and
relation, count and pulled-back tests in a `where:`. Each raises
`NotImplementedError` by name. The OSeMOSYS spec uses none of them.

## Tests

`uv run pytest` runs the operators on hand-checkable specs, the bridge, and
SIMPLICITY and UTOPIA end to end against GLPK's objective (relative tolerance
1e-6). The SIMPLICITY data is CC-BY-4.0. See `tests/fixtures/simplicity/ATTRIBUTION.md`.
The UTOPIA reference is in `tests/fixtures/utopia/REFERENCE.md`.
