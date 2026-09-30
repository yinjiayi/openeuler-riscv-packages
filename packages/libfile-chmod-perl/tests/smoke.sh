#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-chmod
rpm -q --whatprovides 'perl(File::chmod)'
test_file="$(mktemp)"
trap 'rm -f -- "$test_file"' EXIT
perl -MFile::chmod=chmod,getmod -e '
  die "unexpected File::chmod version\n"
    unless $File::chmod::VERSION eq "0.42";
  $File::chmod::UMASK = 0;
  my $path = $ARGV[0];
  chmod("u+x", $path) or die "symbolic chmod failed\n";
  (getmod($path) & 0100) or die "owner executable bit missing\n";
' "$test_file"
