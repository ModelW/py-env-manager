# Contributing

Yay you want to contribute! Here are a few rules.

This repository follows the [WITH Madrid](https://code.with-madrid.com/) code 
guidelines. Specifically, this means that:

- Git is managed using git-flow
- You can format the code in any way you want as long as it matches the output
  of `ruff format` and `ruff check --fix`
- The code must be clean for `ruff check` and `mypy`
- Everything needs to be documented

Let's go about those things.

## Environment

Dependencies are managed with [uv](https://docs.astral.sh/uv/). To install the
development environment, run from the root of the repo:

```
uv sync
```

## Formatting and linting

The code is formatted and linted using `ruff`, and type-checked with `mypy`.
While you can run the tools manually, it's simpler to rely on the Makefile
shortcuts. From the root of the repo you can simply:

```
make format
make lint
```

`make format` runs `ruff` in write mode, while `make lint` checks formatting,
ruff rules and types without modifying anything. `make clean` chains both so
the tree is ready to commit.

## Writing documentation

The documentation is written using Sphinx and auto-built using RTD. You can
have a look in the `doc` folder.

Every new feature should be documented!
