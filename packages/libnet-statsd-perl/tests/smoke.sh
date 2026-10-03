#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Net-Statsd
rpm -q --whatprovides 'perl(Net::Statsd)'
perl -MNet::Statsd -MIO::Socket::INET -e '
  die "unexpected Net::Statsd version\n" unless $Net::Statsd::VERSION eq "0.13";
  my $server = IO::Socket::INET->new(
    LocalAddr => "127.0.0.1", LocalPort => 0, Proto => "udp"
  ) or die "localhost UDP bind failed: $!\n";
  $Net::Statsd::HOST = "127.0.0.1";
  $Net::Statsd::PORT = $server->sockport;
  Net::Statsd::increment("ci.counter");
  local $SIG{ALRM} = sub { die "localhost UDP receive timed out\n" };
  alarm 5;
  $server->recv(my $packet, 1024);
  alarm 0;
  die "unexpected UDP metric: $packet\n" unless $packet eq "ci.counter:1|c";
  my $rejected = eval { Net::Statsd::increment("bad\nname"); 1 };
  die "metric injection was accepted\n" if $rejected;
  die "wrong metric rejection\n" unless $@ =~ /malformed metric name/;
'
