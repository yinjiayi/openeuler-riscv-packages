#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Class-C3-Adopt-NEXT
rpm -q --whatprovides 'perl(Class::C3::Adopt::NEXT)'
perl -MClass::C3::Adopt::NEXT -e '
  die "wrong installed version\n" unless $Class::C3::Adopt::NEXT::VERSION eq "0.14";
  { package OEBase; sub value { 42 } }
  { package OEChild; our @ISA = ("OEBase"); use Class::C3::Adopt::NEXT "-no_warn"; sub value { shift->NEXT::value } }
  my $object = bless {}, "OEChild";
  die "installed NEXT dispatch failed\n" unless $object->value == 42;
'
