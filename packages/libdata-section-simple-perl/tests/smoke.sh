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
# Audit installed origin grant/provenance, not just repository-side notices.
license_dir=/usr/share/licenses/perl-Data-Section-Simple
printf '%s  %s\n' \
  363a7a9263d30474b76654efd142831934c71a4ec9be858465d93dbce3d9b881 "$license_dir/LICENSE" \
  685e534b60d4e2b4fbb1a259a83b5a86e877a919bbb9efc95994276f706a3a71 "$license_dir/LICENSE.Mojo" \
  9b1bcdbe80a754a21699892287bbf9a8920fa62e64a0086a2c240887a125e64e "$license_dir/MOJO-PROVENANCE" \
  | sha256sum --check
module_path=$(perl -MData::Section::Simple -e 'print $INC{"Data/Section/Simple.pm"}')
printf '%s  %s\n' \
  7fd0b65746bfddd3bbc870b36968ac613311e918bdb300ad2efdd961ffca2dcd "$module_path" \
  | sha256sum --check
echo 'Original Perl grant, exact Mojo license/provenance and unchanged module bytes verified'
