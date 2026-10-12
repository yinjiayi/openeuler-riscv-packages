#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Test-Refcount
rpm -q --whatprovides 'perl(Test::Refcount)'
module_path=$(perl -e 'require Test::Refcount; print $INC{"Test/Refcount.pm"} or die "module path missing\n"')
test -f "$module_path"
rpm -qf -- "$module_path"

output=$(perl -MTest::Refcount -e '
  my $object = [];
  is_oneref($object, "one reference");
  my $alias = $object;
  is_refcount($object, 2, "two references");
  Test::Refcount->builder->done_testing;
')
[[ "$output" == *"ok 1 - one reference"* ]]
[[ "$output" == *"ok 2 - two references"* ]]
[[ "$output" == *"1..2"* ]]
printf '%s\n' "$output"
