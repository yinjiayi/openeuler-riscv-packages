#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Net-DHCPv6-DUID-Parser
rpm -q --whatprovides 'perl(Net::DHCPv6::DUID::Parser)'
perl -MNet::DHCPv6::DUID::Parser -e '
  die "unexpected parser version\n"
    unless $Net::DHCPv6::DUID::Parser::VERSION eq "1.01";
  my $parser = Net::DHCPv6::DUID::Parser->new(decode => "hex", warnings => 0);
  die "DUID-LLT decode failed\n"
    unless $parser->decode("000100011286F55C0007E90F2FEE") && $parser->type == 1;
  die "DUID-EN decode failed\n"
    unless $parser->decode("0002000000090CC084D303000912") && $parser->type == 2;
  die "DUID-LL decode failed\n"
    unless $parser->decode("000300010004ED9F7522") && $parser->type == 3;
  die "malformed DUID accepted\n" if defined $parser->decode("foo");
'
