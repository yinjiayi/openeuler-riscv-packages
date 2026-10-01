#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-chdir
rpm -q --whatprovides 'perl(File::chdir)'
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
perl -MFile::chdir -MCwd -e '
  die "unexpected File::chdir version\n" unless $File::chdir::VERSION eq "0.1011";
  my $before = Cwd::getcwd();
  {
    local $CWD = $ARGV[0];
    die "local directory change failed\n" unless Cwd::getcwd() eq $ARGV[0];
  }
  die "original directory not restored\n" unless Cwd::getcwd() eq $before;
' "$smoke_dir"
