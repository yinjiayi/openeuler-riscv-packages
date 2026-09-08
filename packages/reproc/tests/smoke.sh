#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- reproc
rpm -ql reproc | grep -E '/libreproc(\+\+)?\.so\.14'

