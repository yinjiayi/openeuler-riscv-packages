#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Test-CheckDeps
rpm -q --whatprovides 'perl(Test::CheckDeps)'
module_path=$(perl -e 'require Test::CheckDeps; print $INC{"Test/CheckDeps.pm"} or die "module path missing\n"')
test -f "$module_path"
rpm -qf -- "$module_path"

# Exercise installed functionality without relying on a source-tree META file.
output=$(perl -MCPAN::Meta -MTest::More -MTest::CheckDeps=check_dependencies_opts -e '
  my $meta = CPAN::Meta->new({
    "meta-spec" => { version => 2 },
    name => "Installed-Smoke", version => "0.001",
    abstract => "installed dependency check",
    author => ["package smoke"], license => ["perl_5"],
    generated_by => "installed package smoke",
    dynamic_config => 0, release_status => "stable",
    prereqs => { runtime => { requires => { "Test::Builder" => 0 } } }
  });
  check_dependencies_opts($meta, "runtime", "requires");
  done_testing;
')
[[ "$output" == *"ok 1 - Test::Builder satisfies '0'"* ]]
[[ "$output" == *"1..1"* ]]
