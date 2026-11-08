#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
set -eu
exec python3 -I -B /usr/libexec/lsw-tests/qa.py ''
