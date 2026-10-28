#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
tmp="$(mktemp -d /tmp/hdrhistogram-c-smoke.XXXXXXXX)"
python3 /usr/libexec/hdrhistogram-c/qa.py --phase installed \
  --prefix /usr --libdir lib64 --work-dir "$tmp/qa" \
  --expected-self-sha b4e1a2cd7e6d5ecd21c525ad272c6be9042661a5a98561cfd0a779c78b9df7be
