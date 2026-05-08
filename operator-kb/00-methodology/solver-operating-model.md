# Solver Operating Model

## Core Loop

The operator loop is:

```text
Inventory -> classify -> hypothesize -> run one small test -> record evidence -> refine -> exploit or pivot
```

Good CTF solving is not "try all tools." It is controlled uncertainty reduction. Every command should answer a question.

## Operational Principles

| Principle | Competition Behavior |
|---|---|
| Preserve evidence | Hash inputs, keep originals read-only, write derived files under `work/`, `extracts/`, or `logs/`. |
| Establish baseline | Capture normal behavior before fuzzing, patching, brute forcing, or exploitation. |
| Prove primitives | Demonstrate leak, write, oracle, bypass, or control before building a long chain. |
| Favor remote parity | Use local source and Docker for analysis, but solve through the exposed interface. |
| Minimize scope | Reverse only the validation path, exploit only the needed bug, carve only likely evidence first. |
| Automate after understanding | Write scripts after mapping protocol/rules manually. |
| Log assumptions | Mark facts, hypotheses, failed attempts, and next tests separately. |

## Hypothesis Quality

| Weak | Strong |
|---|---|
| "Maybe SQLi." | "`id` changes response length on boolean predicates and quote errors differ by DB." |
| "Maybe stego." | "PNG has valid IEND at offset X and extra ZIP magic after EOF." |
| "Maybe pwn." | "`gets()` reaches saved RIP, no canary, offset is 72." |
| "Maybe crypto." | "Two ECDSA signatures share `r`, so nonce reuse can recover the private key." |

## Escalation Ladder

Before advanced tooling, validate:

1. Prompt, title, tags, filenames, and all provided files.
2. File type, magic bytes, metadata, hashes, strings.
3. Baseline behavior with normal input.
4. One-variable mutations.
5. Physical flag location: file, DB, browser, memory, blockchain, model output, hidden object.
6. Local vs remote differences.
7. Whether the current plan depends on local setup secrets.

## Competition Timeboxes

| Time | Action |
|---|---|
| 0-5 min | Inventory, classify, obvious strings/metadata/routes. |
| 5-15 min | Build baseline and test two or three high-confidence primitives. |
| 15-35 min | Commit to the best hypothesis and script the loop. |
| 35-45 min | If no primitive exists, pivot category or hand off notes. |
| 45+ min | Continue only with a concrete primitive or high-confidence path. |

## Stuck Recovery

Use this when activity becomes random:

- State the challenge in one sentence.
- List known facts only.
- List current hypotheses and what would falsify each one.
- Re-run low-cost checks: `file`, `strings`, metadata, routes, protocol stats.
- Try smallest inputs: empty, one byte, long string, null, newline, quote, slash, JSON object, array.
- Search for decoys: fake flags, troll encodings, misleading extensions, dead branches.
- Ask which parser, trust boundary, or oracle is actually exposed.

## Source Notes

- Web remote parity and bot workflow: [ctf-web/SKILL.md](../../ctf-web/SKILL.md)
- Forensic evidence loop: [ctf-forensic/SKILL.md](../../ctf-forensic/SKILL.md)
- Reverse quick wins: [ctf-reverse/SKILL.md](../../ctf-reverse/SKILL.md)
- Pwn service-only exploit rule: [ctf-pwn/SKILL.md](../../ctf-pwn/SKILL.md)

