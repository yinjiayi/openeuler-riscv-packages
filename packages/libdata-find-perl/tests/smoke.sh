#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-Find
rpm -q --whatprovides 'perl(Data::Find)'
perl -MData::Find=dfind -e '
  die "unexpected Data::Find version\n" unless $Data::Find::VERSION eq "0.03";
  my @paths = dfind({ a => [1, 2], b => 3 }, 2);
  die "nested search mismatch\n"
    unless @paths == 1 && $paths[0] eq "{a}[1]";
'
