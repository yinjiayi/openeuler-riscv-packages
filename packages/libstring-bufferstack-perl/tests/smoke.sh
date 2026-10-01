#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-BufferStack
rpm -q --whatprovides 'perl(String::BufferStack)'
perl -MString::BufferStack -e '
  die "unexpected version\n" unless $String::BufferStack::VERSION eq "1.16";
  my $output = "";
  my $stack = String::BufferStack->new(out_method => sub { $output .= join "", @_ });
  $stack->append("root");
  $stack->push;
  $stack->append("-nested");
  die "wrong nested buffer\n" unless $stack->buffer eq "root-nested";
  $stack->pop;
  $stack->flush;
  die "wrong flushed output\n" unless $output eq "root-nested";
  die "buffer not cleared\n" unless $stack->buffer eq "";
'
