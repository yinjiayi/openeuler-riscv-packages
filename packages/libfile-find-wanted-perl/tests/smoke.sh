#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Find-Wanted
rpm -q --whatprovides 'perl(File::Find::Wanted)'
perl -MFile::Temp=tempdir -MFile::Find::Wanted=find_wanted -e '
  die "unexpected File::Find::Wanted version\n"
    unless $File::Find::Wanted::VERSION eq "1.00";
  my $dir = tempdir(CLEANUP => 1);
  for my $name (qw(keep.txt skip.log)) {
    open my $out, ">", "$dir/$name" or die $!;
    print {$out} "$name\n";
    close $out or die $!;
  }
  my @found = find_wanted(sub { -f && /[.]txt$/ }, $dir);
  @found == 1 && $found[0] eq "$dir/keep.txt"
    or die "file predicate did not select only the text fixture\n";
'
