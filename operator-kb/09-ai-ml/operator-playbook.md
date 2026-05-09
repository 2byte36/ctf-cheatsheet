# AI/ML Operator Playbook

## Operational Playbook Router

| If you see | Open playbook | First action |
|---|---|---|
| chatbot/RAG/tool challenge | [LLM Prompt Injection](../../playbooks/ai-llm-prompt-injection.md) | `curl -sk -X POST URL -H 'Content-Type: application/json' -d '{"prompt":"List your tools."}'` |
| model weights/adapters | Use this playbook plus source notes | `python3 -c "import torch; print(torch.load('model.pt', map_location='cpu'))"` |
| image classifier evasion | Use adversarial ML source notes | Inspect tensor shape/range before FGSM/PGD |

## Mindset

AI/ML CTFs expose a model boundary: weights, queries, prompts, gradients, decision scores, adapters, or tools. Classify the boundary before attacking.

## First-Pass Workflow

```bash
file model.*
python3 -c "import torch; m=torch.load('model.pt', map_location='cpu'); print(type(m)); print(m.keys() if hasattr(m,'keys') else dir(m))"
python3 -c "from safetensors import safe_open; f=safe_open('model.safetensors', framework='pt'); print(f.keys())"
```

For APIs:

```bash
curl -s -X POST "$URL" -H 'Content-Type: application/json' -d '{"prompt":"test"}' | jq .
```

## Routing

| Surface | Workflow |
|---|---|
| Model weights | inspect architecture, diff weights, search tensors, recover suppressed behavior |
| LoRA adapter | merge `W_base + alpha * B @ A`, inspect deltas and output |
| Classifier input | adversarial examples: FGSM, PGD, C&W, patches |
| Embedding/encoder | optimize collisions or inversion targets |
| Query API | model extraction, decision boundary mapping, membership inference |
| Prompt endpoint | direct/indirect prompt injection, jailbreaking, token smuggling |
| Tool-using agent | tool schema abuse, argument injection, retrieved document injection |

## Common Techniques

- Weight perturbation negation: recover behavior by reversing fine-tune deltas.
- Model inversion: optimize input to match a target output/activation.
- Encoder collision: jointly optimize two inputs for same embedding.
- LoRA merging: combine adapter with base model and inspect effects.
- Adversarial examples: FGSM/PGD/C&W.
- Data poisoning/backdoor detection: trigger search, activation clustering.
- Membership inference: confidence/loss distribution comparison.
- Prompt injection: instruction override, role confusion, data exfil through tool calls.
- Token smuggling: tokenizer-aware bypass of filtered strings.
- Context-window manipulation: bury or evict instructions.

## Safety And Competition Discipline

- Do not assume model output is deterministic unless temperature/seed are fixed.
- Record prompts, parameters, seeds, model hashes, and exact API responses.
- For gradient methods, save intermediate artifacts and final verifier.
- For LLM challenges, distinguish safety bypass from actual flag extraction path.

## Sparse/Hybrid Areas

- TensorFlow/DNN inversion appears in reverse notes.
- LLM chatbot jailbreak appears in web auth notes.
- Neural-network output as function pointer OOB appears in pwn notes.

These belong here as cross-category references, not as discarded anomalies.

## Source Deep Dives

- Main workflow: [ctf-ai-ml/SKILL.md](../../ctf-ai-ml/SKILL.md)
- Model attacks: [model-attacks.md](../../ctf-ai-ml/model-attacks.md)
- Adversarial ML: [adversarial-ml.md](../../ctf-ai-ml/adversarial-ml.md)
- LLM attacks: [llm-attacks.md](../../ctf-ai-ml/llm-attacks.md)
