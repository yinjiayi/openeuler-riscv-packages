#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-Binary
rpm -q --whatprovides 'perl(Data::Binary)'
perl -MData::Binary=is_text,is_binary -e '
  die "unexpected Data::Binary version\n" unless $Data::Binary::VERSION eq "0.01";
  die "text classification failed\n" unless is_text("ordinary text");
  die "binary classification failed\n" unless is_binary("binary\0payload");
'
