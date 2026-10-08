"""Hold attached data to a spec's ``assumptions:``, which mathspec leaves to the consumer."""

from __future__ import annotations

from typing import TYPE_CHECKING

import xarray as xr
from mathspec.program import assumption_message

if TYPE_CHECKING:
    from mathspec import program as ms

    from osemosys_mathspec.engine.evaluate import Evaluator

#: How many failing coordinates a refusal lists before it stops.
SHOWN = 5


def check_assumptions(program: ms.Program, evaluator: Evaluator) -> list[str]:
    """One message per assumption the data breaks, naming the first coordinates it fails at."""
    failures = []
    for name, assumption in program.assumptions.items():
        holds = evaluator.predicate(assumption.predicate.root)
        applies = evaluator.mask(assumption.where)
        broken = applies & ~holds
        if not broken.any():
            continue
        message = assumption_message(name, assumption)
        if broken.ndim:
            message += f' (at {failing_at(broken)})'
        failures.append(message)
    return failures


def failing_at(mask: xr.DataArray) -> list:
    """The first ``SHOWN`` coordinates where *mask* holds; none for a scalar."""
    if not mask.ndim:
        return []
    return mask.where(mask, drop=True).to_series().dropna().index[:SHOWN].tolist()
