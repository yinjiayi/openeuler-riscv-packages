#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libxml-writer-string-perl
unset PERL5LIB PERLLIB PERL5OPT
/usr/bin/perl - <<'PERL'
use strict;
use warnings;
use XML::Writer;
use XML::Writer::String;

my $output = XML::Writer::String->new;
my $writer = XML::Writer->new(OUTPUT => $output);
$writer->dataElement('x', 'a<b&');
$writer->end;
die "wrong escaped XML output" unless $output->value eq "<x>a&lt;b&amp;</x>\n";
print "installed XML writer escaped output passed\n";
PERL
