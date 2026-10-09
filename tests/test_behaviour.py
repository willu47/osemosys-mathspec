"""OSeMOSYS behaviour on models small enough to work out by hand, stated in Gherkin in `features/`.

A scenario names its sets and its parameter rows, as otoole would read them, and every row it leaves out is the
parameter's otoole default. A `*` in a table stands for every label of that column's set when the model is solved,
and a later row overrides an earlier one.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import cache
from itertools import product
from pathlib import Path

import linopy
import mathspec
import pandas as pd
import pytest
import yaml
from mathspec import program as ms
from pytest_bdd import given, parsers, scenarios, then, when

from osemosys_mathspec import SPEC_PATH
from osemosys_mathspec.bridge.inputs import SET_ALIASES, from_otoole
from osemosys_mathspec.engine.build import build

scenarios('features')

CONFIG = Path(__file__).parent / 'fixtures' / 'simplicity' / 'config.yaml'
DEFAULTS = {name: entry['default'] for name, entry in yaml.safe_load(CONFIG.read_text()).items() if entry['type'] == 'param'}
UNNAMED_SETS = {
    'MODE_OF_OPERATION': [1],
    'SEASON': [1],
    'DAYTYPE': [1],
    'DAILYTIMEBRACKET': [1],
    'EMISSION': ['CO2'],
    'STORAGE': ['DAM'],
}


@cache
def merged(fragments: tuple[Path, ...]) -> ms.Program:
    return mathspec.merge(list(fragments)).program


@dataclass
class Scenario:
    fragments: list[Path] = field(default_factory=lambda: sorted(SPEC_PATH.glob('*.yaml')))
    sets: dict[str, list] = field(default_factory=lambda: dict(UNNAMED_SETS))
    tables: dict[str, list[list[str]]] = field(default_factory=dict)
    model: linopy.Model = field(init=False)
    refusal: ValueError | None = None

    @property
    def program(self) -> ms.Program:
        return merged(tuple(self.fragments))

    def label(self, dim: str, text: str) -> int | str:
        return int(text) if self.program.dimensions[dim].dtype == 'int' else text

    def rows(self, dims: tuple[str, ...], datatable: list[list[str]]) -> pd.DataFrame:
        header, *body = datatable
        assert sorted(header) == sorted([*dims, 'VALUE']), f'columns {header} are not {[*dims, "VALUE"]}'
        records = []
        for cells in (dict(zip(header, row, strict=True)) for row in body):
            labels = [
                self.sets[SET_ALIASES.get(dim, dim)] if cells[dim] == '*' else [self.label(dim, cells[dim])]
                for dim in dims
            ]
            records += [(*key, float(cells['VALUE'])) for key in product(*labels)]
        return pd.DataFrame(records, columns=[*dims, 'VALUE']).drop_duplicates(list(dims), keep='last')

    @property
    def parameters(self) -> dict[str, pd.DataFrame]:
        dims = {name: self.program.parameters[name].dims for name in self.tables}
        return {name: self.rows(dims[name], table).set_index(list(dims[name])) for name, table in self.tables.items()}

    def solve(self) -> None:
        inputs = {name: pd.DataFrame({'VALUE': labels}) for name, labels in self.sets.items()} | self.parameters
        try:
            model = build(self.program, from_otoole(inputs, DEFAULTS, self.program))
        except ValueError as refusal:
            self.refusal = refusal
            return
        model.solve(solver_name='highs', output_flag=False)
        self.model = model

    def built(self) -> linopy.Model:
        if self.refusal is not None:
            raise self.refusal
        return self.model

    def solved(self) -> linopy.Model:
        model = self.built()
        assert (model.status, model.termination_condition) == ('ok', 'optimal'), model.termination_condition
        return model


@pytest.fixture
def scenario() -> Scenario:
    return Scenario()


@given(parsers.parse('the set {name} holds {labels}'))
def set_holds(scenario: Scenario, name: str, labels: str) -> None:
    scenario.sets[name] = [scenario.label(name, label) for label in labels.split(', ')]


@given(parsers.re(r'(?P<name>[A-Z]\w+) is'))
def parameter_is(scenario: Scenario, name: str, datatable: list[list[str]]) -> None:
    scenario.tables[name] = datatable


@given(parsers.parse('the model leaves out the {block} block'))
def leaves_out(scenario: Scenario, block: str) -> None:
    kept = [path for path in scenario.fragments if path.stem.split('_', 1)[1] != block.replace(' ', '_')]
    assert len(kept) == len(scenario.fragments) - 1, f'no {block} block among {scenario.fragments}'
    scenario.fragments = kept


@when('the model is solved')
def model_is_solved(scenario: Scenario) -> None:
    scenario.solve()


@then(parsers.parse('the objective is {value:g}'))
def objective_is(scenario: Scenario, value: float) -> None:
    assert scenario.solved().objective.value == pytest.approx(value, rel=1e-6)


@then(parsers.re(r'(?P<name>[A-Z]\w+) is'))
def variable_is(scenario: Scenario, name: str, datatable: list[list[str]]) -> None:
    solution = scenario.solved().variables[name].solution
    for *key, value in scenario.rows(solution.dims, datatable).itertuples(index=False):
        at = dict(zip(solution.dims, key, strict=True))
        assert float(solution.sel(at)) == pytest.approx(value, rel=1e-6, abs=1e-6), f'{name} at {at}'


@then('the model is infeasible')
def model_is_infeasible(scenario: Scenario) -> None:
    assert scenario.built().termination_condition in {'infeasible', 'infeasible_or_unbounded'}


@then(parsers.parse('the data is refused for "{reason}"'))
def data_is_refused(scenario: Scenario, reason: str) -> None:
    assert scenario.refusal is not None and re.search(reason, str(scenario.refusal)), scenario.refusal
