"""Each engine operator on a spec small enough to check by hand."""

from __future__ import annotations

import mathspec
import numpy as np
import pandas as pd
import pytest
import xarray as xr

from osemosys_mathspec.engine.build import build
from osemosys_mathspec.engine.evaluate import ModelData


def solve(spec: dict, data: ModelData):
    model = build(mathspec.to_spec(spec).program, data)
    status, termination = model.solve(solver_name='highs', output_flag=False)
    assert (status, termination) == ('ok', 'optimal')
    return model


def years(n: int) -> pd.Index:
    return pd.Index(range(2020, 2020 + n), name='year')


def over(values, **coords) -> xr.DataArray:
    return xr.DataArray(np.asarray(values), coords=coords, dims=list(coords))


def test_sum_back_with_a_named_window_and_an_empty_one():
    spec = {
        'dimensions': {'tech': {}, 'year': {'dtype': 'int'}},
        'parameters': {'built': {'dims': ['tech', 'year']}, 'life': {'dims': ['tech'], 'dtype': 'int'}},
        'variables': {
            'build': {'dims': ['tech', 'year'], 'bounds': {'lower': 'built', 'upper': 'built'}},
            'active': {'dims': ['tech', 'year']},
        },
        'constraints': {
            'in_service': {'dims': ['tech', 'year'], 'expression': 'active == sum_back(build, along=year, window=life)'}
        },
        'objective': {'sense': 'minimize', 'expression': 'sum(active)'},
    }
    tech, year = pd.Index(['a', 'b'], name='tech'), years(4)
    built = over([[1.0, 2.0, 4.0, 8.0], [1.0, 1.0, 1.0, 1.0]], tech=tech, year=year)
    data = ModelData({'tech': tech, 'year': year}, {'built': built, 'life': over([2, 0], tech=tech)})
    active = solve(spec, data).variables['active'].solution
    np.testing.assert_allclose(active.sel(tech='a'), [1, 3, 6, 12])
    np.testing.assert_allclose(active.sel(tech='b'), [0, 0, 0, 0])


def test_a_bare_shift_drops_the_row_at_the_vacated_edge():
    spec = {
        'dimensions': {'year': {'dtype': 'int'}},
        'variables': {'x': {'dims': ['year'], 'bounds': {'lower': 0}}},
        'constraints': {'grows': {'dims': ['year'], 'expression': 'x >= shift(x, along=year, offset=1) + 1'}},
        'objective': {'sense': 'minimize', 'expression': 'sum(x)'},
    }
    model = solve(spec, ModelData({'year': years(3)}, {}))
    np.testing.assert_allclose(model.variables['x'].solution, [0, 1, 2])
    assert int((model.constraints['grows'].labels != -1).sum()) == 2


def test_at_through_a_relation_reads_the_transpose():
    spec = {
        'dimensions': {'r': {}, 'rr': {}},
        'relations': {'reverse': {'key': ['r', 'rr'], 'values': {'back_r': 'r', 'back_rr': 'rr'}}},
        'parameters': {'p': {'dims': ['r', 'rr']}},
        'variables': {'q': {'dims': ['r', 'rr']}},
        'constraints': {
            'mirror': {'dims': ['r', 'rr'], 'expression': 'q == at(p, by=reverse, over=[back_r, back_rr], into=[r, rr])'}
        },
        'objective': {'sense': 'minimize', 'expression': 'sum(q)'},
    }
    r, rr = pd.Index(['A', 'B'], name='r'), pd.Index(['A', 'B'], name='rr')
    pairs = pd.MultiIndex.from_product([r, rr]).to_frame(index=False, name=['r', 'rr'])
    pairs['back_r'], pairs['back_rr'] = pairs['rr'], pairs['r']
    p = over([[1.0, 2.0], [3.0, 4.0]], r=r, rr=rr)
    model = solve(spec, ModelData({'r': r, 'rr': rr}, {'p': p}, {'reverse': pairs}))
    np.testing.assert_allclose(model.variables['q'].solution, p.T.values)


def test_cases_seed_the_first_position_and_carry_the_rest():
    spec = {
        'dimensions': {'year': {'dtype': 'int'}},
        'parameters': {'start': {'dims': []}, 'inflow': {'dims': ['year']}},
        'variables': {'level': {'dims': ['year']}},
        'expressions': {
            'carried': {
                'dims': ['year'],
                'cases': {'first': {'when': 'position(year) == 0', 'expression': 'start'}},
                'otherwise': 'shift(level, along=year, offset=1)',
            }
        },
        'constraints': {'balance': {'dims': ['year'], 'expression': 'level == carried + inflow'}},
        'objective': {'sense': 'minimize', 'expression': 'sum(level)'},
    }
    year = years(3)
    data = ModelData({'year': year}, {'start': xr.DataArray(10.0), 'inflow': over([1.0, 2.0, 3.0], year=year)})
    np.testing.assert_allclose(solve(spec, data).variables['level'].solution, [11, 13, 16])


def test_a_masked_variable_removes_the_row_outside_a_sum_and_one_summand_inside():
    spec = {
        'dimensions': {'g': {}},
        'parameters': {'cap': {'dims': ['g']}},
        'variables': {
            'x': {'dims': ['g'], 'bounds': {'lower': 0}},
            'y': {'dims': ['g'], 'where': 'cap > 0', 'bounds': {'lower': 0}},
        },
        'constraints': {
            'each': {'dims': ['g'], 'expression': 'x + y >= 1'},
            'total': {'dims': [], 'expression': 'sum(y, over=g) >= 5'},
        },
        'objective': {'sense': 'minimize', 'expression': 'sum(x) + sum(y)'},
    }
    g = pd.Index(['wind', 'gas', 'old'], name='g')
    model = solve(spec, ModelData({'g': g}, {'cap': over([10.0, 5.0, 0.0], g=g)}))
    assert int((model.constraints['each'].labels != -1).sum()) == 2
    assert model.objective.value == pytest.approx(5.0)


def test_data_that_breaks_an_assumption_is_refused():
    spec = {
        'dimensions': {'g': {}},
        'parameters': {'share': {'dims': ['g']}},
        'variables': {'x': {'dims': ['g'], 'bounds': {'lower': 0}}},
        'constraints': {'c': {'dims': ['g'], 'expression': 'x >= share'}},
        'objective': {'sense': 'minimize', 'expression': 'sum(x)'},
        'assumptions': {'share_is_a_fraction': 'share >= 0 AND share <= 1'},
    }
    g = pd.Index(['a', 'b'], name='g')
    with pytest.raises(ValueError, match='share_is_a_fraction'):
        build(mathspec.to_spec(spec).program, ModelData({'g': g}, {'share': over([0.5, 2.0], g=g)}))


@pytest.mark.parametrize(
    ('constraint', 'objective', 'd', 'refused'),
    [
        ('x / d == 1', 'sum(x)', 0.0, "Constraint 'c'.*non-finite"),
        ('d * x == 1', 'sum(x)', np.inf, "Constraint 'c'.*non-finite"),
        ('x + d == 1', 'sum(x)', -np.inf, "Constraint 'c'.*non-finite"),
        ('x == 1', 'sum(d * x)', np.inf, 'objective.*non-finite'),
    ],
)
def test_a_non_finite_coefficient_in_a_kept_row_or_the_objective_is_refused(constraint, objective, d, refused):
    spec = {
        'dimensions': {'g': {}},
        'parameters': {'d': {'dims': ['g']}},
        'variables': {'x': {'dims': ['g']}},
        'constraints': {'c': {'dims': ['g'], 'expression': constraint}},
        'objective': {'sense': 'minimize', 'expression': objective},
    }
    g = pd.Index(['a', 'b'], name='g')
    with pytest.raises(ValueError, match=refused):
        build(mathspec.to_spec(spec).program, ModelData({'g': g}, {'d': over([1.0, d], g=g)}))


def test_an_infinite_upper_bound_leaves_the_variable_open():
    spec = {
        'dimensions': {'t': {}},
        'parameters': {'cap': {'dims': ['t']}},
        'variables': {'x': {'dims': ['t'], 'bounds': {'lower': 0, 'upper': 'cap'}}},
        'constraints': {'need': {'dims': ['t'], 'expression': 'x >= 3'}},
        'objective': {'sense': 'minimize', 'expression': 'sum(x)'},
    }
    t = pd.Index(['a', 'b'], name='t')
    model = solve(spec, ModelData({'t': t}, {'cap': over([np.inf, 5.0], t=t)}))
    np.testing.assert_allclose(model.variables['x'].solution, [3, 3])


@pytest.mark.parametrize('where', ['p > 0', 'p * 2 > 0'])
def test_an_infinite_parameter_in_a_where_is_a_number(where):
    spec = {
        'dimensions': {'t': {}},
        'parameters': {'p': {'dims': ['t']}},
        'variables': {'x': {'dims': ['t'], 'bounds': {'lower': 0}}},
        'constraints': {'need': {'dims': ['t'], 'expression': 'x >= 1', 'where': where}},
        'objective': {'sense': 'minimize', 'expression': 'sum(x)'},
    }
    t = pd.Index(['a', 'b'], name='t')
    model = solve(spec, ModelData({'t': t}, {'p': over([np.inf, 1.0], t=t)}))
    np.testing.assert_allclose(model.variables['x'].solution, [1, 1])


def test_a_nan_parameter_is_refused_when_attached():
    t = pd.Index(['a', 'b'], name='t')
    with pytest.raises(ValueError, match=r"parameter 'p' holds NaN.*\['a'\]"):
        ModelData({'t': t}, {'p': over([np.nan, 1.0], t=t)})
