#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- sipsak
sipsak --version | grep -F '0.9.8.1'

