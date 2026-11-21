#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
perl -MTest::ConsistentVersion -e '
  BEGIN {
    package ConsistentVersionSmokeFixture;
    our $VERSION = "1.0";
    $INC{"ConsistentVersionSmokeFixture.pm"} = __FILE__;
  }
  die "unexpected installed module version" unless
    version->parse(Test::ConsistentVersion->VERSION)->normal eq "v0.3.1";
  Test::ConsistentVersion::check_consistent_versions(
    files => 1, modules => ["ConsistentVersionSmokeFixture"],
    no_pod => 1, no_changelog => 1, no_readme => 1
  );
'
