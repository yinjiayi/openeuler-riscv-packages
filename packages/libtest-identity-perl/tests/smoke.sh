#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Test-Identity
rpm -q --whatprovides 'perl(Test::Identity)'
module_path=$(perl -e 'require Test::Identity; print $INC{"Test/Identity.pm"} or die "module path missing\n"')
test -f "$module_path"
rpm -qf -- "$module_path"

output=$(perl -MTest::More -MTest::Identity -e '
  my $reference = [];
  identical($reference, $reference, "same reference");
  identical(undef, undef, "both undefined");
  done_testing;
')
[[ "$output" == *"ok 1 - same reference"* ]]
[[ "$output" == *"ok 2 - both undefined"* ]]
[[ "$output" == *"1..2"* ]]
printf '%s\n' "$output"
