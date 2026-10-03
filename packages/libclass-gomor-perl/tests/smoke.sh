#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Class-Gomor
rpm -q --whatprovides 'perl(Class::Gomor)'
rpm -q --whatprovides 'perl(Class::Gomor::Hash)'
rpm -q --whatprovides 'perl(Class::Gomor::Array)'
perl -MClass::Gomor::Hash -MClass::Gomor::Array -e '
  use strict;
  use warnings;
  die "wrong installed version\n" unless $Class::Gomor::VERSION eq "1.03";
  { package OEHash;
    our @ISA = ("Class::Gomor::Hash");
    our @AS = ("value");
    our @AA = ("items");
    __PACKAGE__->cgBuildAccessorsScalar(\@AS);
    __PACKAGE__->cgBuildAccessorsArray(\@AA);
  }
  { package OEArray;
    our @ISA = ("Class::Gomor::Array");
    our @AS = ("value");
    our @AA = ("items");
    __PACKAGE__->cgBuildIndices;
    __PACKAGE__->cgBuildAccessorsScalar(\@AS);
    __PACKAGE__->cgBuildAccessorsArray(\@AA);
  }
  for my $class (qw(OEHash OEArray)) {
    my $root = $class->new(value => "base", items => ["one"]);
    die "$class accessor failed\n"
      unless $root->value eq "base" && join(",", $root->items) eq "one";
    my $clone = $root->cgClone;
    $clone->value("changed");
    die "$class shallow clone failed\n"
      unless $root->value eq "base" && $clone->value eq "changed";
    my $parent = $class->new(value => $root, items => ["two"]);
    my $deep = $parent->cgFullClone;
    die "$class nested full clone failed\n"
      unless ref($deep->value) eq $class
        && $deep->value != $root
        && $deep->value->value eq "base";
    print "$class installed behavior OK\n";
  }
'
