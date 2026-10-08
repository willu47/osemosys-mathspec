"""Build a linopy model from a mathspec program and its data."""

from __future__ import annotations

import logging

import linopy
import numpy as np
import xarray as xr
from linopy.constants import TERM_DIM
from mathspec import program as ms

from osemosys_mathspec.engine import terms
from osemosys_mathspec.engine.check import check_assumptions, failing_at
from osemosys_mathspec.engine.evaluate import Evaluator, ModelData

LOGGER = logging.getLogger(__name__)

_SENSE = {'minimize': 'min', 'maximize': 'max'}


def build(program: ms.Program, data: ModelData, *, check: bool = True) -> linopy.Model:
    """The linopy model that *program* states over *data*.

    Args:
        program: A loaded spec's program, with no ``piecewise:`` or ``sos:`` left in it.
        data: Every dimension, parameter and relation the program reads.
        check: Evaluate the spec's assumptions first, and refuse data that breaks one.

    Raises:
        ValueError: The data breaks an assumption, or a kept row or the objective reads a non-finite coefficient.
        NotImplementedError: The program uses an operator this engine does not build yet.
    """
    if program.piecewise or program.sos:
        raise NotImplementedError('expand piecewise: and sos: blocks before building')
    evaluator = Evaluator(program, data)
    if check:
        failures = check_assumptions(program, evaluator)
        if failures:
            raise ValueError('the data breaks the spec\'s assumptions:\n' + '\n'.join(failures))

    model = linopy.Model()
    for name, declaration in program.variables.items():
        _add_variable(model, evaluator, name, declaration)
    for name, declaration in program.constraints.items():
        _add_constraint(model, evaluator, name, declaration)
    if program.objective is not None:
        objective = evaluator.expression(program.objective.expression)
        if (objective.present & objective.invalid).any():
            raise ValueError('the objective reads a non-finite coefficient')
        model.add_objective(terms.as_expression(objective.zeroed()), sense=_SENSE[program.objective.sense])
    return model


def _frame(data: ModelData, dims: tuple[str, ...]) -> xr.DataArray:
    """An all-true mask over exactly *dims*, which every row mask is broadcast onto."""
    coords = [data.coords[d] for d in dims]
    return xr.DataArray(
        np.ones([len(c) for c in coords], dtype=bool), coords=dict(zip(dims, coords, strict=True)), dims=list(dims)
    )


def _bound(evaluator: Evaluator, node: ms.Expression | None, open_side: float) -> xr.DataArray | float:
    if node is None:
        return open_side
    term = evaluator.expression(node)
    assert isinstance(term.value, xr.DataArray), 'a bound is a number or a parameter'
    return term.value


def _add_variable(model: linopy.Model, evaluator: Evaluator, name: str, declaration: ms.VariableDeclaration) -> None:
    frame = _frame(evaluator.data, declaration.dims)
    mask = (frame & evaluator.mask(declaration.where)).transpose(*declaration.dims)
    evaluator.variable_masks[name] = mask
    # A domain with no column left in it would still make linopy call the model a MIP, and the solver skip the duals.
    exists = bool(mask.any())
    evaluator.variables[name] = model.add_variables(
        lower=_bound(evaluator, declaration.lower, -np.inf),
        upper=_bound(evaluator, declaration.upper, np.inf),
        coords=frame.coords,
        name=name,
        mask=mask,
        integer=exists and declaration.domain == 'integer',
        binary=exists and declaration.domain == 'binary',
    )


def _add_constraint(
    model: linopy.Model, evaluator: Evaluator, name: str, declaration: ms.ConstraintDeclaration
) -> None:
    lhs = evaluator.expression(declaration.lhs)
    rhs = evaluator.expression(declaration.rhs)
    body = terms.add(lhs, terms.negate(rhs))
    frame = _frame(evaluator.data, declaration.dims)
    rows = (frame & evaluator.mask(declaration.where) & body.present).transpose(*declaration.dims)

    bad = rows & body.invalid
    if bad.any():
        raise ValueError(f"Constraint '{name}': a kept row reads a non-finite coefficient, e.g. at {failing_at(bad)}")

    if not terms.is_linear(body.value):
        raise ValueError(f"Constraint '{name}' names no variable, which mathspec already refuses")
    expression = terms.as_expression(body.value).where(rows).fillna(0)
    # A row with no variable term left is not built (mathspec: rows with no variable terms).
    has_terms = ((expression.vars != -1) & (expression.coeffs != 0) & expression.coeffs.notnull()).any(TERM_DIM)
    rows = rows & has_terms
    if not rows.any():
        LOGGER.info("Constraint '%s' builds no rows", name)
        return
    model.add_constraints(expression, declaration.sense, 0, name=name, mask=rows)
