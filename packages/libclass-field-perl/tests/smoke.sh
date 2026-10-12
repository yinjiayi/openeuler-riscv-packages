#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Class-Field
rpm -q --whatprovides 'perl(Class::Field)'
perl -MClass::Field -e '
  die "wrong installed version\n" unless $Class::Field::VERSION eq "0.24";
  { package OEField; use Class::Field qw(field const); field "value" => "seed"; const "kind" => "field"; }
  my $object = bless {}, "OEField";
  die "default accessor failed\n" unless $object->value eq "seed";
  $object->value("updated");
  die "setter/getter failed\n" unless $object->value eq "updated";
  die "constant failed\n" unless $object->kind eq "field";
'
