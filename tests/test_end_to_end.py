"""Each dataset end to end: otoole CSVs in, HiGHS, otoole CSVs out, GLPK's objective matched."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest
from mathspec.advising import advice

from osemosys_mathspec import SPEC_PATH, run

FIXTURES = Path(__file__).parent / 'fixtures'

#: GLPK 5.0 on osemosys.txt with each dataset — see the fixture's ATTRIBUTION.md or REFERENCE.md.
GLPK_OBJECTIVE = {'simplicity': 4.497319670e3, 'utopia': 2.974758860e4}


@pytest.fixture(scope='module', params=sorted(GLPK_OBJECTIVE))
def solved(request, tmp_path_factory):
    dataset = FIXTURES / request.param
    out = tmp_path_factory.mktemp(request.param)
    result = run(dataset / 'config.yaml', 'csv', dataset / 'data', to_format='csv', to_path=out)
    return request.param, result, out


def test_the_spec_loads_with_no_advice():
    assert tuple(advice(SPEC_PATH)) == ()


def test_objective_matches_glpk(solved):
    name, result, _ = solved
    assert (result.status, result.termination) == ('ok', 'optimal')
    assert result.objective == pytest.approx(GLPK_OBJECTIVE[name], rel=1e-6)


def test_results_are_written_in_otoole_csv(solved):
    _, result, out = solved
    written = pd.read_csv(out / 'TotalDiscountedCost.csv')
    assert list(written.columns) == ['REGION', 'YEAR', 'VALUE']
    assert written['VALUE'].sum() == pytest.approx(result.objective, rel=1e-9)
    # otoole names a result's columns after its config indices, so both ends of a route are REGION.
    header = (out / 'Trade.csv').read_text().splitlines()[0]
    assert header == 'REGION,REGION,TIMESLICE,FUEL,YEAR,VALUE'
