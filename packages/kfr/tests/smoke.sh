#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- kfr
test -f /usr/include/kfr/config.h
test -f /usr/lib/libkfr_dsp.a
test -f /usr/lib64/cmake/kfr/KFRConfig.cmake
