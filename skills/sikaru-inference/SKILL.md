---
name: sikaru-inference
description: Call Sikaru catalog models from the CLI or from code with the OpenAI-shaped Python and TypeScript SDKs. Use when the user wants to list or compare Sikaru models, check a model's pricing, context or reasoning settings, chat with a model, stream a reply, or point OpenAI-style code at Sikaru.
---

# Sikaru inference

Sikaru serves a model catalog behind OpenAI-shaped endpoints: chat completions,
completions, responses and models. Model IDs look like `lab/model`, for example
`moonshotai/kimi-k3`. Always take IDs from the catalog rather than from memory.

## From the CLI

```sh
sikaru inference models                          # the catalog
sikaru inference models --search kimi --sort input
sikaru inference models MODEL                    # specs, pricing, reasoning efforts
sikaru inference chat MODEL "Explain a rainbow in one sentence."
sikaru inference chat MODEL "..." --stream       # answer on stdout, reasoning on stderr
echo "..." | sikaru inference chat MODEL --system "Answer in plain words." -o json
```

`chat` also takes `-t/--temperature`, `--max-tokens` and `--reasoning-effort`. Read the
supported reasoning efforts from `sikaru inference models MODEL` before setting one.
Signed-in calls bill the saved project (`sikaru config set project PROJECT`).

## From code

Use the inference client, `Sikaru`. It reads `SIKARU_API_KEY` from the environment.
The platform client for agents, runs and datasets is a different class,
`SikaruApi`, so don't mix them up.

```python
from sikaru_sdk import Sikaru  # AsyncSikaru for asyncio

client = Sikaru()
models = client.models.list()
reply = client.chat.completions.create(
    model="moonshotai/kimi-k3",
    messages=[{"role": "user", "content": "Explain a rainbow in one sentence."}],
)
print(reply.choices[0].message.content)

for chunk in client.chat.completions.create(model=..., messages=..., stream=True):
    if chunk.choices and chunk.choices[0].delta:
        print(chunk.choices[0].delta.content or "", end="")
```

```typescript
import { Sikaru } from "@aadi-labs/sikaru-sdk/inference";

const client = new Sikaru({ apiKey: process.env.SIKARU_API_KEY });
const reply = await client.chat.completions.create({
  model: "moonshotai/kimi-k3",
  messages: [{ role: "user", content: "Explain a rainbow in one sentence." }],
});
```

Install with `pip install sikaru-sdk` or `uv add sikaru-sdk`, or `npm i @aadi-labs/sikaru-sdk`.
For reasoning output, pass `include_reasoning`. To move existing OpenAI-style code
over, swap the client and the model ID. Keep the key on the server.

## Choosing a model

Compare candidates with `sikaru inference models --sort input` (or `output`) and read
each card. Recommend by the user's constraints: price, context length, reasoning
support. State the numbers you read; don't assert them from memory.

Docs: https://docs.sikaru.ai/inference/inference-api.md
