#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Array-RefElem
perl -MArray::RefElem=av_store -e '
  die "unexpected version\n" unless $Array::RefElem::VERSION eq "1.00";
  my $value = "before";
  my @array = ("unused");
  av_store(@array, 0, $value);
  $value = "after";
  die "array alias failed\n" unless $array[0] eq "after";
'
