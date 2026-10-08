# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

OSeMOSYS (an energy system optimisation model) whose formulation lives in [mathspec](https://mathspec.readthedocs.io) YAML fragments, one per OSeMOSYS block, merged into one spec. A generic engine turns that spec into a [linopy](https://github.com/PyPSA/linopy) model. [otoole](https://github.com/OSeMOSYS/otoole) reads the input data and writes the results. `README.md` holds the modelling decisions and the list of mathspec operators the engine does not build yet.

## Commands

```bash
uv sync                                    # install, incl. the pytest dev group
uv run pytest                              # whole suite (~15 s, needs HiGHS via highspy)
uv run pytest tests/test_engine.py::test_a_bare_shift_drops_the_row_at_the_vacated_edge
uv run pytest tests/test_end_to_end.py -k utopia   # one dataset end to end
uv run osemosys run csv tests/fixtures/simplicity/data tests/fixtures/simplicity/config.yaml \
    --to-path results/ --solver highs      # expect objective 4497.31967

uv run python -m mathspec check src/osemosys_mathspec/spec/06_storage.yaml   # one fragment; only `given` notes
uv run python -c "import mathspec, osemosys_mathspec as o; print(mathspec.advising.advice(o.load_spec()))"   # the merge; must be ()
uv run python -c "import mathspec, osemosys_mathspec as o; print(mathspec.to_markdown(o.load_spec()), end='')" > osemosys.md
```

No linter or formatter is configured in `pyproject.toml`. The code uses single quotes, `from __future__ import annotations`, and lines up to about 120 characters.

## Architecture

```
otoole.read ─▶ bridge/inputs.py ─▶ engine/check.py ─▶ engine/build.py ─▶ linopy solve
otoole.write ◀─ otoole ResultsPackage ◀─ bridge/results.py ◀──────────── solution
```

`api.run()` wires these steps together. `cli.py` is a thin wrapper over it.

### The spec is the source of truth

- `src/osemosys_mathspec/spec/` is the formulation, one fragment per OSeMOSYS block. It is translated from `osemosys.txt`, the original GNU MathProg file (OSeMOSYS_2017_11_08). Each constraint keeps its MathProg name, so compare against `osemosys.txt` when you change one.
- `api.load_spec()` merges the fragments with `mathspec.merge`, in sorted file order, under the description of `00_core.yaml`. The two-digit prefixes follow `osemosys.txt`, and the file order is the order of a merged sum's terms. The CLI (`python -m mathspec check|markdown`) reads one file, so the merge goes through Python.
- Each fragment must load alone. A name it reads from a sibling is a `given:` entry with the sibling's `dims` (an int parameter also needs `dtype: int`). A dimension it uses is declared again, identically, and its description is written once. Put a declaration in the block that defines it; a parameter several blocks read goes in `00_core.yaml`.
- A block adds to another block's sum with `adds_to:` on a given expression: TDC1 (`DiscountedCostByTechnology`, emissions), TDC2 (`DiscountedCostByRegion`, storage), EBa11 (`OutflowEachTS`, trade) and EBb4 (`OutflowAnnual`, trade).
- A fragment cannot divide by, or raise to the power of, an expression it reads under `given:` ([mathspec#862](https://github.com/energy-models/mathspec/issues/862)). So E5 writes `DiscountFactorMid` out in full, and `DiscountFactorMid` lives in `07_cost.yaml` with the one block that divides by it.
- `osemosys.md` is a rendering of the merged spec. Regenerate it after a spec change.
- The spec's `assumptions:` are the MathProg `check` statements. `engine/check.py` evaluates them against the data before the build.
- `mathspec` is pinned to `0.2.1`. An expression cannot read a dimension's coordinates, so `YearsSinceStart` and `YearsUntilEnd` are data prep. The discounting (`DiscountFactor`, `CapitalRecoveryFactor`, `PvAnnuity`, the salvage-value factors) is spec arithmetic on `(1 + rate)`, as `osemosys.txt` writes it, since 0.2.1 accepts a sum as a power base or divisor.
- The spec is not in `python -m mathspec canonical` form, so `canonical --check` fails on it. Do not run `canonical --write`: it reorders the file and drops all its comments.

### Engine (`engine/`): knows mathspec, not OSeMOSYS

- `evaluate.py` walks mathspec program nodes with `match` statements. A node it does not support raises `NotImplementedError` by name. To support a new operator, add a case there. Do not special-case OSeMOSYS.
- `terms.py` defines `Term(value, present, invalid)`. mathspec separates *absence* from zero, and linopy has no such idea. So every evaluated value carries:
  - `present`: false at a masked variable, a vacated `shift` edge, or a coordinate a relation does not map. Absence spreads through arithmetic and removes the row. A sum skips an absent summand instead.
  - `invalid`: true where parameter arithmetic gave NaN (such as 0/0), or where a non-finite number meets a variable. The value there is zeroed. `build.py` raises an error if a kept constraint row or the objective touches an invalid coordinate, so the solver never sees a non-finite coefficient.
  - `±inf` in data is a value: a bound passes it to linopy, and a `where:` comparison reads it as a number. `ModelData` refuses NaN in any parameter.
- `build.py` adds variables (masked by `where:`), then constraints, then the objective. It drops rows that have no variable terms left.
- `ModelData.coords` order is the order `shift`, `sum_back` and `position()` count in.

### Bridge (`bridge/`): knows otoole and OSeMOSYS

- `inputs.from_otoole` makes every parameter dense over its declared dims and fills every missing row with its otoole default. This matters because mathspec reads a missing row as 0, or as false in `where:`, but OSeMOSYS reads the default.
- Data-prep parameters (`YearsSinceStart`, `YearsUntilEnd`, `DailyTimeBracketCount`, `DiscountRateIdv`) are derived in `prep.py` and registered, in dependency order, in the `DERIVED` dict in `inputs.py`. A `DERIVED` entry applies only where otoole supplies the parameter neither rows nor a default, which is how `DiscountRateIdv` falls back to `DiscountRate`. A new data-prep parameter needs three things: a spec declaration, a function in `prep.py`, and a `DERIVED` entry.
- `_REGION` is the far end of a trade route. `SET_ALIASES` maps it to otoole's `REGION`. otoole names both columns `REGION`, so `results._spec_dims` maps a repeated index name back to its alias by position.
- `TradeReverse` is the only relation. `prep.trade_reverse` builds it.
- `prep.check_consecutive` refuses gaps in `YEAR`, `SEASON` and `DAYTYPE`. The spec reads the previous label by position, and MathProg reads it by value.
- `results.py` reads only the spec variables that the otoole config lists as `type: result`. A `ReadResults` subclass hands them to otoole, and otoole calculates every other listed result.

## Tests and fixtures

- `test_engine.py` checks each operator on tiny hand-written specs that are passed as dicts to `mathspec.to_spec`.
- `test_bridge.py` checks defaults, aliases and data prep against minimal otoole-shaped inputs.
- `test_end_to_end.py` solves SIMPLICITY and UTOPIA end to end. It asserts each dataset's GLPK objective from `GLPK_OBJECTIVE` (relative tolerance 1e-6) and that `advice(load_spec())` is empty. Per fragment, it asserts that advice holds only `given` notes. It also asserts that the merge without each optional block (trade, storage, limits, reserve margin, RE target, emissions) leaves nothing under `given` and that the bridge reads SIMPLICITY's data for it, and that `osemosys.md` equals `mathspec.to_markdown(load_spec())`. Any spec or engine change must keep these objectives. Run one dataset with `-k utopia` or `-k simplicity`.
- Each dataset fixture has `config.yaml` (otoole config), `data/` (otoole CSVs) and a note with the `glpsol` command that produced its reference (`ATTRIBUTION.md` or `REFERENCE.md`). A new dataset needs that layout and an entry in `GLPK_OBJECTIVE`.

## Outside the package

`results/` and `test.lp` (a 24 MB LP dump) are run outputs. The root `config.yaml` is an otoole user config that differs from the SIMPLICITY fixture's config. The VS Code workspace also opens the sibling repo `../OSeMOSYS/OSeMOSYS_GNU_MathProg`.
