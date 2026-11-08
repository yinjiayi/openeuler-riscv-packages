#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
perl -MTie::Function -e '
    tie my %multiply, "Tie::Function", sub { $_[0] * $_[1] };
    die "tied lookup did not invoke function\n" unless $multiply{6,7} == 42;
'
printf '%s\n' 'ok - installed Tie::Function invokes the tied function'
