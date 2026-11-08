#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-tie-simple
perl -MTie::Simple -e '
use strict; use warnings;
die "version" unless $Tie::Simple::VERSION eq "1.04";
my $value = "initial";
tie my $tied, "Tie::Simple", \$value,
  FETCH => sub { ${$_[0]} },
  STORE => sub { ${$_[0]} = $_[1] };
die "FETCH" unless $tied eq "initial";
$tied = "updated";
die "STORE" unless $value eq "updated" && $tied eq "updated";
print "Tie::Simple installed FETCH/STORE passed\n";
'
