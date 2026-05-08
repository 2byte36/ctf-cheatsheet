# Evidence Notes And Remote Parity

## Evidence Notebook Template

Use this for every challenge:

````markdown
# <challenge>

## Prompt
> exact prompt

## Artifacts
- path, size, sha256, file type
- target URL/host/port

## Facts
- evidence-backed observation

## Hypotheses
- confidence / effort / expected proof

## Commands
```bash
copyable command
```

## Results
- decisive snippets only

## Failed Paths
- what was tested and why it failed

## Next Test
- one concrete next action

## Flag
`flag{...}`
````

## Remote Parity

Local files, source, and containers help identify reachable behavior. They are not solve inputs.

Allowed:

- Read Dockerfiles for binary name, base image, architecture, port, and internal flag path.
- Read source code to identify sinks, trust boundaries, and reachable bugs.
- Start local services and interact through exposed HTTP/TCP/WebSocket interfaces.
- Use local behavior to validate a primitive that would still work remotely.

Avoid:

- Reading `.env`, fixture credentials, seeded admin passwords, hardcoded flags, or startup logs as solve input.
- `docker exec`, `docker cp`, `docker inspect`, direct volume reads, overlayfs reads, or container process environment reads to obtain secrets.
- Logging in with credentials discovered only from setup files.
- Treating local seeded data as the remote exploit.

Parity test:

```text
Would this chain still work if secrets, admin passwords, seeded rows, and flags were rotated?
```

If no, record the observation as reconnaissance and continue toward a reachable weakness.

## Safe Static Analysis

For unknown executables, scripts, macro documents, shellcode, and malware-like artifacts:

- Do not execute directly on the host.
- Prefer `file`, `sha256sum`, `strings`, `xxd`, `objdump`, `readelf`, `oletools`, decompilers, and isolated emulation of extracted routines.
- Record hashes and output paths for carved/extracted files.

## Minimal Workspace Layout

```bash
mkdir -p work extracts carved logs scripts notes
find . -maxdepth 3 -type f -printf '%p\t%s bytes\n' | sort | tee notes/inventory.txt
find . -maxdepth 3 -type f -exec file -k {} \; | tee notes/filetypes.txt
find . -maxdepth 3 -type f -exec sha256sum {} \; | tee notes/hashes.txt
```

