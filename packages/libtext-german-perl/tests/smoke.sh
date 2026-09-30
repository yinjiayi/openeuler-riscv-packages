#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-German
perl -MText::German -e '
  die "unexpected version\n" unless $Text::German::VERSION eq "0.06";
  die "word reduction mismatch\n"
    unless Text::German::reduce("Jahre") eq "Jahr";
  die "cached reduction mismatch\n"
    unless Text::German::cache_reduce("Jahre") eq "Jahr";
'
