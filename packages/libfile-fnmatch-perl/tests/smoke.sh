#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-FnMatch
rpm -q --whatprovides 'perl(File::FnMatch)'
perl -MFile::FnMatch=:fnmatch -e '
  die "unexpected File::FnMatch version\n"
    unless $File::FnMatch::VERSION eq "0.02";
  fnmatch("*.txt", "example.txt") or die "simple match failed\n";
  !fnmatch("*.txt", "example.log") or die "extension mismatch accepted\n";
  !fnmatch("*.txt", "dir/example.txt", FNM_PATHNAME)
    or die "pathname flag did not constrain wildcard\n";
'
