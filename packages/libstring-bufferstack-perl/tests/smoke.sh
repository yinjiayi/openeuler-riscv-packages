#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-BufferStack
rpm -q --whatprovides 'perl(String::BufferStack)'
perl -MString::BufferStack -e '
  die "unexpected version\n" unless $String::BufferStack::VERSION eq "1.16";
  my $output = "";
  my $stack = String::BufferStack->new(out_method => sub { $output .= join("", @_); });
  $stack->append("base");
  $stack->push(filter => sub { uc shift });
  $stack->append(" plus");
  $stack->pop;
  $stack->flush_output;
  die "nested filter/output mismatch\n" unless $output eq "base PLUS";
'
