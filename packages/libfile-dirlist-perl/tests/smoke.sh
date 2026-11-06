#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-DirList
rpm -q --whatprovides 'perl(File::DirList)'
perl -MFile::Temp=tempdir -MFile::DirList -e '
  die "unexpected File::DirList version\n"
    unless $File::DirList::VERSION eq "0.05";
  my $dir = tempdir(CLEANUP => 1);
  for my $name (qw(b.txt a.txt)) {
    open my $fh, ">", "$dir/$name" or die $!;
    print {$fh} "$name\n";
    close $fh or die $!;
  }
  my $entries = File::DirList::list($dir, "n", 1, 1, 0);
  die "listing failed\n" unless defined $entries;
  my @names = map { $_->[13] } grep { $_->[13] ne ".." } @$entries;
  die "unexpected sorted listing: @names\n"
    unless @names == 2 && $names[0] eq "a.txt" && $names[1] eq "b.txt";
'
