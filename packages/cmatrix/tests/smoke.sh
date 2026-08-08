#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- cmatrix
cmatrix -h 2>&1 | grep -i 'usage'
test -r /usr/lib/kbd/consolefonts/matrix.fnt
test -r /usr/lib/kbd/consolefonts/matrix.psf.gz
