#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Test-Fixme
rpm -q --whatprovides 'perl(Test::Fixme)'
module_path=$(perl -e 'require Test::Fixme; print $INC{"Test/Fixme.pm"} or die "module path missing\n"')
test -f "$module_path"
rpm -qf -- "$module_path"

fixture_dir=$(mktemp -d)
trap 'rm -rf -- "$fixture_dir"' EXIT
printf 'ordinary line\n' > "$fixture_dir/clean.txt"
output=$(perl -MTest::Fixme -e 'run_tests(where => $ARGV[0])' "$fixture_dir")
[[ "$output" == *"1..1"* ]]
[[ "$output" == *"ok 1"* ]]
printf 'FIXME pending\n' > "$fixture_dir/marked.txt"
perl -MTest::Fixme -e '
  my $hits = Test::Fixme::scan_file(file => $ARGV[0], match => "FIXME");
  die "expected one marker\n" unless @$hits == 1 && $hits->[0]{line} == 1;
' "$fixture_dir/marked.txt"
printf '%s\n' "$output"
