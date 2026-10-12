#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-URI-Query
rpm -q --whatprovides 'perl(URI::Query)'
perl -MURI::Query -e '
  die "wrong URI::Query version\n" unless $URI::Query::VERSION eq "0.16";
  my $query = URI::Query->new("z=1&a=hello%20world");
  die "query canonicalization failed\n"
    unless $query->stringify eq "a=hello%20world&z=1";
  die "clone dependency or behavior failed\n"
    unless $query->clone->strip("z")->stringify eq "a=hello%20world";
'
