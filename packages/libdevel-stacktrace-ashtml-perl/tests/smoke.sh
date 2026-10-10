#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Devel-StackTrace-AsHTML
rpm -q --whatprovides 'perl(Devel::StackTrace::AsHTML)'
perl -MDevel::StackTrace::AsHTML -e '
  die "wrong installed version\n" unless $Devel::StackTrace::AsHTML::VERSION eq "0.15";
  my $trace = Devel::StackTrace->new(message => "\x{30c6}&<>");
  my $html = $trace->as_html;
  die "HTML heading missing\n" unless $html =~ /Error trace/;
  die "Unicode escaping missing\n" unless $html =~ /&#12486;/;
  die "ampersand escaping missing\n" unless $html =~ /&amp;/;
  die "angle escaping missing\n" unless $html =~ /&lt;&gt;/;
  print "installed HTML rendering and escaping OK\n";
'
