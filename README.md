# Veripy

Github Actions to perform static analysis of Python code


## Getting Started

You can include the action in your workflow to trigger on any event that [GitHub actions supports](https://help.github.com/en/articles/events-that-trigger-workflows). If the remote branch that you wish to deploy to doesn't already exist the action will create it for you. Your workflow will also need to include the `actions/checkout` step before this workflow runs in order for the deployment to work. If you intend to make multiple deployments in quick succession [you may need to levereage the concurrency parameter in your workflow](https://docs.github.com/en/actions/learn-github-actions/workflow-syntax-for-github-actions#concurrency) to prevent overlaps.

You can view an example of this below.

<details><summary><code>Pylint - Code Linting</code></summary>

```yml
  pylint:
    name: Pylint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@master
      - name: check
        uses: nsavelyeva/veripy@master
        with:
          scan: lint
          token: ${{ secrets.GITHUB_TOKEN }}
```

</details>

<details><summary><code>Bandit - Security Scan</code></summary>

```yml
  bandit:
    name: Bandit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@master
      - name: check
        uses: nsavelyeva/veripy@master
        with:
          scan: sec
          token: ${{ secrets.GITHUB_TOKEN }}
```

</details>

<details><summary><code>Radon - Cyclomatic Complexity of Code</code></summary>

```yml
  radoncc:
    name: Radon Cyclomatic Complexity
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@master
      - name: check
        uses: nsavelyeva/veripy@master
        with:
          scan: cc
          token: ${{ secrets.GITHUB_TOKEN }}
```

</details>

<details><summary><code>Radon - Maintainability Index of Code</code></summary>

```yml
  radommi:
    name: Radon Maintainability Index
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@master
      - name: check
        uses: nsavelyeva/veripy@master
        with:
          scan: mi
          token: ${{ secrets.GITHUB_TOKEN }}
```

</details>

<details><summary><code>Radon - Halstead Metrics</code></summary>

```yml
  hal:
    name: Halstead metrics info
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@master
      - name: check
        uses: nsavelyeva/veripy@master
        with:
          scan: hal
          token: ${{ secrets.GITHUB_TOKEN }}
```

</details>

<details><summary><code>Radon - Raw Metrics</code></summary>

```yml
  info:
    name: Raw info
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@master
      - name: check
        uses: nsavelyeva/veripy@master
        with:
          scan: raw
          token: ${{ secrets.GITHUB_TOKEN }}
```

</details>

<details><summary><code>Nose2 & Coverage - Unit Tests with Code Coverage</code></summary>

```yml
  covgate:
    name: Unit tests with coverage
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@master
      - name: check
        uses: nsavelyeva/veripy@master
        with:
          scan: cov
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Archive artifacts
        if: success() || failure()
        uses: actions/upload-artifact@v2
        with:
          name: results
          path: |
            coverage.xml
            htmlcov
```
</details>


If you need them all, feel free to copy-paste [this full snippet](docs/examples/veripy_all.yml).

## Configuration

The `with` portion of the workflow **must** be configured before the action will work. You can add these in the `with` section found in the examples above.

| Parameter | Description                                                                                                                                                                                                                                                                                                                                                            | Type   | Required |
| --------- | --------------------------------------------------------------------------------------------------------------------- | ------ | -------- |
| `scan`    | execute command - use one of `lint/sec/cc/mi/hal/raw/cov`                                                             | `with` | **Yes**  |
| `path`    | a path to scan, defaults to current working directory                                                                 | `with` | **No**   |
| `options` | additional options for the chosen scanner                                                                             | `with` | **No**   |
| `covgate` | a threshold for unit test coverage to be used as quality gate                                                         | `with` | **No**   |
| `comment` | if `true`, send the comment to the PR                                                                                 | `with` | **No**   |
| `update`  | if `true` and `comment` is `true`, the previously sent comment will be updated otherwise a new one will be created    | `with` | **No**   |
| `token`   | github token, required if `comment` is `true`                                                                         | `with` | **No**   |
