#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-YAML
rpm -q --whatprovides 'perl(Data::YAML::Reader)'
perl -MData::YAML -MData::YAML::Reader -MData::YAML::Writer -e '
  die "unexpected Data::YAML version\n"
    unless $Data::YAML::VERSION eq "0.0.7";
  my $input = { alpha => [1, 2], beta => "ok" };
  my $yaml = "";
  Data::YAML::Writer->new->write($input, \$yaml);
  my $output = Data::YAML::Reader->new->read($yaml);
  die "installed YAML round-trip failed\n"
    unless $output->{alpha}[1] == 2 && $output->{beta} eq "ok";
'
