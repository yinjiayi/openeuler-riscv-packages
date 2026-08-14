#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Config-Simple
perl -MConfig::Simple -e '
  die "unexpected Config::Simple version\n"
    unless $Config::Simple::VERSION eq "4.59";
  my $cfg = Config::Simple->new(syntax => "ini");
  $cfg->param("target.arch", "riscv64");
  die "round-trip failed\n"
    unless $cfg->param("target.arch") eq "riscv64";
'
