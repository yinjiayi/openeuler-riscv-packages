#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-Interpolate-Named
rpm -q --whatprovides 'perl(String::Interpolate::Named)'
perl -MString::Interpolate::Named -e '
  die "unexpected version\n"
    unless $String::Interpolate::Named::VERSION eq "1.06";
  my $ctl = { args => { fn => "Johann", ln => "Bach" } };
  die "named interpolation mismatch\n"
    unless interpolate($ctl, "The famous %{fn} %{ln}.")
       eq "The famous Johann Bach.";
'
