#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-DHCPLeases
rpm -q --whatprovides 'perl(Text::DHCPLeases)'
rpm -q --whatprovides 'perl(Text::DHCPLeases::Object)'
rpm -q --whatprovides 'perl(Text::DHCPLeases::Object::Iterator)'
perl -MText::DHCPLeases -MFile::Temp=tempfile -e '
  die "unexpected Text::DHCPLeases version\n"
    unless $Text::DHCPLeases::VERSION eq "1.0";
  my ($fh, $path) = tempfile();
  print {$fh} "lease 192.0.2.1 {\n  binding state active;\n}\n";
  close $fh or die "closing lease fixture failed: $!\n";
  my $leases = Text::DHCPLeases->new(file => $path);
  unlink $path;
  die "lease parsing or iterator count mismatch\n"
    unless $leases->get_objects->count == 1;
'
