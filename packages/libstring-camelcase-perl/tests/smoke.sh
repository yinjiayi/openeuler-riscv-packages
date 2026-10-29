#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-CamelCase
rpm -q --whatprovides 'perl(String::CamelCase)'
perl -MString::CamelCase=camelize,decamelize,wordsplit -e '
  die "unexpected String::CamelCase version\n"
    unless $String::CamelCase::VERSION eq "0.04";
  die "camelize mismatch\n" unless camelize("some_keyword") eq "SomeKeyword";
  die "decamelize mismatch\n" unless decamelize("SomeKeyword") eq "some_keyword";
  die "word split mismatch\n"
    unless join(",", wordsplit("SomeKeyword")) eq "Some,Keyword";
'
