#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-IO-Prompt-Tiny
PERL_MM_USE_DEFAULT=1 perl -MIO::Prompt::Tiny=prompt -e 'die "default prompt failed" unless prompt("Question?", "default") eq "default";'
