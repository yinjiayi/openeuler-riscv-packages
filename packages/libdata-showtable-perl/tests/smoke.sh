#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-ShowTable
rpm -q --whatprovides 'perl(Data::ShowTable)'
perl -MData::ShowTable -e '
  die "unexpected Data::ShowTable version\n"
    unless $Data::ShowTable::VERSION eq "4.6";
'
command -v showtable
rendered=$(printf 'Name\tAge\nAda\t37\n' | showtable -titles -simple)
[[ "$rendered" == *Name* && "$rendered" == *Ada* && "$rendered" == *37* ]] || {
  printf '%s\n' 'showtable command did not render installed input' >&2
  exit 1
}
