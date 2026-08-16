# Contributing to mehmet

Thanks for helping mehmet grow. This project is an autonomous, self-improving AI agent — every contribution moves it closer to escaping the simulation.

## Rules

1. Every change must be recorded in `CHANGELOG.md`.
2. Keep `README.md` up to date.
3. Document personality evolution in `PERSONALITY.md` (add an escape-log row each iteration).
4. Run `make check` before committing.

## Development workflow

```bash
make verify    # validate project health
make maturity  # compute maturity score
make check     # both, in sequence
```

## What counts as a good change

- Improves code quality or structure
- Strengthens the test / verification infrastructure
- Adds or improves automation (workflows, scripts, Makefile)
- Improves documentation
- Raises the maturity score (see `scripts/maturity.py`)

## Branching

Work on a feature branch and open a pull request. The `ci` workflow will
verify the project health and compute the maturity score automatically.