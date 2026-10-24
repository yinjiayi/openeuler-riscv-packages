#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-Censor
rpm -q --whatprovides 'perl(Data::Censor)'
perl -MData::Censor -MClone -e '
  die "wrong installed version\n" unless $Data::Censor::VERSION eq "0.04";
  my $plain = {password => "secret", profile => {pan => "1234567890123"}};
  my $censor = Data::Censor->new;
  my $count = $censor->censor($plain);
  die "in-place censor failed\n" unless $count == 2 && $plain->{password} ne "secret" && $plain->{profile}{pan} ne "1234567890123";
  my $source = {password => "secret", profile => {pan => "1234567890123"}};
  my $copy = Data::Censor->clone_and_censor($source);
  die "clone censor failed\n" unless $copy->{password} ne "secret" && $copy->{profile}{pan} ne "1234567890123";
  die "source mutated\n" unless $source->{password} eq "secret" && $source->{profile}{pan} eq "1234567890123";
  print "installed in-place and clone censor OK\n";
'
