# Docker Lab Snippets

## Start And Inspect Exposed Service

```bash
docker compose up --build
docker compose ps
curl -sI http://127.0.0.1:PORT/
nc -vz 127.0.0.1 PORT
```

## Remote Parity Rule

Allowed:

- Read Dockerfile for binary name, architecture, exposed ports, flag path.
- Read source to find reachable bugs.
- Connect only through exposed HTTP/TCP/WebSocket service.

Avoid:

- Reading `.env`, seeded admin passwords, hardcoded flags.
- `docker exec`, `docker cp`, `docker inspect`, overlayfs reads to get secrets.
- Treating local fixture data as the final solve.

## Web Local Replay

```bash
BASE=http://127.0.0.1:PORT
curl -sI "$BASE"
curl -s "$BASE/robots.txt"
ffuf -u "$BASE/FUZZ" -w wordlist.txt
```

## Pwn Local Replay

```bash
docker compose up --build
nc -vz 127.0.0.1 PORT
python3 exploit.py LOCAL
python3 exploit.py REMOTE HOST=127.0.0.1 PORT=PORT
```

## Source-To-Exploit Discipline

If source reveals:

- admin password: use it only to understand auth boundary, not as solve input.
- flag path: use it for ORW/file-read payloads, not direct host read.
- service names: use them for SSRF hypotheses.
- internal ports: verify through exposed SSRF/network primitive.

