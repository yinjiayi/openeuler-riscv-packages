#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-Glob-Permute
rpm -q --whatprovides 'perl(String::Glob::Permute)'
perl -MString::Glob::Permute=string_glob_permute -e '
  die "unexpected version\n" unless $String::Glob::Permute::VERSION eq "0.01";
  my @expanded = string_glob_permute("node{a,b}[1-2]");
  die "permutation mismatch\n"
    unless join(",", @expanded) eq "nodea1,nodeb1,nodea2,nodeb2";
  die "single literal mismatch\n"
    unless join(",", string_glob_permute("literal")) eq "literal";
'
