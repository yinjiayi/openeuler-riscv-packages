#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-JSON-Types
perl -MJSON::Types -e 'my $n = number("42"); my $b = bool(1); die "type helpers failed" unless $n == 42 && ref($b) eq "SCALAR" && $$b == 1;'
