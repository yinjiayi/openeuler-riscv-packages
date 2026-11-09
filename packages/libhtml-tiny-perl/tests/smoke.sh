#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libhtml-tiny-perl
unset PERL5LIB PERLLIB PERL5OPT
/usr/bin/perl - <<'PERL'
use strict;
use warnings;
use HTML::Tiny;

my $html = HTML::Tiny->new;
my $output = $html->tag('b', $html->entity_encode('<&'));
die "wrong entity-encoded tag" unless $output eq '<b>&lt;&amp;</b>';
die "wrong query encoding" unless $html->query_encode({b => 1, a => 'x y'}) eq 'a=x+y&b=1';
print "installed HTML escaping and query encoding passed\n";
PERL
