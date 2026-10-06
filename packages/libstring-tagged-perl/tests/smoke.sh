#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-Tagged
rpm -q --whatprovides 'perl(String::Tagged)'
perl -MString::Tagged -e '
  die "unexpected version\n" unless $String::Tagged::VERSION eq "0.24";
  my $s = String::Tagged->new("Hello, world");
  $s->apply_tag(0, 5, emphasis => 1);
  die "plain string mismatch\n" unless $s->str eq "Hello, world";
  die "tag mismatch\n" unless $s->get_tag_at(1, "emphasis") == 1;
  die "unexpected tag\n" if defined $s->get_tag_at(7, "emphasis");
  $s->set_substr(7, 5, "there");
  die "mutation mismatch\n" unless $s->str eq "Hello, there";
'
