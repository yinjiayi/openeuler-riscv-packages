#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Class-Container
rpm -q --whatprovides 'perl(Class::Container)'
perl -MClass::Container -e '
  die "wrong installed version\n" unless $Class::Container::VERSION eq "0.13";
  { package OEParent; our @ISA = ("Class::Container"); }
  { package OEChild; our @ISA = ("Class::Container"); }
  OEParent->valid_params(child => {isa => "OEChild"});
  OEParent->contained_objects(child => "OEChild");
  my $parent = OEParent->new;
  die "contained child not built\n" unless ref($parent->{child}) eq "OEChild";
  die "container back-reference missing\n" unless $parent->{child}->container == $parent;
'
