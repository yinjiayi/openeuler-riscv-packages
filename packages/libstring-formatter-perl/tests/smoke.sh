#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-Formatter
rpm -q --whatprovides 'perl(String::Formatter)'
rpm -q --whatprovides 'perl(String::Formatter::Cookbook)'
perl -MString::Formatter -MString::Formatter::Cookbook -e '
  die "unexpected version\n" unless $String::Formatter::VERSION eq "1.235";
  my $fmt = String::Formatter->new({ codes => { x => "fox", y => "yak" } });
  die "format result mismatch\n"
    unless $fmt->format("A:%x B:%y") eq "A:fox B:yak";
  my $accepted = eval { $fmt->format("%z"); 1 };
  die "unknown conversion was accepted\n" if $accepted;
  die "wrong unknown-conversion failure: $@\n"
    unless $@ =~ /Unknown conversion/i;
'
