#!/bin/bash
# SPDX-License-Identifier: MIT
set -euo pipefail
rpm -q liblcf liblcf-devel liblcf-tools
rpm -V liblcf liblcf-devel liblcf-tools
exec bash /usr/share/liblcf/run-tests.sh
