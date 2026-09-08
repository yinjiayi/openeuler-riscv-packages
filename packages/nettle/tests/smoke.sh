#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

command -v nettle-hash >/dev/null
digest="$(printf 'abc' | nettle-hash -a sha256 | tr -d ' \n')"
grep -F 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad' <<<"${digest}"
