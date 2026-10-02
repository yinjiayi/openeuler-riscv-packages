#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Class-ErrorHandler
rpm -q --whatprovides 'perl(Class::ErrorHandler)'
perl -MClass::ErrorHandler -e '
  die "wrong installed version\n" unless $Class::ErrorHandler::VERSION eq "0.04";
  { package Child; our @ISA = ("Class::ErrorHandler"); }
  my $child = bless {}, "Child";
  die "object error return changed\n" if defined $child->error("object failure");
  die "object error missing\n" unless $child->errstr eq "object failure";
  die "class error return changed\n" if defined Child->error("class failure");
  die "class error missing\n" unless Child->errstr eq "class failure";
  die "class/object state aliased\n" unless $child->errstr eq "object failure";
'
