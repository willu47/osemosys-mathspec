# osemosys-mathspec

OSeMOSYS with its formulation kept as [mathspec](https://mathspec.readthedocs.io)
fragments, one per OSeMOSYS block, merged into one spec, the model built and
solved with [linopy](https://github.com/PyPSA/linopy),
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
| `src/osemosys_mathspec/spec/` | The formulation — OSeMOSYS_2017_11_08, translated from `osemosys.txt`, one fragment per block. `api.load_spec()` merges them; `osemosys.md` renders the merge |
| `bridge/inputs.py` | otoole's frames to dense xarray arrays, **every** parameter filled with its otoole default |
| `bridge/prep.py` | The parameters the spec marks as data prep: `YearsSinceStart`, `YearsUntilEnd`, `DailyTimeBracketCount`, `DiscountRateIdv` where otoole has none, and the `TradeReverse` relation |
| `engine/evaluate.py` | A generic evaluator of mathspec program nodes. It knows mathspec, not OSeMOSYS |
| `engine/build.py` | Variables, constraints and objective added to a linopy model |
| `engine/check.py` | The spec's `assumptions:` (the MathProg `check` statements), held against the data before the build |
| `bridge/results.py` | Solved variables as otoole results. otoole's ResultsPackage calculates any other result the config lists |

## The spec in fragments

Each file in `spec/` is one OSeMOSYS block and loads on its own. The two-digit
prefixes follow `osemosys.txt`, and `load_spec()` merges the files in that order:

`00_core` (the model description and the parameters several blocks read),
`01_demand`, `02_capacity`, `03_balance`, `04_trade`, `05_accounting`,
`06_storage`, `07_cost` (with the objective), `08_limits`, `09_reserve_margin`,
`10_re_target`, `11_emissions`.

- A name one fragment reads from another is a `given:` entry with its `dims`.
- A block that adds to another block's sum does so with `adds_to:`. Four sums are
  built this way: emissions adds its penalty to `DiscountedCostByTechnology`
  (TDC1), storage adds its cost to `DiscountedCostByRegion` (TDC2), and trade adds
  its flows to `OutflowEachTS` (EBa11) and `OutflowAnnual` (EBb4).
- Trade, storage, the limits, the reserve margin, the renewable target and
  emissions are optional: the merge without any one of them still resolves, and
  the bridge still reads its data.
- A fragment cannot divide by an expression it reads under `given:`
  ([mathspec#862](https://github.com/energy-models/mathspec/issues/862)), so E5
  writes `DiscountFactorMid` out in full.

```bash
uv run python -m mathspec check src/osemosys_mathspec/spec/06_storage.yaml   # only `given` notes
uv run python -c "import mathspec, osemosys_mathspec as o; print(mathspec.to_markdown(o.load_spec()), end='')" > osemosys.md
```

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

`uv run pytest` runs the operators on hand-checkable specs, the bridge, the
fragments (each loads alone, the merge has no advice and renders as `osemosys.md`,
the merge without each optional block resolves and reads SIMPLICITY's data), and SIMPLICITY and UTOPIA end to end against GLPK's objective
(relative tolerance 1e-6). The SIMPLICITY data is CC-BY-4.0. See `tests/fixtures/simplicity/ATTRIBUTION.md`.
The UTOPIA reference is in `tests/fixtures/utopia/REFERENCE.md`.

`tests/features/` states OSeMOSYS behaviour in Gherkin, one feature per block: demand
is met at least cost, capacity covers the peak, salvage value is credited, a limit
binds, storage shifts energy into the night. Each scenario is a model small enough to
work out by hand, and its expected values were worked out from `osemosys.txt` and
matched by GLPK on it. `tests/test_behaviour.py` holds the steps:

```gherkin
Scenario: Residual capacity is used before new capacity is built
  Given ResidualCapacity is
    | REGION | TECHNOLOGY | YEAR | VALUE |
    | R1     | PLANT      | *    | 60    |
  When the model is solved
  Then NewCapacity is
    | REGION | TECHNOLOGY | YEAR | VALUE |
    | R1     | PLANT      | 2020 | 100   |
```

A table's columns are the parameter's or variable's dims, `*` is every label of that
set, and a row the scenario leaves out takes its otoole default. The suite runs on
every core (`-n auto`, pytest-xdist); pass `-n0` to run in one process.
