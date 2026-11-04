---
name: sikaru-decision
description: Ask Sikaru System One choice, yes-or-no and score questions about a text or JSON state, and get answers with probabilities and confidence. Use when the user wants to classify, route, triage, tag, gate or score tickets, messages, documents or app state, or wants a calibrated yes/no instead of free-form LLM output.
---

# Sikaru decisions (System One)

System One answers named questions about one **state**, which is a text or a JSON
value. There are three question types:

| Type | Use for | Shape |
| --- | --- | --- |
| `noul` | Yes or no | an instruction |
| `choice` | Pick one label | `criteria` maps each label to `null` (or a description) |
| `score` | An ordered scale | `criteria` lists levels from low to high |

A `noul` answer is the probability of yes, from 0 to 1. A `choice` or `score` answer
comes with per-option probabilities and a confidence. Use these numbers: route on a
threshold, or send uncertain cases to a human. Don't treat every answer as certain.
If the model couldn't answer a question, that question is missing from `answers`, so
check for it. Each question can have at most 26 options.

## From the CLI

```sh
# Yes-or-no questions inline (repeatable).
sikaru decision infer "I was charged twice. Please fix this ASAP." \
  --noul urgent="Is this urgent?" --noul refund="Does the customer want a refund?"

# Choice and score questions from a file, as JSON.
cat > questions.json <<'JSON'
{
  "category": {"type": "choice", "instructions": "What is this ticket about?",
               "criteria": {"billing": null, "technical": null, "other": null}},
  "severity": {"type": "score", "instructions": "How severe is it?",
               "criteria": ["low", "medium", "high"]}
}
JSON
sikaru decision infer "I was charged twice." --questions questions.json -o json

# A JSON state from stdin.
cat ticket.json | sikaru decision infer --json --questions questions.json -o json
```

Signed-in calls bill the saved project.

## From code

```python
import os

from sikaru_sdk import SikaruApi

client = SikaruApi(api_key=os.environ["SIKARU_API_KEY"])  # defaults to https://api.sikaru.ai
decision = client.decisions.create(
    state="I was charged twice.",
    questions={"refund": {"type": "noul", "instructions": "Does the customer want a refund?"}},
)
```

TypeScript has the same call, `client.decisions.create(...)`, on `SikaruApi` from
`@aadi-labs/sikaru-sdk`. Check exact fields with `sikaru decision infer --schema` or the OpenAPI
schema (`POST /v1/systemone`).

## Writing good questions

- Make each question about one thing, and name it for the field your code reads.
- Make choice labels mutually exclusive. Add an `other` label when the set isn't closed.
- Order score levels from low to high, and keep them few.
- Put only the facts needed for the decision in the state. It can contain customer
  data, so don't log it carelessly.
