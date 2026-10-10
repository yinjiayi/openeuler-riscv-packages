#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Math-Expression-Evaluator
rpm -q --whatprovides 'perl(Math::Expression::Evaluator)'
perl -MMath::Expression::Evaluator -e '
  die "unexpected version\n" unless $Math::Expression::Evaluator::VERSION eq "0.3.2";
  my $e = Math::Expression::Evaluator->new("2+a*3");
  die "evaluation failed\n" unless $e->val({a => 4}) == 14;
  $e->optimize;
  die "optimization failed\n" unless $e->val({a => 4}) == 14;
  my $compiled = $e->compiled;
  die "compiled expression failed\n" unless $compiled->({a => 4}) == 14;
  eval { Math::Expression::Evaluator->new("2+") };
  die "invalid expression was accepted\n" unless $@;
'
