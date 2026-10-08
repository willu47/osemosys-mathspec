"""The value an expression node evaluates to, and the arithmetic between them.

mathspec defines *absence* (a masked variable, a vacated shift edge, a
coordinate a relation does not map) separately from zero: absence spreads
through arithmetic and removes the row, while a summing operator skips an
absent summand. linopy has no such notion, since a masked variable simply
contributes nothing. So every value carries its own ``present`` mask, and a
summing operator zeroes the absent summands before it reduces.

``invalid`` marks coordinates where parameter arithmetic produced NaN, such
as 0/0, or where a non-finite number meets a variable as a coefficient or
constant. The value there is set to 0 so that linopy never sees it. A kept
constraint row or an objective that touches an invalid coordinate is refused.
Elsewhere ``±inf`` is a value: a bound or a comparison reads it as it is.
"""

from __future__ import annotations

import operator
from dataclasses import dataclass, field
from typing import Callable

import linopy
import numpy as np
import xarray as xr
from linopy.constants import TERM_DIM

Value = xr.DataArray | linopy.Variable | linopy.LinearExpression

TRUE = xr.DataArray(True)
FALSE = xr.DataArray(False)


def is_linear(value: Value) -> bool:
    return isinstance(value, (linopy.Variable, linopy.LinearExpression))


def as_expression(value: Value) -> linopy.LinearExpression:
    if isinstance(value, linopy.Variable):
        return 1 * value
    assert isinstance(value, linopy.LinearExpression)
    return value


def dims_of(value: Value) -> tuple[str, ...]:
    if isinstance(value, linopy.LinearExpression):
        return tuple(d for d in value.dims if d != TERM_DIM)
    return tuple(value.dims)


@dataclass(frozen=True)
class Term:
    """An evaluated expression: its value, where it exists, and where it is invalid."""

    value: Value
    present: xr.DataArray = field(default_factory=lambda: TRUE)
    invalid: xr.DataArray = field(default_factory=lambda: FALSE)

    @classmethod
    def constant(cls, number: float) -> Term:
        return cls(xr.DataArray(float(number)))

    @classmethod
    def data(cls, array: xr.DataArray, present: xr.DataArray = TRUE, invalid: xr.DataArray = FALSE) -> Term:  # noqa: B008
        """A parameter-only value, with any NaN entry recorded as invalid and zeroed; ``±inf`` stays a value."""
        nan = array.isnull()
        return cls(array.where(~nan, 0.0), present, invalid | nan)

    @property
    def dims(self) -> tuple[str, ...]:
        return dims_of(self.value)

    def zeroed(self) -> Value:
        """The value with every absent or invalid coordinate contributing nothing — what a summing operator reads."""
        keep = self.present & ~self.invalid
        if isinstance(self.value, xr.DataArray):
            return self.value.where(keep, 0.0)
        return as_expression(self.value).where(keep).fillna(0)


def combine(left: Term, right: Term, op: Callable[[Value, Value], Value]) -> Term:
    """An element-wise operation: absence and invalidity spread from either side."""
    present = left.present & right.present
    if not is_linear(left.value) and not is_linear(right.value):
        with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
            return Term.data(op(left.value, right.value), present, left.invalid | right.invalid)
    left, right = _coefficient(left), _coefficient(right)
    return Term(op(left.value, right.value), present, left.invalid | right.invalid)


def add(left: Term, right: Term) -> Term:
    return combine(left, right, _add)


def multiply(left: Term, right: Term) -> Term:
    return combine(left, right, _multiply)


def divide(left: Term, right: Term) -> Term:
    if is_linear(right.value):
        raise ValueError('a divisor carries a variable, which mathspec already refuses')
    if is_linear(left.value):
        with np.errstate(divide='ignore'):
            return multiply(left, Term(1 / right.value, right.present, right.invalid))
    return combine(left, right, operator.truediv)


def power(base: Term, exponent: Term) -> Term:
    if is_linear(base.value) or is_linear(exponent.value):
        raise ValueError('a power carries a variable, which mathspec already refuses')
    return combine(base, exponent, operator.pow)


def negate(term: Term) -> Term:
    return Term(-term.value, term.present, term.invalid)


def _coefficient(term: Term) -> Term:
    """A parameter value as a variable reads it: any non-finite entry recorded as invalid and zeroed."""
    if is_linear(term.value):
        return term
    finite = xr.apply_ufunc(np.isfinite, term.value)
    return Term(term.value.where(finite, 0.0), term.present, term.invalid | ~finite)


def _add(a: Value, b: Value) -> Value:
    # linopy implements arithmetic with a DataArray on the linopy side only.
    if isinstance(a, xr.DataArray) and is_linear(b):
        return b + a
    return a + b


def _multiply(a: Value, b: Value) -> Value:
    if isinstance(a, xr.DataArray) and is_linear(b):
        return b * a
    return a * b
