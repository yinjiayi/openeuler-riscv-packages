#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-Random
rpm -q --whatprovides 'perl(String::Random)'
perl -MString::Random -e '
  die "unexpected version\n" unless $String::Random::VERSION eq "0.32";
  my $r = String::Random->new(rand_gen => sub { my ($max) = @_; return $max - 1 });
  die "pattern mismatch\n" unless $r->randpattern("cCn") eq "zZ9";
  die "regex mismatch\n" unless $r->randregex("[a-z][A-Z][0-9]") eq "zZ9";
'
