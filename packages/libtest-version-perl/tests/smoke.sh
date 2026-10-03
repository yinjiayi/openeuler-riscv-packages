#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Test-Version
rpm -q --whatprovides 'perl(Test::Version)'
perl -MTest::Version=version_ok -e '
  Test::Version->VERSION("2.09");
  my $path = $INC{"Test/Version.pm"} or die "installed module path missing\n";
  version_ok($path) or die "installed module version rejected\n";
'
