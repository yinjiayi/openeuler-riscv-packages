#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Copy-Recursive
rpm -q --whatprovides 'perl(File::Copy::Recursive)'
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
perl -MFile::Copy::Recursive=dircopy -e '
  die "unexpected File::Copy::Recursive version\n"
    unless $File::Copy::Recursive::VERSION eq "0.45";
  mkdir "$ARGV[0]/source" or die "mkdir source: $!\n";
  open my $out, ">", "$ARGV[0]/source/message.txt" or die "open: $!\n";
  print {$out} "RVA23\n" or die "write: $!\n";
  close $out or die "close: $!\n";
  dircopy("$ARGV[0]/source", "$ARGV[0]/copy") or die "dircopy: $!\n";
  open my $in, "<", "$ARGV[0]/copy/message.txt" or die "copied file: $!\n";
  my $text = <$in>;
  die "copied content mismatch\n" unless $text eq "RVA23\n";
' "$smoke_dir"
