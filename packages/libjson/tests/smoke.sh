#!/bin/bash
# SPDX-License-Identifier: MIT
set -euo pipefail
rpm -q libjson libjson-devel
rpm -V libjson libjson-devel
bash /usr/share/libjson/run-tests.sh
