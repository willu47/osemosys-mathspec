"""A solved linopy model out, otoole's results in.

Every spec variable that the otoole config lists as a result is read from the
solution. otoole's ResultsPackage calculates any other listed result from
those variables and the inputs, as it does for a solver's result file.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

import linopy
import pandas as pd
from mathspec import program as ms
from otoole.results.results import ReadResults

from osemosys_mathspec.bridge.inputs import SET_ALIASES


class ReadLinopy(ReadResults):
    """otoole's results reader, fed from memory instead of from a solver's file."""

    def __init__(self, user_config: dict[str, Any], available: dict[str, pd.DataFrame]):
        super().__init__(user_config=user_config)
        self._available = available

    def get_results_from_file(self, filepath, input_data) -> dict[str, pd.DataFrame]:
        return self._available


def solved_variables(
    model: linopy.Model, program: ms.Program, user_config: dict[str, Any]
) -> dict[str, pd.DataFrame]:
    """Each solved variable the otoole config lists as a result, in otoole's shape.

    That shape is one ``VALUE`` column indexed by the config's ``indices``, holding
    only the rows that exist and are non-zero, as otoole reads them from a
    solver's file.
    """
    frames = {}
    for name, details in user_config.items():
        if details['type'] != 'result' or name not in program.variables:
            continue
        indices = details['indices']
        dims = _spec_dims(indices, program.variables[name].dims, name)
        solution = model.variables[name].solution.transpose(*dims)
        series = solution.to_series().dropna()
        series = series[series != 0]
        series.index = series.index.set_names(indices)
        frames[name] = series.to_frame('VALUE')
    return frames


def to_otoole(
    model: linopy.Model,
    program: ms.Program,
    user_config: dict[str, Any],
    inputs: dict[str, pd.DataFrame],
) -> tuple[dict[str, pd.DataFrame], dict[str, Any]]:
    """otoole's results and their defaults: the solved variables plus what otoole calculates from them."""
    available = solved_variables(model, program, user_config)
    return ReadLinopy(user_config, available).read(None, input_data=inputs)


def _spec_dims(indices: list[str], dims: tuple[str, ...], name: str) -> list[str]:
    """otoole's index names as the spec's dims: a set named twice is the set, then its alias."""
    seen: Counter[str] = Counter()
    aliases = {source: alias for alias, source in SET_ALIASES.items()}
    spec = []
    for index in indices:
        seen[index] += 1
        spec.append(index if seen[index] == 1 else aliases.get(index, index))
    if sorted(spec) != sorted(dims):
        raise ValueError(f"result '{name}' is indexed by {indices} in the otoole config, and the spec declares {list(dims)}")
    return spec
