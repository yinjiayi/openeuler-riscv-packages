#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-cpan-perl-releases
perl -MCPAN::Perl::Releases=perl_tarballs,perl_versions <<'PERL'
use strict;
use warnings;
my $tarballs = perl_tarballs('5.14.0');
die "wrong release mapping" unless $tarballs->{'tar.gz'} eq 'J/JE/JESSE/perl-5.14.0.tar.gz';
die "missing version" unless grep { $_ eq '5.6.1' } perl_versions();
die "unexpected version" unless $CPAN::Perl::Releases::VERSION eq '5.20261022';
print "ok 1 - installed release mapping and version enumeration\n";
PERL
