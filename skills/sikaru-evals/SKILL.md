---
name: sikaru-evals
description: Create and version Sikaru RL environment datasets from CSV or JSONL, run an agent against them, and read pass rates and failed examples. Use when the user wants to evaluate, test, benchmark or regression-check a Sikaru agent, build an eval set or golden dataset, compare agent versions, or find out why examples fail.
---

# Sikaru evals

An eval runs every eligible example in an environment dataset against an agent's
**live** version, then reports pass rates for each agent version. Publish the agent
first (see `author-sikaru-agent`), because a saved draft isn't what gets tested.

## 1. Build the dataset

Each example needs an `input` and can have `expected`, `tags` and `metadata`.

```jsonl
{"input": "Which pandas function reads a CSV file?", "expected": "pandas.read_csv", "tags": ["io"]}
{"input": [{"role": "user", "content": "Drop rows with nulls"}], "expected": "df.dropna()"}
```

- `input` is a string (one user message) or a list of messages.
- `expected` is optional. A string becomes the expected assistant reply.
- In a CSV, the columns are `input`, `expected` and `tags`, with tags separated by commas.
- The limits are 10 MB and 5,000 examples per file.

```sh
sikaru environment push examples.jsonl --name pandas-qa --purpose eval
sikaru environment list
sikaru environment info DATASET_ID                  # examples, versions, check results
sikaru environment pull DATASET_ID --file out.jsonl # export, e.g. to edit and re-push
```

`--purpose` is `eval`, `training` or `experiment`. Keep held-out eval data apart from
training data.

## 2. Run the eval

```sh
sikaru eval run DATASET_ID --agent AGENT --follow   # waits, then prints the summary
sikaru eval run DATASET_ID --agent AGENT --dataset-version N
```

Without `--follow`, `eval run` returns once checks start. Read the results with
`eval get` and don't report numbers before the checks settle.

## 3. Read results and dig into failures

```sh
sikaru eval list                                     # datasets that have been run
sikaru eval get DATASET_ID --agent AGENT             # pass rate per agent version
sikaru eval samples DATASET_ID --agent AGENT         # failed examples with run IDs
sikaru eval logs RUN_ID                              # one example run's events
sikaru traces get RUN_ID                             # its full trajectory
sikaru eval stop RUN_ID
```

When you report, give the pass rate with its agent version and dataset version.
Group failures by cause and quote the run IDs. Propose document changes, then
re-run on the same dataset version so the numbers stay comparable.

## Judging retained traces with a rubric

To score traces you already have against a rubric, instead of re-running examples,
use evaluation jobs: `sikaru eval evaluation-jobs --help` and
https://docs.sikaru.ai/improve/evaluations.md.
