#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- checksec
checksec --version | grep -F '3.2.0'

