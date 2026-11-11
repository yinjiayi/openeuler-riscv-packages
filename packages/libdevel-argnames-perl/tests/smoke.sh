#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
perl -MDevel::ArgNames -e '
  use strict;
  use warnings;
  die "version mismatch\n" unless $Devel::ArgNames::VERSION eq "0.03";
  sub names { Devel::ArgNames::arg_names() }
  my ($first, $second) = (23, 64);
  my @names = names($first, $second);
  die "lexical names mismatch\n" unless @names == 2 && $names[0] eq q($first) && $names[1] eq q($second);
  print "Devel::ArgNames lexical argument names passed\n";
'
