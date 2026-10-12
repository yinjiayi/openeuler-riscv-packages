#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Test-Filename
rpm -q --whatprovides 'perl(Test::Filename)'
module_path=$(perl -e 'require Test::Filename; print $INC{"Test/Filename.pm"} or die "module path missing\n"')
test -f "$module_path"
rpm -qf -- "$module_path"

output=$(perl -MTest::Filename -e '
  filename_is("./alpha.txt", "alpha.txt", "same normalized path");
  filename_isnt("alpha.txt", "beta.txt", "distinct paths");
  Test::Filename->builder->done_testing;
')
[[ "$output" == *"ok 1 - same normalized path"* ]]
[[ "$output" == *"ok 2 - distinct paths"* ]]
[[ "$output" == *"1..2"* ]]
printf '%s\n' "$output"
