#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Slurp
rpm -q --whatprovides 'perl(File::Slurp)'
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
perl -MFile::Slurp=write_file,read_file -e '
  die "unexpected File::Slurp version\n" unless $File::Slurp::VERSION eq "9999.32";
  write_file($ARGV[0], "RVA23\n") or die "write failed\n";
  die "round-trip failed\n" unless read_file($ARGV[0]) eq "RVA23\n";
' "$smoke_dir/message.txt"
