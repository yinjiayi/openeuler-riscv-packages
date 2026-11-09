#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libio-interactive-perl
unset PERL5LIB PERLLIB PERL5OPT
/usr/bin/perl - <<'PERL'
use strict;
use warnings;
use IO::Interactive qw(interactive is_interactive);

die "expected non-terminal input" if is_interactive();
my $sink = interactive();
die "expected a separate non-interactive sink"
    unless defined fileno($sink) && fileno($sink) != fileno(STDOUT);
{
    # Upstream's sink is the read end of its internal pipe.
    no warnings 'io';
    print {$sink} "non-terminal text must not be emitted\n";
}
print "installed non-interactive sink passed\n";
PERL
