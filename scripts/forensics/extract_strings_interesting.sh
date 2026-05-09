#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:?usage: extract_strings_interesting.sh <file-or-dir>}"

if [ -d "$TARGET" ]; then
  find "$TARGET" -type f -print0 | xargs -0 strings -a -n 6
else
  strings -a -n 6 "$TARGET"
fi | rg -i 'flag|ctf|secret|token|password|passwd|key|http|ftp|ssh|powershell|cmd\.exe|admin|cookie|session' || true

