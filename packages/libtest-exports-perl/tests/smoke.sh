#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-test-exports
perl -MTest::Exports -e '
  { package SmokeExports; sub provided { 42 } sub omitted { 1 }
    sub import { my $caller = caller; no strict "refs";
      *{"${caller}::provided"} = \&provided;
    }
  }
  die "unexpected release" unless $Test::Exports::VERSION eq "1";
  import_ok "SmokeExports", [], "import known symbol" or exit 1;
  is_import "provided", "SmokeExports", "symbol comes from fixture" or exit 1;
  cant_ok "omitted", "unrequested symbol was not imported" or exit 1;
  Test::Exports->builder->done_testing;
'
