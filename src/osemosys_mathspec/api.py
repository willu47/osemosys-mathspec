"""Read OSeMOSYS data with otoole, build the spec's model with linopy, solve it, and write the results with otoole."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any

import linopy
import mathspec
import otoole
import pandas as pd

# otoole reads and validates a user config only inside convert; its reader is the one to agree with.
from otoole.convert import _get_user_config

from osemosys_mathspec.bridge.inputs import from_otoole
from osemosys_mathspec.bridge.results import to_otoole
from osemosys_mathspec.engine.build import build
from osemosys_mathspec.engine.evaluate import ModelData

LOGGER = logging.getLogger(__name__)

#: The formulation, shipped with the package as one fragment per block.
SPEC_PATH = Path(str(resources.files('osemosys_mathspec') / 'spec'))


def load_spec(path: str | Path = SPEC_PATH) -> mathspec.Spec:
    """A mathspec file, or a folder of fragments merged in file order under the first fragment's description."""
    if not Path(path).is_dir():
        return mathspec.to_spec(path)
    fragments = sorted(Path(path).glob('*.yaml'))
    if not fragments:
        raise ValueError(f'no *.yaml fragments in {path}')
    return mathspec.merge(fragments, description=mathspec.to_spec(fragments[0]).description)


@dataclass
class Run:
    """What one run produced."""

    model: linopy.Model
    data: ModelData
    status: str
    termination: str
    objective: float | None
    results: dict[str, pd.DataFrame]
    result_defaults: dict[str, Any]


def run(
    config: str | Path,
    from_format: str,
    from_path: str | Path,
    *,
    to_format: str | None = None,
    to_path: str | Path | None = None,
    solver: str = 'highs',
    spec: mathspec.Spec | None = None,
    **solver_options: Any,
) -> Run:
    """Solve the OSeMOSYS model for one dataset.

    Args:
        config: The otoole user configuration for the dataset.
        from_format: Any format ``otoole.read`` takes: ``csv``, ``excel`` or ``datafile``.
        from_path: The dataset, as ``otoole.read`` takes it.
        to_format: Any format ``otoole.write`` takes; results are written only with ``to_path``.
        to_path: Where the results go.
        solver: Any solver linopy drives.
        spec: The formulation; the packaged fragments in ``spec/``, merged, when omitted.
        solver_options: Passed to the solver through linopy.
    """
    spec = spec or load_spec()
    program = spec.program
    inputs, defaults = otoole.read(str(config), from_format, str(from_path))
    data = from_otoole(inputs, defaults, program)
    model = build(program, data)
    status, termination = model.solve(solver_name=solver, **solver_options)

    results: dict[str, pd.DataFrame] = {}
    result_defaults: dict[str, Any] = {}
    objective = None
    if status == 'ok':
        objective = float(model.objective.value)
        user_config = _get_user_config(str(config))
        results, result_defaults = to_otoole(model, program, user_config, inputs)
        if to_path is not None:
            otoole.write(str(config), to_format or from_format, str(to_path), results, result_defaults)
    else:
        LOGGER.warning('solve ended %s (%s); no results written', status, termination)
    return Run(model, data, status, termination, objective, results, result_defaults)
