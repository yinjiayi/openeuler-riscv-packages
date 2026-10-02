#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Net-LDAP-FilterBuilder
rpm -q --whatprovides 'perl(Net::LDAP::FilterBuilder)'
perl -MNet::LDAP::FilterBuilder -e '
  die "unexpected version\n" unless $Net::LDAP::FilterBuilder::VERSION eq "1.200002";
  my $escaped = Net::LDAP::FilterBuilder->new(sn => "foo*bar");
  die "wildcard not escaped\n" unless "$escaped" eq q{(sn=foo\*bar)};
  my $combined = Net::LDAP::FilterBuilder->new(sn => "Jones")
    ->and(givenName => "David");
  die "and expression mismatch\n"
    unless "$combined" eq q{(&(sn=Jones)(givenName=David))};
  $combined->not;
  die "not expression mismatch\n"
    unless "$combined" eq q{(!(&(sn=Jones)(givenName=David)))};
'
