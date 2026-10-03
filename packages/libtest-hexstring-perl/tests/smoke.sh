#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Test-HexString
rpm -q --whatprovides 'perl(Test::HexString)'
module_path=$(perl -e 'require Test::HexString; print $INC{"Test/HexString.pm"} or die "module path missing\n"')
test -f "$module_path"
rpm -qf -- "$module_path"

output=$(perl -MTest::More -MTest::HexString -e '
  is_hexstr("\x00\xff", "\x00\xff", "binary equality");
  is_hexstr("alpha", "alpha", "text equality");
  done_testing;
')
[[ "$output" == *"ok 1 - binary equality"* ]]
[[ "$output" == *"ok 2 - text equality"* ]]
[[ "$output" == *"1..2"* ]]
printf '%s\n' "$output"
