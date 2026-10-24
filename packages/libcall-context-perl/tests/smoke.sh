#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
perl -MCall::Context -e '
  die "version mismatch\n" unless $Call::Context::VERSION eq "0.05";
  sub list_only { Call::Context::must_be_list(); return (2, 3, 5); }
  sub reject_scalar { Call::Context::must_not_be_scalar(); return (7, 11); }
  my @items = list_only();
  die "list result mismatch\n" unless join(",", @items) eq "2,3,5";
  scalar eval { list_only() };
  die "missing scalar exception\n" unless ref($@) eq "Call::Context::X" && "$@" =~ /scalar/;
  reject_scalar();
  scalar eval { reject_scalar() };
  die "missing non-scalar exception\n" unless ref($@) eq "Call::Context::X";
  print "Call::Context list/scalar/void checks passed\n";
'
