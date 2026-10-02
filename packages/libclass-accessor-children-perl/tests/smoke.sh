#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Class-Accessor-Children
rpm -q --whatprovides 'perl(Class::Accessor::Children)'
rpm -q --whatprovides 'perl(Class::Accessor::Children::Fast)'
perl -MClass::Accessor::Children -MClass::Accessor::Children::Fast -e '
  die "wrong installed version\n"
    unless $Class::Accessor::Children::VERSION eq "0.02"
      && $Class::Accessor::Children::Fast::VERSION eq "0.02";
  { package Normal; our @ISA = ("Class::Accessor::Children");
    __PACKAGE__->mk_child_accessors( Kid => [qw(name)] ); }
  { package Fast; our @ISA = ("Class::Accessor::Children::Fast");
    __PACKAGE__->mk_child_accessors( Kid => [qw(name)] ); }
  my $normal = Normal::Kid->new({ name => "normal" });
  my $fast = Fast::Kid->new({ name => "fast" });
  die "normal child accessor failed\n" unless $normal->name eq "normal";
  die "fast child accessor failed\n" unless $fast->name eq "fast";
'
