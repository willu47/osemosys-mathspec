"""The parameters and relations the spec marks as *data prep*: what the spec cannot state, derived from what otoole reads.

Each function reads the ordered coordinates, and any dense array the bridge
has already built, in the spec's dimension names.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import xarray as xr

#: Dimensions the spec steps along by position (`y-1`, `ls-1`, `ld-1`), so a
#: gap in their integer labels would change the model.
CONSECUTIVE = ('YEAR', 'SEASON', 'DAYTYPE')


def check_consecutive(coords: dict[str, pd.Index]) -> None:
    """Refuse integer labels with a gap along a dimension the spec shifts along.

    MathProg's ``y-1`` reads the year before by value, and the spec's ``shift``
    reads it by position. The two agree only when the labels are consecutive.
    """
    for dim in CONSECUTIVE:
        labels = coords[dim].to_numpy()
        if len(labels) > 1 and not np.all(np.diff(labels) == 1):
            raise ValueError(
                f'{dim} must be consecutive integers, since the spec reads the previous {dim.lower()} '
                f'by position; got {labels.tolist()}'
            )


def years_since_start(coords: dict[str, pd.Index]) -> xr.DataArray:
    """``y - min(YEAR)``."""
    years = _years(coords)
    return years - years.min()


def years_until_end(coords: dict[str, pd.Index]) -> xr.DataArray:
    """``max(YEAR) - y + 1``."""
    years = _years(coords)
    return years.max() - years + 1


def daily_time_bracket_count(coords: dict[str, pd.Index]) -> xr.DataArray:
    return xr.DataArray(len(coords['DAILYTIMEBRACKET']))


def discount_rate_idv(coords: dict[str, pd.Index], rate: xr.DataArray) -> xr.DataArray:
    """``DiscountRate`` for every technology: OSeMOSYS's default where otoole supplies no ``DiscountRateIdv``."""
    return rate.expand_dims(TECHNOLOGY=coords['TECHNOLOGY'], axis=1)


def trade_reverse(coords: dict[str, pd.Index]) -> pd.DataFrame:
    """One row ``(r, rr, rr, r)`` per pair of regions: each route read from its far end."""
    pairs = pd.MultiIndex.from_product([coords['REGION'], coords['_REGION']], names=['REGION', '_REGION'])
    table = pairs.to_frame(index=False)
    table['reverse_region'] = table['_REGION']
    table['reverse_partner'] = table['REGION']
    return table


def _years(coords: dict[str, pd.Index]) -> xr.DataArray:
    years = coords['YEAR']
    return xr.DataArray(years.to_numpy(), dims=['YEAR'], coords={'YEAR': years})
