#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-Transformer
rpm -q --whatprovides 'perl(Data::Transformer)'
perl -MData::Transformer -e '
  die "unexpected Data::Transformer version\n"
    unless $Data::Transformer::VERSION eq "0.04";
  my $data = { name => "sample" };
  my $transformer = Data::Transformer->new(
    normal => sub { ${$_[0]} = uc ${$_[0]} }
  );
  $transformer->traverse($data);
  die "installed traversal failed\n" unless $data->{name} eq "SAMPLE";
'
