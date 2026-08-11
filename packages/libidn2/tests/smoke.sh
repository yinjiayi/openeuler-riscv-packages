#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libidn2 libidn2-devel idn2

encoded=$(idn2 --quiet -- 'bücher.example')
test "$encoded" = 'xn--bcher-kva.example'
decoded=$(idn2 --quiet --decode -- "$encoded")
test "$decoded" = 'bücher.example'
