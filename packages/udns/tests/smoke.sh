#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

command -v dnsget >/dev/null
command -v rblcheck >/dev/null
dnsget_help="$(dnsget -h 2>&1 || true)"
rblcheck_help="$(rblcheck -h 2>&1 || true)"
grep -Eiq '(^|[^[:alpha:]])usage:|dnsget' <<<"${dnsget_help}"
grep -Eiq '(^|[^[:alpha:]])usage:|rblcheck' <<<"${rblcheck_help}"
