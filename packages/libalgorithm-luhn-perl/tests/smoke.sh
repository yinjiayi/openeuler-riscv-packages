#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Algorithm-LUHN
rpm -q --whatprovides 'perl(Algorithm::LUHN)'
perl -MAlgorithm::LUHN=check_digit,is_valid -e '
  die "unexpected Algorithm::LUHN version\n"
    unless $Algorithm::LUHN::VERSION eq "1.02";
  die "unexpected Luhn check digit\n"
    unless check_digit("4992739871") eq "6";
  die "valid Luhn identifier rejected\n"
    unless is_valid("49927398716");
  die "invalid Luhn identifier accepted\n"
    if is_valid("49927398717");
'
