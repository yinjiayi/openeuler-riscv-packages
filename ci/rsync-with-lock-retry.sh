#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -uo pipefail

lock_error='rrsync error: Another instance of rrsync is already accessing this directory.'
max_attempts=${RRSYNC_LOCK_MAX_ATTEMPTS:-6}
base_delay=${RRSYNC_LOCK_BASE_DELAY_SECONDS:-2}
jitter_max=${RRSYNC_LOCK_JITTER_MAX_SECONDS:-7}
jitter_key=${RRSYNC_LOCK_JITTER_KEY:-local}

[[ $max_attempts =~ ^[1-9][0-9]*$ && $max_attempts -le 10 ]] \
  || { printf 'invalid RRSYNC_LOCK_MAX_ATTEMPTS: %s\n' "$max_attempts" >&2; exit 2; }
[[ $base_delay =~ ^[0-9]+$ && $base_delay -le 60 ]] \
  || { printf 'invalid RRSYNC_LOCK_BASE_DELAY_SECONDS: %s\n' "$base_delay" >&2; exit 2; }
[[ $jitter_max =~ ^[0-9]+$ && $jitter_max -le 10 ]] \
  || { printf 'invalid RRSYNC_LOCK_JITTER_MAX_SECONDS: %s\n' "$jitter_max" >&2; exit 2; }
[[ ${#jitter_key} -le 128 && $jitter_key =~ ^[A-Za-z0-9._:-]+$ ]] \
  || { printf 'invalid RRSYNC_LOCK_JITTER_KEY\n' >&2; exit 2; }
[[ ${1:-} == -- && $# -ge 2 ]] \
  || { printf 'usage: %s -- command [args...]\n' "$0" >&2; exit 2; }
shift

retry_log=$(mktemp "${TMPDIR:-/tmp}/rrsync-lock-retry.XXXXXX")
trap 'rm -f -- "$retry_log"' EXIT

attempt=1
while :; do
  : >"$retry_log"
  "$@" >"$retry_log" 2>&1
  result=$?
  cat "$retry_log" >&2
  if (( result == 0 )); then
    exit 0
  fi
  if (( result != 12 )) || ! grep -Fq -- "$lock_error" "$retry_log"; then
    exit "$result"
  fi
  if (( attempt >= max_attempts )); then
    printf 'rrsync lock remained busy after %s attempts\n' "$attempt" >&2
    exit "$result"
  fi
  jitter_hash=$(printf '%s:%s\n' "$jitter_key" "$attempt" | cksum | awk '{print $1}')
  jitter=$(( jitter_hash % (jitter_max + 1) ))
  delay=$(( base_delay * (1 << (attempt - 1)) + jitter ))
  printf 'rrsync directory lock busy on attempt %s/%s; retrying after %ss\n' \
    "$attempt" "$max_attempts" "$delay" >&2
  sleep "$delay"
  attempt=$((attempt + 1))
done
