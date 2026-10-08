"""otoole's input data in, the engine's ModelData out.

otoole returns sets as one-column frames and parameters as frames indexed by
their index names, with the defaults held apart. mathspec reads a missing
parameter row as 0 in arithmetic and as false in a where comparison, where
OSeMOSYS reads the default. So every parameter is filled densely with its
otoole default, and the spec then sees what GLPK sees.
"""

from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd
import xarray as xr
from mathspec import program as ms

from osemosys_mathspec.bridge import prep
from osemosys_mathspec.engine.evaluate import ModelData

#: A spec dimension read from another otoole set: `_REGION` is REGION seen
#: from the other end of a trade route.
SET_ALIASES = {'_REGION': 'REGION'}

Derived = Callable[[dict[str, pd.Index], dict[str, xr.DataArray]], xr.DataArray]

#: The data-prep parameters, in the order they are derived; each reads what
#: otoole supplied and what is derived before it.
DERIVED: dict[str, Derived] = {
    'YearsSinceStart': lambda c, p: prep.years_since_start(c),
    'YearsUntilEnd': lambda c, p: prep.years_until_end(c),
    'DailyTimeBracketCount': lambda c, p: prep.daily_time_bracket_count(c),
    'DiscountRateIdv': lambda c, p: prep.discount_rate_idv(c, p['DiscountRate']),
}


def from_otoole(
    inputs: dict[str, pd.DataFrame], defaults: dict[str, float], program: ms.Program
) -> ModelData:
    """The engine's data for *program*, from what ``otoole.read`` returned.

    ``DiscountRateIdv`` is read where otoole supplies it, and is DiscountRate
    otherwise, as OSeMOSYS defaults it.

    Raises:
        ValueError: A dimension or parameter the program reads is neither in the
            otoole data nor derivable, a parameter arrives over different
            dimensions with rows in it, or the data breaks a data-prep rule.
    """
    coords = {dim: _coords(inputs, dim, declaration.dtype) for dim, declaration in program.dimensions.items()}
    prep.check_consecutive(coords)

    parameters: dict[str, xr.DataArray] = {}
    for name, declaration in program.parameters.items():
        if name in inputs or name in defaults:
            frame = inputs.get(name, pd.DataFrame(columns=['VALUE']))
            parameters[name] = _dense(name, frame, defaults.get(name, 0), declaration, coords)
    for name, derive in DERIVED.items():
        if name in program.parameters and name not in parameters:
            array = derive(coords, parameters)
            parameters[name] = array.astype(int) if program.parameters[name].dtype == 'int' else array

    missing = sorted(set(program.parameters) - set(parameters))
    if missing:
        raise ValueError(f'no data for parameters {missing}: otoole supplies none of them and none is derived')

    relations = {}
    if 'TradeReverse' in program.relations:
        relations['TradeReverse'] = prep.trade_reverse(coords)
    return ModelData(coords=coords, parameters=parameters, relations=relations)


def _coords(inputs: dict[str, pd.DataFrame], dim: str, dtype: str) -> pd.Index:
    source = SET_ALIASES.get(dim, dim)
    if source not in inputs:
        raise ValueError(f"no otoole set '{source}' for dimension '{dim}'")
    labels = inputs[source]['VALUE']
    if dtype == 'int':
        labels = labels.astype(int).sort_values()
    else:
        labels = labels.astype(str)
    return pd.Index(labels.to_numpy(), name=dim)


def _dense(
    name: str,
    frame: pd.DataFrame,
    default: float,
    declaration: ms.ParameterDeclaration,
    coords: dict[str, pd.Index],
) -> xr.DataArray:
    """One parameter over exactly its declared dims, every missing row its default.

    otoole names a parameter's index columns after sets, so a repeated set (the
    two ends of a route) arrives twice under one name. The columns are matched to
    the spec's dims by position.
    """
    dims = declaration.dims
    frame_coords = [coords[d] for d in dims]
    dtype = int if declaration.dtype == 'int' else float
    if frame.empty:
        shape = [len(c) for c in frame_coords]
        return xr.DataArray(np.full(shape, default, dtype=dtype), coords=dict(zip(dims, frame_coords, strict=True)), dims=list(dims))
    if frame.index.nlevels != len(dims):
        raise ValueError(
            f"parameter '{name}' arrives over {list(frame.index.names)}, and the spec declares it over {list(dims)}"
        )
    series = frame['VALUE'].copy()
    series.index = series.index.set_names(list(dims))
    series.index = pd.MultiIndex.from_arrays(
        [series.index.get_level_values(d).astype(coords[d].dtype) for d in dims], names=list(dims)
    ) if len(dims) > 1 else pd.Index(series.index.astype(coords[dims[0]].dtype), name=dims[0])
    full = pd.MultiIndex.from_product(frame_coords, names=list(dims)) if len(dims) > 1 else frame_coords[0]
    unknown = series.index.difference(full)
    if len(unknown):
        raise ValueError(f"parameter '{name}' has rows at labels no set declares, e.g. {unknown[:3].tolist()}")
    series = series.reindex(full, fill_value=default).astype(dtype)
    array = xr.DataArray.from_series(series) if len(dims) > 1 else xr.DataArray(series)
    return array.reindex({d: coords[d] for d in dims}).transpose(*dims)
