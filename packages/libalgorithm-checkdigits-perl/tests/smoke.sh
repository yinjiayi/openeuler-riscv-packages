#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Algorithm-CheckDigits
rpm -q --whatprovides 'perl(Algorithm::CheckDigits)'
perl -MAlgorithm::CheckDigits -e '
  my $imei = CheckDigits("IMEI");
  $imei->is_valid("260531793113837") or die "valid IMEI rejected\n";
  $imei->is_valid("260531793113838") and die "invalid IMEI accepted\n";
'
output=$(checkdigits.pl --algorithm=IMEI check 260531793113837 260531793113838)
test "$output" = $'valid\nnot valid'
