#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-text-reflow
expected='Alpha beta gamma
delta epsilon zeta.

Second paragraph.'
result=$(perl -MText::Reflow=reflow_string -e 'die "wrong module" unless $Text::Reflow::VERSION eq "1.17"; print reflow_string("Alpha beta gamma delta epsilon zeta.\n\nSecond paragraph.\n", maximum=>20, optimum=>[18])')
test "$result" = "$expected"
result=$(printf 'Alpha beta gamma delta epsilon zeta.\n\nSecond paragraph.\n' | /usr/bin/reflow)
test "$result" = 'Alpha beta gamma delta epsilon zeta.

Second paragraph.'
printf '%s\n' 'Text::Reflow XS line-breaking and CLI paragraph handling passed'
