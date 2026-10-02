#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Net-LDAP-SID
rpm -q --whatprovides 'perl(Net::LDAP::SID)'
perl -MNet::LDAP::SID -e '
  die "unexpected Net::LDAP::SID version\n" unless $Net::LDAP::SID::VERSION eq "0.001";
  my $text = "S-1-5-21-2127521184-1604012920-1887927527-72713";
  my $from_text = Net::LDAP::SID->new($text);
  die "text SID mismatch\n" unless $from_text->as_string eq $text;
  my $from_binary = Net::LDAP::SID->new($from_text->as_binary);
  die "binary SID round-trip mismatch\n"
    unless $from_binary->as_string eq $text
      && $from_binary->as_binary eq $from_text->as_binary;
'
