#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-MethodProxy
rpm -q --whatprovides 'perl(Data::MethodProxy)'
rpm -q --whatprovides 'perl(Config::MethodProxy)'
perl -MData::MethodProxy -MConfig::MethodProxy=apply_method_proxies -e '
  die "unexpected Data::MethodProxy version\n"
    unless $Data::MethodProxy::VERSION eq "0.05";
  package My::MethodProxy::Smoke;
  sub half { my ($class, $value) = @_; return $value / 2; }
  $INC{"My/MethodProxy/Smoke.pm"} = 1;
  package main;
  my $result = Data::MethodProxy->new->render({
    value => [q($proxy), "My::MethodProxy::Smoke", "half", 6],
  });
  die "Data::MethodProxy render mismatch\n" unless $result->{value} == 3;
  my $compat = apply_method_proxies({
    value => [q($proxy), "My::MethodProxy::Smoke", "half", 8],
  });
  die "Config::MethodProxy compatibility mismatch\n"
    unless $compat->{value} == 4;
'
