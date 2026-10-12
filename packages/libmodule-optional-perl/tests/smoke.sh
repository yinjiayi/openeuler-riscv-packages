#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Module-Optional
rpm -q --whatprovides 'perl(Module::Optional)'
rpm -q --whatprovides 'perl(Params::Validate::Dummy)'
perl -MParams::Validate::Dummy -e '
  require Module::Optional;
  die "wrong Module::Optional version\n"
    unless $Module::Optional::VERSION eq "0.03";
  my @input = ("alpha", "beta");
  my @values = Params::Validate::Dummy::validate_pos(@input, 1, 1);
  die "dummy fallback changed\n"
    unless @values == 2 && $values[0] eq "alpha" && $values[1] eq "beta";
'
