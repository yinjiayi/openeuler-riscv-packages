#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
task_dir=$(mktemp -d)
trap 'rm -rf -- "$task_dir"' EXIT
perl -MData::Section::Simple - "$task_dir/sample.pl" <<'PERL'
use strict;
use warnings;
open my $out, '>', $ARGV[0] or die $!;
print {$out} <<'PROGRAM';
use strict;
use warnings;
use Data::Section::Simple qw(get_data_section);
die "version mismatch\n" unless $Data::Section::Simple::VERSION eq '0.07';
my $all = get_data_section();
die "section names\n" unless join(',', sort keys %$all) eq 'greeting,number';
die "section value\n" unless get_data_section('greeting') eq "hello RVA23\n\n";
die "missing value\n" if defined get_data_section('missing');
my $reader = Data::Section::Simple->new('main');
die "object read\n" unless $reader->get_data_section('number') eq "23\n";
print "Data::Section::Simple functional and object reads passed\n";
__DATA__
@@ greeting
hello RVA23

@@ number
23
PROGRAM
close $out or die $!;
PERL
perl "$task_dir/sample.pl"
