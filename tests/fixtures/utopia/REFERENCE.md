# UTOPIA

`config.yaml` is a copy of SIMPLICITY's otoole config. It declares exactly the
sets and parameters in `data/`.

## GLPK reference

`tests/test_end_to_end.py` compares against the objective GLPK 5.0 reports for
this data with `osemosys.txt` (OSeMOSYS_2017_11_08):

```bash
# from the repository root; glpsol writes results/SelectedResults.csv into its working directory
uv run otoole convert csv datafile tests/fixtures/utopia/data utopia.txt tests/fixtures/utopia/config.yaml
pixi exec -s glpk glpsol -m osemosys.txt -d utopia.txt
# OPTIMAL LP SOLUTION FOUND, obj = 2.974758860e+04
```

GLPK passes every `check` statement and solves the problem as an LP (no integer columns).
HiGHS through this package gives 29747.59421, a relative difference of 1.9e-7.
