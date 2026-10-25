#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Net-IPTrie
rpm -q --whatprovides 'perl(Net::IPTrie)'
perl -MNet::IPTrie -e '
  die "unexpected Net::IPTrie version\n" unless $Net::IPTrie::VERSION eq "0.7";
  my $v4 = Net::IPTrie->new(version => 4);
  my $root = $v4->add(address => "0.0.0.0", prefix => 0);
  my $network = $v4->add(address => "10.0.0.0", prefix => 8);
  die "IPv4 closest-prefix mismatch\n"
    unless $v4->find(address => "10.1.2.3")->address eq "10.0.0.0";
  die "IPv4 parent mismatch\n" unless $network->parent->address eq $root->address;
  my $v6 = Net::IPTrie->new(version => 6);
  $v6->add(address => "2001:db8::", prefix => 32);
  die "IPv6 closest-prefix mismatch\n"
    unless $v6->find(address => "2001:db8::1")->address eq "2001:db8::";
'
