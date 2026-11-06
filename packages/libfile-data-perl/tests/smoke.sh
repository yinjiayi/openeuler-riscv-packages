#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Data
rpm -q --whatprovides 'perl(File::Data)'
perl -MFile::Data -MFile::Temp=tempdir -e '
  die "unexpected version\n" unless $File::Data::VERSION eq "1.20";
  my $directory = tempdir(CLEANUP => 1);
  my $path = "$directory/payload";
  open my $created, ">", $path or die $!;
  close $created;
  my $count = File::Data->new($path)->WRITE("alpha\n", "beta\n");
  die "write failed\n" unless $count == 2;
  my @lines = File::Data->new($path, "ro")->READ(".+");
  die "readback failed\n" unless join("", @lines) eq "alpha\nbeta\n";
'
