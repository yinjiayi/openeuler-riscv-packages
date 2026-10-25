#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Devel-CheckBin
rpm -q --whatprovides 'perl(Devel::CheckBin)'
perl -MDevel::CheckBin -e '
  die "wrong installed version\n" unless $Devel::CheckBin::VERSION eq "0.04";
  my $ls = Devel::CheckBin::can_run("ls");
  die "installed ls not found\n" unless defined $ls && -x $ls;
  die "nonexistent command found\n" if Devel::CheckBin::can_run("codex_definitely_missing_command_96255");
  die "positive check_bin failed\n" unless Devel::CheckBin::check_bin("ls");
'
