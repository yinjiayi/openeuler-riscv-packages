#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Test-ClassAPI
rpm -q --whatprovides 'perl(Test::ClassAPI)'
perl -MTest::ClassAPI -MTest::More - <<'PERL'
die "unexpected Test::ClassAPI version\n"
  unless $Test::ClassAPI::VERSION eq '1.07';
{
  package SmokeClass;
  sub ping { 1 }
}
Test::More->builder->plan(tests => 2);
Test::ClassAPI->execute;
__DATA__
SmokeClass=class

[SmokeClass]
ping=method
PERL
