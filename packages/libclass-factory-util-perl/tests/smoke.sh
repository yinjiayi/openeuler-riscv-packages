#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Class-Factory-Util
rpm -q --whatprovides 'perl(Class::Factory::Util)'
perl -MFile::Spec -e '
  { package File::Spec; use Class::Factory::Util; }
  die "wrong installed version\n" unless $Class::Factory::Util::VERSION eq "1.7";
  my @children = File::Spec->subclasses;
  die "Unix subclass missing\n" unless grep { $_ eq "Unix" } @children;
  die "Win32 subclass missing\n" unless grep { $_ eq "Win32" } @children;
'
