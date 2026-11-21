#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-test-mojibake
fixture_dir=$(mktemp -d)
trap 'rm -f -- "$fixture_dir/example.pl"; rmdir -- "$fixture_dir"' EXIT
printf '%s\n' 'use strict;' 'use warnings;' 'my $value = 42;' > "$fixture_dir/example.pl"
tap=$(scan_mojibake "$fixture_dir/example.pl")
printf '%s\n' "$tap"
grep -Fqx -- "1..1" <<< "$tap"
grep -Fqx -- "ok 1 - Mojibake test for $fixture_dir/example.pl" <<< "$tap"
