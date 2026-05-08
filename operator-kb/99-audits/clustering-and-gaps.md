# Clustering And Gaps

## Proposed Clusters

### 1. Methodology And Operations

- Evidence logging
- Remote parity
- Local lab reproduction
- Timeboxing
- Stuck recovery
- Safe static analysis
- Tool escalation rules

### 2. Domain Playbooks

- Web
- Forensics
- Reverse Engineering
- Pwn
- Crypto
- OSINT
- Misc/Specialized
- AI/ML

### 3. Cross-Category Patterns

- Parser discrepancies
- Oracles and side channels
- Polyglots and file-format abuse
- Covert channels
- Encoding and serialization boundaries
- Source leaks and repository recovery
- Local-to-remote parity failures
- Multi-stage chains

### 4. Specialized/Niche Technique Families

- Web3 governance/proxy/proof issues
- Malware-style C2 and config extraction
- RF/SDR/IQ signal analysis
- Peripheral captures: USB, Bluetooth, keyboard LEDs, MIDI
- Hardware/firmware/bootloader/automotive
- Kernel exploitation and kernel reversing
- AI/ML model and LLM attacks
- CTFd API operations
- Platform privesc in Linux-like challenge boxes

## Orphan Or Hard-To-Categorize Techniques

These are preserved as first-class references rather than discarded:

| Technique | Why It Is Awkward | Assigned Home |
|---|---|---|
| AI chatbot jailbreak inside Web auth flow | Web surface, AI reasoning bug | `09-ai-ml/` plus Web auth notes |
| Web3 Groth16 proof forgery | Crypto math inside blockchain app | Web3 under Web, crypto cross-reference |
| ExifTool RCE | File parser CVE used through web upload or forensics | Web server-side and cross-category file parser abuse |
| XSS-to-binary-pwn bridge | Browser exploit used to drive native exploit | Cross-category chains and Pwn advanced |
| QR reconstruction from format-string constraints | Forensics/Misc/Pwn overlap | Misc specialized plus cross-category polyglots |
| DNS compression pointer overflow | Network protocol plus binary exploitation | Pwn advanced plus DNS references |
| Neural network output function-pointer OOB | AI model behavior creates pwn primitive | AI/ML and Pwn advanced |
| TensorFlow DNN inversion in reverse notes | ML technique discovered through RE | AI/ML plus Reverse specialized |
| CTFd API navigation | Operational workflow, not challenge category | Misc specialized / competition ops |
| Linux privesc in CTF boxes | Not classic CTF category, but frequent operator task | Misc specialized / platform privesc |

## Recurring Cross-Category Workflows

- Decode before exploit: encodings appear in Web cookies, Crypto inputs, Forensics blobs, Reverse constants, and Misc puzzles.
- Parser mismatch hunting: Web URL parsers, archive tools, image libraries, XML, SQL, browsers, binary file parsers.
- Oracle extraction: blind SQLi, timing leaks, padding oracles, comparison services, instruction counts, jails, games.
- File-format polyglots: PNG/ZIP/PHP, JPEG/HTML, DOCX/XXE, WAV upload bypass, QR tiles, Office XML.
- Secret recovery from side artifacts: Git history, source maps, browser storage, memory dumps, environment leaks, build artifacts.
- Local lab parity: Docker/web/pwn challenges can mislead if setup secrets are used directly.

## Sparse Coverage

| Area | Current State | Suggested Future Work |
|---|---|---|
| Standalone crypto | Present mostly through Misc/Web/Reverse examples, not a source folder | Add `ctf-crypto/` with RSA, ECC, symmetric, hashes/MACs, lattices, RNG, oracles. |
| Cloud-native CTFs | Some S3/K8s/BuildKit notes | Add cloud IAM, metadata services, GCP/Azure/AWS service-specific playbooks. |
| Modern mobile forensics | Android coverage exists, iOS sparse | Add iOS backups, keychain, app containers, APFS mobile artifacts. |
| ICS/OT and radio | Some CAN/RF/signal notes | Add Modbus, MQTT, Zigbee, LoRa, BLE, SDR demod recipes. |
| Modern browser exploitation | XSS/CSP/XS-Leaks exist, memory corruption sparse | Add browser exploit triage and V8/WebKit CTF patterns. |
| Blue-team log analytics | Windows/Linux notes exist | Add Sigma, EVTX timelines, cloud audit logs, SIEM query patterns. |
| Hardware fault/side-channel | Some power/acoustic/signal notes | Add chip-off, JTAG/SWD, glitching, side-channel tooling. |

## Missing-Topic Audit

Add over time:

- `ctf-crypto/` source notes.
- A payload corpus with tested variants and constraints.
- A "challenge postmortem" template.
- Tool installation/bootstrap scripts.
- A glossary of parser differentials and encoding edge cases.
- A decision-tree wall chart for live competitions.
- More sample exploit skeletons with remote/local toggles.

