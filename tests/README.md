# PtAC tests

First, please ensure that you have installed the necessary [dependencies](environment-dev.yml). Then run the scripts in this folder to:

  - format the code
  - lint the code and the docstrings
  - run unit tests

Please refer to the [contributing guidelines](../CONTRIBUTING.md) to read more about the project's standards and code/docstring style.

## Code format

Format the code and sort imports according to the project's style by changing directories to the repository's root and running:

```
./tests/code_format.sh
```

## Lint and test

Lint and test the code and docstrings by changing directories to the repository's root and running:

```
./tests/lint_test.sh
```

## Continuous integration

All PRs trigger continuous integration tests via GitHub Actions. See the [configurations](../.github/workflows/). The following steps are automatically run:

  - build the docs
  - check code formatting
  - docstrings linter
  - code linter
  - unit tests
