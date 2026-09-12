#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- kahip
command -v kaffpa interface_test kaffpaE parhip >/dev/null

smoke_log="$(mktemp)"
trap 'rm -f -- "$smoke_log"' EXIT
interface_test >"$smoke_log"
grep -F 'partitioning graph from the manual' "$smoke_log"
grep -E '^edge cut [0-9]+$' "$smoke_log"
grep -E '^qap [0-9]+$' "$smoke_log"

rpm -ql kahip | grep -E '/libkahip\.so$'
rpm -ql kahip | grep -E '/libparhip_interface\.so$'
