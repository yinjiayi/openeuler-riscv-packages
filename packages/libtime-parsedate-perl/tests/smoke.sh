#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libtime-parsedate-perl
unset PERL5LIB PERLLIB PERL5OPT
export TZ=PST8PDT LC_ALL=C
/usr/bin/perl -MTime::ParseDate - <<'PERL'
use strict;
use warnings;

my $summer = parsedate('2000/07/04 12:00:00', WHOLE => 1);
my $winter = parsedate('1969/12/31 16:00:00', WHOLE => 1);
die "incorrect summer epoch" unless defined($summer) && $summer == 962737200;
die "incorrect winter epoch" unless defined($winter) && $winter == 0;
print "installed summer/winter epoch conversion passed\n";
PERL
