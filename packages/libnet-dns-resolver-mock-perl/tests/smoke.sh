#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Net-DNS-Resolver-Mock
rpm -q --whatprovides 'perl(Net::DNS::Resolver::Mock)'
perl -MNet::DNS::Resolver::Mock -e '
  die "wrong version\n" unless $Net::DNS::Resolver::Mock::VERSION eq "1.20230216";
  my $resolver = Net::DNS::Resolver::Mock->new;
  $resolver->zonefile_parse("example.test 3600 A 192.0.2.25\n");
  my $positive = $resolver->query("example.test", "A");
  my @answers = $positive->answer;
  die "positive mock lookup failed\n"
    unless @answers == 1 && $answers[0]->rdatastr eq "192.0.2.25";
  my $negative = $resolver->query("missing.example.test", "A");
  die "negative mock lookup failed\n" if defined $negative;
'
