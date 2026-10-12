#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-pushd
rpm -q --whatprovides 'perl(File::pushd)'
perl -MFile::pushd=pushd -MCwd=getcwd -e '
  die "unexpected File::pushd version\n" unless $File::pushd::VERSION eq "1.016";
  my $original = getcwd();
  {
    my $guard = pushd("/");
    die "pushd did not change directory\n" unless getcwd() eq "/";
  }
  die "pushd did not restore directory\n" unless getcwd() eq $original;
'
