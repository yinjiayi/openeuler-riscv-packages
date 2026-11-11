#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Text-Autoformat
rpm -q --whatprovides 'perl(Text::Autoformat)'
perl -MText::Autoformat=autoformat -e '
  die "unexpected version\n" unless $Text::Autoformat::VERSION eq "1.75";
  die "empty input mismatch\n" unless autoformat("") eq "";
'
