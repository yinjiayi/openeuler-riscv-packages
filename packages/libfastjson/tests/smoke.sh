#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libfastjson
rpm -ql libfastjson | grep -F '/libfastjson.so.4'

