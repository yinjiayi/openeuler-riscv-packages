#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Inplace
rpm -q --whatprovides 'perl(File::Inplace)'
perl -MFile::Temp=tempdir -MFile::Inplace -e '
  die "unexpected File::Inplace version\n"
    unless $File::Inplace::VERSION eq "0.20";
  my $dir = tempdir(CLEANUP => 1);
  my $path = "$dir/input.txt";
  open my $out, ">", $path or die $!;
  print {$out} "a\nb\n";
  close $out or die $!;
  my $edit = File::Inplace->new(file => $path, suffix => ".bak");
  while ($edit->has_lines) {
    my $line = $edit->next_line;
    $edit->replace_line("c") if $line eq "b";
  }
  $edit->commit;
  open my $changed, "<", $path or die $!;
  my $body = do { local $/; <$changed> };
  close $changed or die $!;
  open my $backup, "<", "$path.bak" or die $!;
  my $original = do { local $/; <$backup> };
  close $backup or die $!;
  $body eq "a\nc\n" && $original eq "a\nb\n"
    or die "edit or backup content differs\n";
'
