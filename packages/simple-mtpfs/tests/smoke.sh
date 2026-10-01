#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- simple-mtpfs
command -v simple-mtpfs >/dev/null
simple-mtpfs --version | grep -F 'simple-mtpfs version 0.4.0'
simple-mtpfs --help 2>&1 | grep -F 'usage: simple-mtpfs'
