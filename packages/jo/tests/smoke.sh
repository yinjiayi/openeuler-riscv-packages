#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- jo
jo -V | grep -F '"version":"1.9"'

json=$(jo answer=42 enabled=true name=RVA23)
test "$json" = '{"answer":42,"enabled":true,"name":"RVA23"}'
