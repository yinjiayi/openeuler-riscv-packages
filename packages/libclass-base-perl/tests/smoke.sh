#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Class-Base
rpm -q --whatprovides 'perl(Class::Base)'
perl -MClass::Base -e '
  die "wrong installed version\n" unless $Class::Base::VERSION eq "0.09";
  my $base = Class::Base->new(id => "original");
  die "constructor failed\n" unless $base->id eq "original";
  my $copy = $base->clone;
  die "clone failed\n" unless ref($copy) eq "Class::Base"
    && $copy != $base && $copy->id eq "original";
  $copy->id("copy");
  die "clone aliasing\n" unless $base->id eq "original" && $copy->id eq "copy";
  $base->error("expected error");
  die "error handling failed\n" unless $base->error eq "expected error";
'
