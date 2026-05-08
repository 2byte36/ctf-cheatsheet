# CTF Operator Knowledge Base

This directory is the curated operator layer above the raw skill notes in the repository. The original `ctf-*` folders remain source material. The files here reorganize that material by how a solver actually works during a competition: triage, hypothesis loops, exploit/recovery workflows, cross-category patterns, references, and audits.

## How To Use This KB

Start with:

1. [Solver Operating Model](00-methodology/solver-operating-model.md)
2. [Challenge Routing](01-triage/challenge-routing.md)
3. The relevant domain playbook:
   - [Web](02-web/operator-playbook.md)
   - [Forensics](03-forensics/operator-playbook.md)
   - [Reverse Engineering](04-reverse/operator-playbook.md)
   - [Pwn](05-pwn/operator-playbook.md)
   - [Crypto](06-crypto/operator-playbook.md)
   - [OSINT](07-osint/operator-playbook.md)
   - [Misc and Specialized](08-misc-specialized/operator-playbook.md)
   - [AI/ML](09-ai-ml/operator-playbook.md)
4. [Cross-Category Patterns](10-cross-category/patterns.md)
5. [Tools Matrix](90-reference/tools-matrix.md)

## Source Material

The current source notes include:

- `ctf-web/`: Web exploitation, auth, client-side, server-side, JWT/JWE, Node/prototype pollution, Web3, CVE-shaped attacks.
- `ctf-forensic/`: evidence triage, disk/memory/network/stego/windows/linux/peripheral/signal forensics, malware-style static analysis.
- `ctf-reverse/`: binary triage, tooling, anti-analysis, VM/bytecode, platform/language-specific reversing, CTF case patterns.
- `ctf-pwn/`: exploit lifecycle, stack/ROP/shellcode, format strings, heap/FSOP, kernel, sandbox escapes, advanced primitives.
- `ctf-misc/`: encodings, jails, games, VMs, RF/SDR, DNS, privesc, CTFd operations, puzzle oracles.
- `ctf-osint/`: geolocation, social media, usernames, DNS/WHOIS/archive, GitHub, Shodan, platform-specific OSINT.
- `ctf-ai-ml/`: adversarial examples, model extraction, model inversion, LoRA, LLM prompt/tool attacks.

## Architecture

```text
operator-kb/
  00-methodology/       Solver behavior, evidence discipline, remote parity
  01-triage/            Challenge classification and routing heuristics
  02-web/               Web operator playbook
  03-forensics/         Forensics operator playbook
  04-reverse/           Reverse engineering operator playbook
  05-pwn/               Binary exploitation operator playbook
  06-crypto/            Crypto operator playbook and embedded crypto extraction
  07-osint/             OSINT operator playbook
  08-misc-specialized/  Jails, encodings, RF, DNS, games, VMs, privesc, CTFd
  09-ai-ml/             AI/ML challenge playbook
  10-cross-category/    Recurring workflows and attack-chain patterns
  90-reference/         Tools, commands, payloads, magic bytes, snippets
  99-audits/            Extraction, clustering, gaps, orphan techniques
```

## Maintenance Rule

When new CTF notes are added, update:

1. [Knowledge Extraction](99-audits/knowledge-extraction.md)
2. [Clustering And Gaps](99-audits/clustering-and-gaps.md)
3. The relevant domain playbook
4. [Tools Matrix](90-reference/tools-matrix.md) if a new tool appears
5. [Cross-Category Patterns](10-cross-category/patterns.md) if the technique repeats across domains

