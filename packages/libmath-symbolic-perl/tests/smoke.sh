#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Math-Symbolic
rpm -q --whatprovides 'perl(Math::Symbolic)'
perl -MMath::Symbolic -e '
  die "unexpected version\n" unless $Math::Symbolic::VERSION eq "0.613";
  my $tree = Math::Symbolic->parse_from_string("2+3*4");
  die "default parser/evaluator failed\n" unless $tree->value == 14;
  my $bad = Math::Symbolic->parse_from_string("2+");
  die "invalid expression was accepted\n" if defined $bad;
'
perl -MMath::Symbolic -MMath::Symbolic::Parser::Yapp -e '
  $Math::Symbolic::Parser = Math::Symbolic::Parser::Yapp->new();
  my $tree = Math::Symbolic->parse_from_string("2+3*4");
  die "standalone Yapp parser failed\n" unless $tree->value == 14;
'
