#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Math-Base36
rpm -q --whatprovides 'perl(Math::Base36)'
perl -MMath::Base36=:all -e '
  die "unexpected version\n" unless $Math::Base36::VERSION eq "0.14";
  die "unexpected encoding\n" unless encode_base36(1295) eq "ZZ";
  die "unexpected decoding\n" unless decode_base36("ZZ") == 1295;
  die "unexpected padding\n" unless encode_base36(36, 4) eq "0010";
'
