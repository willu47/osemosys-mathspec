"""Each dataset end to end: otoole CSVs in, HiGHS, otoole CSVs out, GLPK's objective matched."""

from __future__ import annotations

from pathlib import Path

import mathspec
import otoole
import pandas as pd
import pytest
from mathspec.advising import advice

from osemosys_mathspec import SPEC_PATH, load_spec, run
from osemosys_mathspec.bridge.inputs import from_otoole

ROOT = Path(__file__).parents[1]
FIXTURES = ROOT / 'tests' / 'fixtures'

#: GLPK 5.0 on osemosys.txt with each dataset — see the fixture's ATTRIBUTION.md or REFERENCE.md.
GLPK_OBJECTIVE = {'simplicity': 4.497319670e3, 'utopia': 2.974758860e4}

FRAGMENTS = sorted(SPEC_PATH.glob('*.yaml'))
OPTIONAL = ('04_trade', '06_storage', '08_limits', '09_reserve_margin', '10_re_target', '11_emissions')


@pytest.fixture(scope='module', params=sorted(GLPK_OBJECTIVE))
def solved(request, tmp_path_factory):
    dataset = FIXTURES / request.param
    out = tmp_path_factory.mktemp(request.param)
    result = run(dataset / 'config.yaml', 'csv', dataset / 'data', to_format='csv', to_path=out)
    return request.param, result, out


@pytest.fixture(scope='module')
def simplicity_inputs():
    dataset = FIXTURES / 'simplicity'
    return otoole.read(str(dataset / 'config.yaml'), 'csv', str(dataset / 'data'))


def test_the_merged_spec_loads_with_no_advice():
    assert advice(load_spec()) == ()


def test_osemosys_md_renders_the_merged_spec():
    assert (ROOT / 'osemosys.md').read_text() == mathspec.to_markdown(load_spec())


def test_a_fragment_loads_alone_as_a_file_and_describes_the_merge():
    assert load_spec(FRAGMENTS[0]).description == load_spec().description


def test_a_folder_without_fragments_is_refused(tmp_path):
    with pytest.raises(ValueError, match=r'no \*\.yaml fragments'):
        load_spec(tmp_path)


@pytest.mark.parametrize('path', FRAGMENTS, ids=lambda path: path.stem)
def test_a_fragment_is_advised_only_of_what_it_reads_from_its_siblings(path):
    assert {note.kind for note in advice(path)} <= {'given'}


@pytest.mark.parametrize('left_out', OPTIONAL)
def test_the_spec_merges_whole_and_reads_its_data_without_an_optional_fragment(left_out, simplicity_inputs):
    fragments = [path for path in FRAGMENTS if path.stem != left_out]
    assert len(fragments) == len(FRAGMENTS) - 1
    program = mathspec.merge(fragments).program
    assert not program.given
    assert set(from_otoole(*simplicity_inputs, program).parameters) == set(program.parameters)


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
