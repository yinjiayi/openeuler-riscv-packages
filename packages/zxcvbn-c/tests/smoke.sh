#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- zxcvbn-c
test -x /usr/bin/zxcvbn-dictgen
test -r /usr/share/zxcvbn/zxcvbn.dict
test -r /usr/include/zxcvbn.h
