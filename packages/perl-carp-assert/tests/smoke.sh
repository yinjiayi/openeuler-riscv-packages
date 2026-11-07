#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-carp-assert
perl <<'PERL'
use strict;
use warnings;
BEGIN { delete @ENV{qw(NDEBUG PERL_NDEBUG)}; }
use Carp::Assert;
die "version" unless $Carp::Assert::VERSION eq '0.22';
assert(1); should('same','same'); shouldnt('left','right');
my $ok=eval { assert(0,'expected failure'); 1 }; die "assertion did not fail" if $ok;
die "unexpected assertion error" unless $@ =~ /expected failure/;
{ package DisabledSmoke; no Carp::Assert; assert(0) if DEBUG; }
print "Carp::Assert smoke passed\n";
PERL
