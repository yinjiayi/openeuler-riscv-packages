#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-Validate-Type
rpm -q --whatprovides 'perl(Data::Validate::Type)'
perl -MData::Validate::Type=:boolean_tests -e '
  die "unexpected Data::Validate::Type version\n"
    unless $Data::Validate::Type::VERSION eq "1.6.0";
  die "installed string check failed\n"
    unless is_string("hello") && !is_string([]);
  die "installed number check failed\n"
    unless is_number(42) && !is_number("not a number");
'
