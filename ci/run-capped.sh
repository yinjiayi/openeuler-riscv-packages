#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail

log=
max_bytes=52428800
timeout_seconds=7200
while (($#)); do
  case $1 in
    --log) log=${2:?}; shift 2 ;;
    --max-bytes) max_bytes=${2:?}; shift 2 ;;
    --timeout-seconds) timeout_seconds=${2:?}; shift 2 ;;
    --) shift; break ;;
    *) printf 'run-capped: unknown argument %s\n' "$1" >&2; exit 2 ;;
  esac
done
[[ -n $log && $# -gt 0 ]] || { printf 'usage: run-capped --log FILE [options] -- COMMAND...\n' >&2; exit 2; }
[[ $max_bytes =~ ^[1-9][0-9]*$ && $timeout_seconds =~ ^[1-9][0-9]*$ ]] || exit 2
mkdir -p "$(dirname "$log")"

blocks=$(( (max_bytes + 511) / 512 ))
set +e
(
  ulimit -f "$blocks"
  timeout --signal=TERM --kill-after=30s "$timeout_seconds" "$@"
) >"$log" 2>&1
status=$?
set -e

size=$(wc -c <"$log" | awk '{$1=$1; print}')
if ((size >= max_bytes)); then
  printf '[ci] log reached the configured %s-byte safety limit\n' "$max_bytes" >&2
  status=1
fi
# Prefix untrusted build output so it cannot inject GitHub workflow commands.
tail -c 4194304 "$log" | sed 's/^/[build] /'
exit "$status"

