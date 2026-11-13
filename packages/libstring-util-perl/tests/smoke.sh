#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-Util
rpm -q --whatprovides 'perl(String::Util)'
perl -MString::Util=trim,contains,startswith,endswith -e '
  die "unexpected version\n" unless $String::Util::VERSION eq "1.36";
  die "trim failed\n" unless trim("  alpha beta  ") eq "alpha beta";
  die "contains zero failed\n" unless contains("value0", "0");
  die "prefix failed\n" unless startswith("alpha", "al");
  die "suffix failed\n" unless endswith("omega", "ga");
'
