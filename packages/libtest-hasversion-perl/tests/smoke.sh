#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Test-HasVersion
rpm -q --whatprovides 'perl(Test::HasVersion)'
rpm -qf -- "$(command -v test_version)"
module_path=$(perl -e 'require Test::HasVersion; print $INC{"Test/HasVersion.pm"} or die "module path missing\n"')
test -f "$module_path"
output=$(test_version "$module_path")
[[ "$output" == *"ok 1 - $module_path has version"* ]]
[[ "$output" == *"1..1"* ]]
