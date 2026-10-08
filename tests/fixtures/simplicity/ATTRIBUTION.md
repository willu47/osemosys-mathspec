# SIMPLICITY

The `data/` directory and `config.yaml` are copied unchanged from the OSeMOSYS
example model SIMPLICITY, <https://github.com/OSeMOSYS/simplicity>, at commit
`2e6a80ce99851aa53239f185d0ca87961fc95f73`. They are licensed under the
Creative Commons Attribution 4.0 International licence (see `LICENSE`).

## GLPK reference

`tests/test_end_to_end.py` compares against the objective GLPK 5.0 reports for
this data with `osemosys.txt` (OSeMOSYS_2017_11_08, identical to SIMPLICITY's
`OSeMOSYS.txt`):

```bash
otoole convert csv datafile data simplicity.txt config.yaml
pixi exec -s glpk glpsol -m ../../../osemosys.txt -d simplicity.txt
# OPTIMAL LP SOLUTION FOUND, obj = 4.497319670e+03
```
