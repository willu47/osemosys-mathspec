"""``osemosys run`` — otoole's formats in and out, the spec's model solved in between."""

from __future__ import annotations

import argparse
import logging
import sys

from osemosys_mathspec.api import SPEC_PATH, load_spec, run

FORMATS = ('csv', 'excel', 'datafile')


def parser() -> argparse.ArgumentParser:
    front = argparse.ArgumentParser(prog='osemosys')
    verbs = front.add_subparsers(dest='verb', required=True)
    solve = verbs.add_parser('run', help='solve one dataset and write its results')
    solve.add_argument('from_format', choices=FORMATS, help='format of the input data')
    solve.add_argument('from_path', help='input data: a folder of CSVs, an Excel file or a datafile')
    solve.add_argument('config', help='otoole user configuration (YAML)')
    solve.add_argument('--to-format', choices=('csv', 'excel'), default='csv', help='format of the results')
    solve.add_argument('--to-path', help='where to write the results; nothing is written without it')
    solve.add_argument('--solver', default='highs', help='any solver linopy drives (default: highs)')
    solve.add_argument(
        '--spec',
        default=str(SPEC_PATH),
        help='a mathspec file, or a folder of fragments to merge (default: the packaged one)',
    )
    return front


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(name)s: %(message)s')
    # otoole reports every deprecated config field at INFO; only its warnings belong on a run's output.
    logging.getLogger('otoole').setLevel(logging.WARNING)
    result = run(
        args.config,
        args.from_format,
        args.from_path,
        to_format=args.to_format,
        to_path=args.to_path,
        solver=args.solver,
        spec=load_spec(args.spec),
        progress=False,
    )
    if result.objective is None:
        sys.stderr.write(f'solve ended {result.status} ({result.termination})\n')
        return 1
    sys.stdout.write(f'{result.termination}: objective {result.objective:.10g}\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
