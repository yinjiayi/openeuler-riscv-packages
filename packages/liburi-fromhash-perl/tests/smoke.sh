#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-URI-FromHash
rpm -q --whatprovides 'perl(URI::FromHash)'
perl -MURI::FromHash=uri,uri_object -MURI -e '
  die "wrong URI::FromHash version\n"
    unless $URI::FromHash::VERSION eq "0.05";
  my $text = uri(
    scheme => "https", host => "example.org", path => "/alpha",
    query => { k => "v" }
  );
  die "URI construction failed\n"
    unless $text eq "https://example.org/alpha?k=v";
  my $parsed = URI->new($text);
  die "URI parse/round-trip failed\n"
    unless $parsed->scheme eq "https"
      && $parsed->host eq "example.org"
      && $parsed->path eq "/alpha"
      && $parsed->query eq "k=v"
      && $parsed->as_string eq $text;
  my $object = uri_object(scheme => "http", host => "example.org");
  die "URI object return path failed\n"
    unless $object->isa("URI")
      && $object->scheme eq "http"
      && $object->host eq "example.org";
'
