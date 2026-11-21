#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libregexp-grammars-perl
unset PERL5LIB PERLLIB PERL5OPT
/usr/bin/perl -MRegexp::Grammars - <<'PERL'
use strict;
use warnings;

my $parser = qr{\A <n> \z <token: n> \d+ }x;
die "expected a structured number capture" unless "123" =~ $parser && $/{n} eq "123";
die "unexpected acceptance of trailing characters" if "12x" =~ $parser;
print "installed grammar capture and rejection passed\n";
PERL
