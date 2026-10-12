#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-URI-Nested
rpm -q --whatprovides 'perl(URI::Nested)'
perl -MURI::Nested -e '
  die "wrong URI::Nested version\n" unless $URI::Nested::VERSION eq "0.10";
  my $uri = URI::Nested->new("http://example.com/a");
  die "direct module load or nested parse failed\n"
    unless $uri->nested_uri->scheme eq "http"
      && $uri->nested_uri->host eq "example.com"
      && $uri->nested_uri->path eq "/a"
      && $uri->as_string eq "Nested:http://example.com/a";
'
