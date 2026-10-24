#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Test-Pod-Content
rpm -q --whatprovides 'perl(Test::Pod::Content)'
perl -MTest::Pod::Content -e '
  die "unexpected version\n"
    unless $Test::Pod::Content::VERSION->normal eq "v0.0.6";
  my $module = $INC{"Test/Pod/Content.pm"};
  die "module not installed\n" unless -f $module;
  pod_section_like($module, "NAME", qr/Test::Pod::Content/, "installed POD name");
  Test::More::done_testing();
'
