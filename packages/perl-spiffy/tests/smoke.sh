#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Spiffy
rpm -q --whatprovides 'perl(Spiffy)'
perl -e '
  package AuditSpiffy;
  use Spiffy -base;
  field "answer";
  package main;
  my $object = AuditSpiffy->new(answer => 23);
  die "unexpected Spiffy version\n" unless $Spiffy::VERSION eq "0.46";
  die "Spiffy field round-trip failed\n" unless $object->answer == 23;
  require Spiffy::mixin;
'
