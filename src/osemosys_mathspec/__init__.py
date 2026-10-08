"""OSeMOSYS: the formulation in a mathspec file, built with linopy, fed and read out by otoole."""

from osemosys_mathspec.api import SPEC_PATH, Run, load_spec, run

__all__ = ['SPEC_PATH', 'Run', 'load_spec', 'run']
