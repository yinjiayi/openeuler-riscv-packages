#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libtest-manifest-perl
unset PERL5LIB PERLLIB PERL5OPT
fixture=$(mktemp -d)
trap 'rm -f -- "$fixture"/t/{test_manifest,include.txt,first.t,second.t,high.t}; rmdir -- "$fixture"/t "$fixture"' EXIT
/usr/bin/perl -MTest::Manifest - "$fixture" <<'PERL'
use strict;
use warnings;

my ($dir) = @ARGV;
chdir $dir or die "chdir $dir: $!";
mkdir 't' or die "mkdir t: $!";
my %files = (
    't/test_manifest' => "second.t 1\n;include t/include.txt\n",
    't/include.txt'   => "first.t 1\nhigh.t 3\n",
    't/first.t'       => "1;\n",
    't/second.t'      => "1;\n",
    't/high.t'        => "1;\n",
);
for my $file (sort keys %files) {
    open my $fh, '>', $file or die "open $file: $!";
    print {$fh} $files{$file} or die "write $file: $!";
    close $fh or die "close $file: $!";
}
my @tests = Test::Manifest::get_t_files(1);
die "unexpected tests: @tests" unless join(',', @tests) eq 't/second.t,t/first.t';
chdir '/' or die "chdir /: $!";
print "installed manifest include and level order passed\n";
PERL
