#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-SearchPath
rpm -q --whatprovides 'perl(File::SearchPath)'
perl -MFile::Temp=tempdir -MFile::SearchPath -e '
  die "unexpected File::SearchPath version\n"
    unless $File::SearchPath::VERSION eq "0.07";
  my $dir = tempdir(CLEANUP => 1);
  my $path = "$dir/wanted.dat";
  open my $fh, ">", $path or die $!;
  print {$fh} "fixture\n";
  close $fh or die $!;
  local $ENV{CODEX_SMOKE_PATH} = $dir;
  my $found = File::SearchPath::searchpath(
    "wanted.dat", env => "CODEX_SMOKE_PATH"
  );
  defined($found) && $found eq $path or die "path search mismatch\n";
  File::SearchPath::searchpath("absent.dat", env => "CODEX_SMOKE_PATH")
    and die "nonexistent file was reported\n";
'
