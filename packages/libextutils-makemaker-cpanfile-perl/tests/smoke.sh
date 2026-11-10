#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-extutils-makemaker-cpanfile
scratch=$(mktemp -d)
trap 'rm -f -- "$scratch/Makefile.PL" "$scratch/cpanfile" "$scratch/Makefile" "$scratch/MYMETA.json" "$scratch/MYMETA.yml"; rmdir -- "$scratch"' EXIT
cd -- "$scratch"
cat > Makefile.PL <<'PERL'
use strict;
use warnings;
use ExtUtils::MakeMaker::CPANfile;
WriteMakefile(NAME => 'Example::CPANfileSmoke', VERSION => '0.01');
PERL
cat > cpanfile <<'PERL'
requires 'strict';
on test => sub { requires 'Test::More', '0.88'; };
PERL
perl Makefile.PL
perl -MCPAN::Meta -e '
    my $p = CPAN::Meta->load_file("MYMETA.json")->prereqs;
    die "missing runtime phase" unless $p->{runtime}{requires}{strict} eq "0";
    die "missing test phase" unless $p->{test}{requires}{"Test::More"} eq "0.88";
    die "missing configure phase" unless $p->{configure}{requires}{"ExtUtils::MakeMaker::CPANfile"} eq "0.11";
    print "ok 1 - installed CPANfile integration preserves dependency phases\n";
'
