#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libperl-version-perl
perl -MPerl::Version -e '
    die "unexpected installed version" unless Perl::Version->VERSION eq "1.019";
    my $v = Perl::Version->new("1.2.3");
    die "bad stringification" unless $v->stringify eq "1.2.3";
    die "bad version ordering" unless $v < Perl::Version->new("1.2.4");
'
help=$(perl-reversion --help)
[[ $help == *'perl-reversion [options] [file ...]'* ]]
