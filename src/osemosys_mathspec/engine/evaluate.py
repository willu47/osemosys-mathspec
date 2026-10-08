"""Evaluate a mathspec program's expressions and masks against attached data.

The evaluator is generic: it knows mathspec's node types, not OSeMOSYS. It
covers the operators the OSeMOSYS spec uses, and refuses the others by name
with ``NotImplementedError``, so a spec that grows a new construct fails
loudly instead of building something wrong.
"""

from __future__ import annotations

import operator
from dataclasses import dataclass, field
from typing import assert_never

import linopy
import numpy as np
import pandas as pd
import xarray as xr
from mathspec import program as ms

from osemosys_mathspec.engine import terms
from osemosys_mathspec.engine.check import failing_at
from osemosys_mathspec.engine.terms import FALSE, TRUE, Term

COMPARE = {
    '<': operator.lt,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '>=': operator.ge,
}


@dataclass
class ModelData:
    """The data a program is evaluated against, in the program's own names.

    ``coords`` holds one ordered index per dimension, and that order is the one
    ``shift``, ``sum_back`` and ``position()`` count in. ``parameters`` holds
    one dense DataArray per parameter over exactly its declared dims, and
    refuses NaN in it: ``±inf`` is a value, NaN is not.
    ``relations`` holds one table per relation, with one column per role.
    """

    coords: dict[str, pd.Index]
    parameters: dict[str, xr.DataArray]
    relations: dict[str, pd.DataFrame] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name, array in self.parameters.items():
            nan = array.isnull()
            if nan.any():
                raise ValueError(f"parameter '{name}' holds NaN, which is not a value, e.g. at {failing_at(nan)}")


class Evaluator:
    """Evaluates expression and predicate nodes of one program, against one ModelData and one linopy model."""

    def __init__(self, program: ms.Program, data: ModelData, variables: dict[str, linopy.Variable] | None = None):
        self.program = program
        self.data = data
        self.variables = variables if variables is not None else {}
        self.variable_masks: dict[str, xr.DataArray] = {}
        self._named: dict[str, Term] = {}

    # ------------------------------------------------------------------ expressions

    def expression(self, node: ms.Expression) -> Term:
        match node:
            case ms.Constant(value):
                return Term.constant(value)
            case ms.Parameter(name):
                return Term.data(self.data.parameters[name].astype(float))
            case ms.Variable(name):
                return self._variable(name)
            case ms.Named(name, body):
                if name not in self._named:
                    self._named[name] = self.expression(body)
                return self._named[name]
            case ms.Negate(operand):
                return terms.negate(self.expression(operand))
            case ms.Add(left, right):
                return terms.add(self.expression(left), self.expression(right))
            case ms.Multiply(left, right):
                return terms.multiply(self.expression(left), self.expression(right))
            case ms.Divide(numerator, divisor):
                return terms.divide(self.expression(numerator), self.expression(divisor))
            case ms.Power(base, exponent):
                return terms.power(self.expression(base), self.expression(exponent))
            case ms.Sum(operand, over):
                return self._sum(self.expression(operand), over)
            case ms.Translate():
                return self._translate(node)
            case ms.WindowSum():
                return self._window_sum(node)
            case ms.Pullback(operand, direction):
                return self._pullback(self.expression(operand), direction)
            case ms.Cases(regions):
                return self._cases(regions)
            case ms.GroupSum() | ms.Dual():
                raise NotImplementedError(f'{type(node).__name__} is not supported by this engine yet')
            case _:
                assert_never(node)

    def _variable(self, name: str) -> Term:
        declaration = self.program.variables[name]
        mask = self.variable_masks.get(name, TRUE)
        present = TRUE if declaration.absence == 'zero' else mask
        return Term(self.variables[name], present)

    def _sum(self, term: Term, over: tuple[str, ...]) -> Term:
        # An absent summand is one fewer; the row stands. An invalid one poisons the sum.
        value = term.zeroed()
        invalid = term.invalid
        for dim in over:
            value = value.sum(dim)
            if dim in invalid.dims:
                invalid = invalid.any(dim)
        if isinstance(value, xr.DataArray):
            return Term.data(value, TRUE, invalid)
        return Term(value, TRUE, invalid)

    def _shift(self, term: Term, along: str, offset: int) -> Term:
        """``term`` read ``offset`` positions back along ``along``; the vacated edge is absent."""
        coords = self.data.coords[along]
        if isinstance(term.value, xr.DataArray):
            shifted: terms.Value = _broadcast_to(term.value, along, coords).shift({along: offset}, fill_value=0.0)
        else:
            shifted = terms.as_expression(term.value).shift({along: offset}).fillna(0)
        present = _shift_mask(term.present, along, offset, coords)
        invalid = _shift_mask(term.invalid, along, offset, coords)
        return Term(shifted, present, invalid)

    def _translate(self, node: ms.Translate) -> Term:
        if node.partition is not None or node.wrap or isinstance(node.offset, str):
            raise NotImplementedError("shift with by=, edge='wrap' or a named offset is not supported yet")
        shifted = self._shift(self.expression(node.operand), node.along, node.offset)
        if node.fill is None:
            return shifted
        # edge=<number>: the vacated positions are present and contribute the number.
        vacated = ~_edge_present(self.data.coords[node.along], node.along, node.offset)
        value = terms.add(Term(shifted.zeroed()), Term(xr.DataArray(node.fill) * vacated)).value
        return Term(value, shifted.present | vacated, shifted.invalid)

    def _window_sum(self, node: ms.WindowSum) -> Term:
        """Σ over the trailing window, built as a sum of shifts ``k < width`` for k = 0 … max(width) - 1."""
        if node.partition is not None or node.wrap:
            raise NotImplementedError("sum_back with by= or edge='wrap' is not supported yet")
        operand = self.expression(node.operand)
        coords = self.data.coords[node.along]
        if isinstance(node.width, str):
            width = self.data.parameters[node.width]
            reach = int(min(len(coords), max(int(width.max()), 0)))
        else:
            width = xr.DataArray(node.width)
            reach = min(len(coords), node.width)
        total: Term | None = None
        for k in range(reach):
            summand = self._shift(operand, node.along, k)
            inside = xr.DataArray(k) < width
            part = Term(summand.value, summand.present & inside, summand.invalid & inside)
            reduced = Term(part.zeroed(), TRUE, part.invalid)
            total = reduced if total is None else terms.add(total, reduced)
        if total is None:  # a window of 0 everywhere is an empty sum
            return Term.constant(0.0)
        return total

    def _pullback(self, term: Term, direction: ms.Direction) -> Term:
        """``at``: read the operand at the coordinates the relation's consumed columns hold, landing on its key.

        The read indexes into temporary dimension names and renames them after,
        because xarray's vectorised indexing mis-reads an indexer that reuses
        the name of a dimension it indexes (which a transpose such as
        TradeReverse does).
        """
        if direction.joined:
            raise NotImplementedError('at() joining on other key columns is not supported yet')
        table = self.data.relations[direction.name]
        produced = direction.produced_dims
        consumed = direction.consumed_dims
        tmp = {d: f'__at_{d}' for d in produced}
        index = pd.MultiIndex.from_product([self.data.coords[d] for d in produced], names=produced)
        rows = table.set_index(list(direction.produced)).reindex(index)
        exists = rows.notna().all(axis=1)

        def unstacked(values: np.ndarray) -> xr.DataArray:
            flat = xr.DataArray(values, dims=['__row'], coords={'__row': index})
            return flat.unstack('__row').transpose(*produced)

        indexers = {}
        for role, dim in zip(direction.consumed, consumed, strict=True):
            labels = rows[role].where(exists, self.data.coords[dim][0])
            indexers[dim] = unstacked(self.data.coords[dim].get_indexer(labels)).rename(tmp)
        back = {v: k for k, v in tmp.items()}

        def read(array: terms.Value) -> terms.Value:
            if isinstance(array, xr.DataArray):
                for dim in consumed:
                    array = _broadcast_to(array, dim, self.data.coords[dim])
            read_at = array.isel(indexers)
            # The consumed labels survive the read as coordinates over the new dims; the key's labels replace them.
            stale = [d for d in consumed if d in read_at.coords]
            return read_at.drop_vars(stale).rename(back)

        value = read(terms.as_expression(term.value) if terms.is_linear(term.value) else term.value)
        present = read(term.present) & unstacked(exists.to_numpy())
        return Term(value, present, read(term.invalid))

    def _cases(self, regions: tuple[ms.Region, ...]) -> Term:
        """Exactly one region applies at each coordinate, so the regions are added, each zero outside its own."""
        total: Term | None = None
        present = FALSE
        invalid = FALSE
        for region in regions:
            when = self.mask(region.when)
            value = self.expression(region.value)
            own = Term(value.value, value.present & when, value.invalid & when)
            present = present | (when & value.present)
            invalid = invalid | own.invalid
            part = Term(own.zeroed(), TRUE)
            total = part if total is None else terms.add(total, part)
        assert total is not None
        return Term(total.value, present, invalid)

    # ------------------------------------------------------------------ masks

    def mask(self, mask: ms.Mask | None) -> xr.DataArray:
        return TRUE if mask is None else self.predicate(mask.root)

    def predicate(self, node: ms.Predicate) -> xr.DataArray:
        match node:
            case ms.BooleanLiteral(value):
                return xr.DataArray(value)
            case ms.Not(operand):
                return ~self.predicate(operand)
            case ms.And(left, right):
                return self.predicate(left) & self.predicate(right)
            case ms.Or(left, right):
                return self.predicate(left) | self.predicate(right)
            case ms.ParameterDefined(name):
                return xr.DataArray(True)  # parameters arrive dense: every row is defined
            case ms.ParameterComparison(name, op, value):
                return COMPARE[op](self.data.parameters[name], value)
            case ms.VariableDefined(name):
                return self.variable_masks.get(name, TRUE)
            case ms.ExpressionComparison(left, op, right):
                a, b = self.expression(left), self.expression(right)
                ok = a.present & b.present & ~a.invalid & ~b.invalid
                return COMPARE[op](a.value, b.value) & ok
            case ms.DimensionComparison(name, op, value):
                return COMPARE[op](_labels(self.data.coords[name], name), value)
            case ms.DimensionPosition(name, op, position, partition):
                if partition is not None:
                    raise NotImplementedError('position(by=) is not supported yet')
                coords = self.data.coords[name]
                target = position if position >= 0 else len(coords) + position
                return COMPARE[op](_position(coords, name), target)
            case ms.TranslatedPredicate(operand, along, offset):
                inner = self.predicate(operand.root)
                return _shift_mask(inner, along, offset, self.data.coords[along])
            case (
                ms.RelationComparison()
                | ms.RelationPairComparison()
                | ms.RelationDefined()
                | ms.CountComparison()
                | ms.PulledBackPredicate()
            ):
                raise NotImplementedError(f'{type(node).__name__} in a where is not supported yet')
            case _:
                assert_never(node)


# ---------------------------------------------------------------------- helpers


def _labels(coords: pd.Index, dim: str) -> xr.DataArray:
    return xr.DataArray(coords.to_numpy(), dims=[dim], coords={dim: coords})


def _position(coords: pd.Index, dim: str) -> xr.DataArray:
    return xr.DataArray(np.arange(len(coords)), dims=[dim], coords={dim: coords})


def _broadcast_to(array: xr.DataArray, dim: str, coords: pd.Index) -> xr.DataArray:
    if dim in array.dims:
        return array
    return array.expand_dims({dim: coords})


def _shift_mask(mask: xr.DataArray, along: str, offset: int, coords: pd.Index) -> xr.DataArray:
    """A boolean mask read ``offset`` positions back; false where the translation vacates."""
    mask = _broadcast_to(mask, along, coords)
    return mask.shift({along: offset}, fill_value=False).astype(bool)


def _edge_present(coords: pd.Index, dim: str, offset: int) -> xr.DataArray:
    position = _position(coords, dim)
    return (position >= offset) if offset >= 0 else (position < len(coords) + offset)

