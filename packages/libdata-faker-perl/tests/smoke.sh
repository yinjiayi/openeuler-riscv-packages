#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-Faker
rpm -q --whatprovides 'perl(Data::Faker)'
perl -MData::Faker -e '
  die "unexpected Data::Faker version\n"
    unless $Data::Faker::VERSION eq "0.10";
  my $faker = Data::Faker->new;
  die "missing built-in first_name method\n"
    unless grep { $_ eq "first_name" } $faker->methods;
  my $name = $faker->first_name;
  die "empty generated name\n" unless defined($name) && length($name);
'
types="$(datafaker --datatypes)"
[[ "$types" == *first_name* ]]
sample="$(datafaker first_name last_name)"
[[ "$sample" == *' '* ]]
