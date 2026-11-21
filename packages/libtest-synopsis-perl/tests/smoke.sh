#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-test-synopsis
fixture_dir=$(mktemp -d)
trap 'rm -f -- "$fixture_dir/example.pm"; rmdir -- "$fixture_dir"' EXIT
printf '%s\n' '=head1 SYNOPSIS' '' '    my $example = 42;' '' '=cut' > "$fixture_dir/example.pm"
tap=$(perl -MTest::Synopsis -MTest::More=tests,1 -e 'synopsis_ok($ARGV[0])' "$fixture_dir/example.pm")
printf '%s\n' "$tap"
grep -Fqx -- "ok 1 - $fixture_dir/example.pm" <<< "$tap"
