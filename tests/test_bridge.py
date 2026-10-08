"""The otoole bridge: defaults, set aliases and data prep."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

from osemosys_mathspec import load_spec
from osemosys_mathspec.bridge import prep
from osemosys_mathspec.bridge.inputs import from_otoole
from osemosys_mathspec.bridge.results import _spec_dims
from osemosys_mathspec.engine.build import build

SIMPLICITY_CONFIG = Path(__file__).parent / 'fixtures' / 'simplicity' / 'config.yaml'


@pytest.fixture(scope='module')
def program():
    return load_spec().program


@pytest.fixture(scope='module')
def defaults():
    """Every parameter's default, as otoole's config gives them."""
    config = yaml.safe_load(SIMPLICITY_CONFIG.read_text())
    return {name: entry['default'] for name, entry in config.items() if entry['type'] == 'param'}


def minimal_inputs() -> dict[str, pd.DataFrame]:
    """Every set, one label or a few each, and no parameter rows at all."""
    sets = {
        'REGION': ['R1', 'R2'],
        'TECHNOLOGY': ['T'],
        'TIMESLICE': ['L'],
        'FUEL': ['F'],
        'EMISSION': ['E'],
        'MODE_OF_OPERATION': [1],
        'YEAR': [2021, 2020, 2022],
        'SEASON': [1],
        'DAYTYPE': [1],
        'DAILYTIMEBRACKET': [1, 2],
        'STORAGE': ['S'],
    }
    return {name: pd.DataFrame({'VALUE': labels}) for name, labels in sets.items()}


def with_parameter(inputs, name, index_names, rows):
    """A parameter frame as otoole returns one, index names repeated where a set is (REGION, REGION)."""
    index = pd.MultiIndex.from_tuples([row[:-1] for row in rows], names=index_names)
    frame = pd.DataFrame({'VALUE': [row[-1] for row in rows]}, index=index, dtype=float)
    return {**inputs, name: frame}


def test_every_parameter_is_dense_with_its_default(program, defaults):
    inputs = with_parameter(minimal_inputs(), 'AvailabilityFactor', ['REGION', 'TECHNOLOGY', 'YEAR'], [])
    data = from_otoole(inputs, defaults, program)
    assert (data.parameters['AvailabilityFactor'] == 1).all()
    assert data.parameters['AvailabilityFactor'].dims == ('REGION', 'TECHNOLOGY', 'YEAR')


def test_integer_sets_are_ordered_and_years_counted(program, defaults):
    data = from_otoole(minimal_inputs(), defaults, program)
    assert data.coords['YEAR'].tolist() == [2020, 2021, 2022]
    np.testing.assert_array_equal(data.parameters['YearsSinceStart'], [0, 1, 2])
    np.testing.assert_array_equal(data.parameters['YearsUntilEnd'], [3, 2, 1])
    assert int(data.parameters['DailyTimeBracketCount']) == 2


def test_the_second_region_of_a_route_is_the_alias(program, defaults):
    inputs = with_parameter(
        minimal_inputs(), 'TradeRoute', ['REGION', 'REGION', 'FUEL', 'YEAR'], [('R1', 'R2', 'F', 2020, 1.0)]
    )
    route = from_otoole(inputs, defaults, program).parameters['TradeRoute']
    assert route.dims == ('REGION', '_REGION', 'FUEL', 'YEAR')
    assert float(route.sel(REGION='R1', _REGION='R2', FUEL='F', YEAR=2020)) == 1
    assert float(route.sum()) == 1


def test_a_route_over_the_wrong_sets_is_refused_unless_empty(program, defaults):
    wrong = with_parameter(minimal_inputs(), 'TradeRoute', ['REGION', 'FUEL', 'YEAR'], [('R1', 'F', 2020, 1.0)])
    with pytest.raises(ValueError, match="'TradeRoute' arrives over"):
        from_otoole(wrong, defaults, program)
    empty = with_parameter(minimal_inputs(), 'TradeRoute', ['REGION', 'FUEL', 'YEAR'], [])
    assert float(from_otoole(empty, defaults, program).parameters['TradeRoute'].sum()) == 0


def test_a_gap_in_the_years_is_refused(program, defaults):
    inputs = minimal_inputs()
    inputs['YEAR'] = pd.DataFrame({'VALUE': [2020, 2022]})
    with pytest.raises(ValueError, match='YEAR must be consecutive'):
        from_otoole(inputs, defaults, program)


def test_trade_reverse_maps_each_route_to_its_far_end():
    coords = {'REGION': pd.Index(['A', 'B'], name='REGION'), '_REGION': pd.Index(['A', 'B'], name='_REGION')}
    table = prep.trade_reverse(coords).set_index(['REGION', '_REGION'])
    assert tuple(table.loc[('A', 'B')]) == ('B', 'A')


@pytest.mark.parametrize(('rows', 'expected'), [(None, [0.08, 0.08]), ([('R2', 'T', 0.2)], [0.07, 0.2])])
def test_discount_rate_idv_is_the_regions_rate_unless_otoole_supplies_it(program, defaults, rows, expected):
    inputs = minimal_inputs()
    defaults = {**defaults, 'DiscountRate': 0.08}
    if rows is not None:
        inputs = with_parameter(inputs, 'DiscountRateIdv', ['REGION', 'TECHNOLOGY'], rows)
        defaults['DiscountRateIdv'] = 0.07
    rate = from_otoole(inputs, defaults, program).parameters['DiscountRateIdv']
    assert rate.dims == ('REGION', 'TECHNOLOGY')
    np.testing.assert_allclose(rate.sel(TECHNOLOGY='T'), expected)


@pytest.mark.parametrize('rate', ['DiscountRate', 'DiscountRateIdv'])
def test_a_zero_discount_rate_is_refused_where_capital_is_recovered(program, defaults, rate):
    data = from_otoole(minimal_inputs(), {**defaults, rate: 0.0}, program)
    with pytest.raises(ValueError, match="'CC1_UndiscountedCapitalInvestment'.*non-finite"):
        build(program, data, check=False)


def test_otoole_indices_name_the_alias_second():
    assert _spec_dims(['REGION', 'REGION', 'FUEL'], ('REGION', '_REGION', 'FUEL'), 'Trade') == [
        'REGION',
        '_REGION',
        'FUEL',
    ]
