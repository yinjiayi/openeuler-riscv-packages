#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Array-Group
perl -MArray::Group=:all -e '
  die "unexpected version\n" unless $Array::Group::VERSION eq "4.2";
  my @rows = ngroup(2, [1 .. 5]);
  die "row grouping mismatch\n"
    unless join(";", map { join(",", @$_) } @rows) eq "1,2;3,4;5";
  my @columns = dissect(2, [1 .. 5]);
  die "interleaved grouping mismatch\n"
    unless join(";", map { join(",", @$_) } @columns) eq "1,3,5;2,4";
'
