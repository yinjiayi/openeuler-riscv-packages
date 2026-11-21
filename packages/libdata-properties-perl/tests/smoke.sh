#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-data-properties
perl -MData::Properties <<'PERL'
use strict;
use warnings;
my $input = <<'PROPERTIES';
Truth1 = Beauty
fruits apple, banana, pear, \
       cantaloupe, watermelon, \
       kiwi, mango
cheeses:
PROPERTIES
my $p = Data::Properties->new;
open my $file, '<', \$input or die $!;
$p->load($file) or die "load failed";
die "wrong continuation" unless $p->get_property('fruits') eq 'apple, banana, pear, cantaloupe, watermelon, kiwi, mango';
die "wrong empty value" unless $p->get_property('cheeses') eq '';
$p->set_property('Truth1', 'Retained');
my $buffer = '';
open my $output, '>', \$buffer or die $!;
$p->store($output) or die "store failed";
close $output or die $!;
open my $written, '<', \$buffer or die $!;
my $q = Data::Properties->new;
$q->load($written) or die "reload failed";
die "wrong round trip" unless $q->get_property('Truth1') eq 'Retained';
print "ok 1 - installed Data::Properties parses continuation, preserves empty values and round-trips updated properties\n";
PERL
