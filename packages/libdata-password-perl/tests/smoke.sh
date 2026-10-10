#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-Password
rpm -q --whatprovides 'perl(Data::Password)'
perl -MData::Password=IsBadPassword -e '
  die "unexpected Data::Password version\n"
    unless $Data::Password::VERSION eq "1.12";
  my $weak = IsBadPassword("qwerTy");
  die "expected sequence rejection\n"
    unless defined($weak) && length($weak);
  my $accepted = IsBadPassword("xxxZZZ");
  die "unexpected rejection\n"
    if defined($accepted) && length($accepted);
'
