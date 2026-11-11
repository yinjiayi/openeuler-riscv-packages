#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-any-uri-escape
rpm -q --whatprovides 'perl(Any::URI::Escape)'
perl -MAny::URI::Escape -e '
  die "unexpected Any::URI::Escape version\n"
    unless $Any::URI::Escape::VERSION eq "0.01";
  my $original = "a+b %/?#";
  my $escaped = uri_escape($original);
  die "URI encoding mismatch: $escaped\n"
    unless $escaped eq "a%2Bb%20%25%2F%3F%23";
  die "URI decoding failed\n" unless uri_unescape($escaped) eq $original;
'
