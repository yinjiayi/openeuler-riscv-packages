#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- macchanger
macchanger --version | grep -F '1.7.0'

