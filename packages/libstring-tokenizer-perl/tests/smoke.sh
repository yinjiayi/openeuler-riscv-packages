#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-Tokenizer
rpm -q --whatprovides 'perl(String::Tokenizer)'
perl -MString::Tokenizer -e '
  die "unexpected String::Tokenizer version\n"
    unless $String::Tokenizer::VERSION eq "0.06";
  my $tokens = String::Tokenizer->new("red blue", "");
  die "tokenization mismatch\n"
    unless join("|", $tokens->getTokens()) eq "red|blue";
  my $iterator = $tokens->iterator();
  die "iterator mismatch\n"
    unless $iterator->nextToken() eq "red"
       && $iterator->nextToken() eq "blue";
'
