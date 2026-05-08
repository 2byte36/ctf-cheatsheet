# Final Audit

## Cross-Reference Validation

Validated after generation:

- All local Markdown links under `operator-kb/` resolve.
- No non-ASCII characters were introduced in `operator-kb/`.
- The curated KB contains 18 Markdown files and preserves links back to the raw source notes.

Validation commands used:

```bash
find operator-kb -type f -name '*.md' -printf '%p\n' | sort
grep -RInP '[^\x00-\x7F]' operator-kb || true
python3 - <<'PY'
from pathlib import Path
import re
root=Path('operator-kb')
missing=[]
for path in root.rglob('*.md'):
    text=path.read_text()
    for m in re.finditer(r'\[[^\]]+\]\(([^)]+)\)', text):
        target=m.group(1).split('#',1)[0]
        if not target or '://' in target or target.startswith('mailto:'):
            continue
        if not (path.parent/target).resolve().exists():
            missing.append((str(path), target))
print(missing or 'all local markdown links resolve')
PY
```

## Difficult-To-Categorize Techniques

| Technique / Workflow | Categorization Issue | KB Placement |
|---|---|---|
| AI chatbot jailbreak in a web auth challenge | Web endpoint, but AI safety/prompt weakness | Web playbook plus AI/ML playbook |
| Web3 Groth16 proof forgery | Blockchain surface with crypto proof logic | Web playbook plus Crypto playbook |
| ExifTool/WeasyPrint/CairoSVG parser bugs | Web upload/external service and file-forensics overlap | Web playbook plus Cross-Category parser mismatch |
| XSS-to-binary-pwn bridge | Browser primitive drives native exploitation | Pwn playbook plus Cross-Category chains |
| TensorFlow inversion in reverse notes | ML recovery technique discovered through binary analysis | Reverse playbook plus AI/ML playbook |
| Neural network function-pointer OOB | ML model output becomes pwn primitive | AI/ML playbook plus Pwn playbook |
| DNS compression pointer overflow | DNS protocol knowledge plus stack ROP | Pwn playbook plus Misc DNS routing |
| QR reconstruction from format-string constraints | File-format, puzzle, and pwn constraint overlap | Misc playbook plus Cross-Category polyglots |
| CTFd API navigation | Operational competition workflow, not a challenge class | Misc specialized / CTF operations |
| Linux privesc notes | Post-exploitation competition box workflow, not classic category | Misc specialized / platform privesc |

## Sparse Coverage Areas

| Area | Current Coverage | Needed Expansion |
|---|---|---|
| Standalone crypto | Consolidated from embedded Web/Misc/Reverse/Pwn/Forensics examples | Add dedicated source folder for RSA, ECC, symmetric, hashes/MACs, RNG, lattices, and oracles |
| Cloud-native CTF | Some S3/K8s/BuildKit/container notes | Add AWS/GCP/Azure IAM, metadata services, cloud logs, serverless, registry, and Kubernetes exploitation/forensics |
| Modern mobile forensics | Android appears in forensics/reverse; iOS sparse | Add iOS backups, keychain, app groups, APFS mobile artifacts |
| ICS/OT/radio | CAN, RF, UART/I2C, signals exist but scattered | Add Modbus, MQTT, Zigbee, LoRa, BLE, SDR recipes |
| Browser memory exploitation | XSS/CSP/XS-Leaks strong; browser pwn sparse | Add V8/WebKit/Chrome sandbox CTF triage |
| Blue-team detection | Windows/Linux logs present | Add Sigma/YARA-L, EVTX timelines, cloud audit logs, SIEM query playbooks |
| Hardware fault attacks | Side-channel/signal notes exist | Add JTAG/SWD, glitching, chip-off, firmware extraction workflows |
| Payload corpus | Payloads are distributed in playbooks | Add tested payload library indexed by sink and constraints |

## Future Sections To Add

- `ctf-crypto/` source notes and `operator-kb/06-crypto/*` split into subfiles.
- `operator-kb/10-cross-category/oracle-workflows.md`.
- `operator-kb/10-cross-category/parser-mismatch-catalog.md`.
- `operator-kb/90-reference/payload-corpus/`.
- `operator-kb/90-reference/tool-installation.md`.
- `operator-kb/99-audits/postmortem-template.md`.
- `operator-kb/01-triage/live-scoreboard-prioritization.md`.
- `operator-kb/08-misc-specialized/cloud-and-container.md`.
- `operator-kb/03-forensics/mobile-forensics.md`.

