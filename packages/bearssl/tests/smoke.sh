#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- bearssl bearssl-devel
brssl impl | grep -F 'hash functions:'
test -f /usr/include/bearssl/bearssl.h
