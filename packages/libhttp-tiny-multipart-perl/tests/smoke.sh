#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-HTTP-Tiny-Multipart
rpm -q --whatprovides 'perl(HTTP::Tiny::Multipart)'
perl -MHTTP::Tiny -MHTTP::Tiny::Multipart -e '
  die "wrong HTTP::Tiny::Multipart version\n"
    unless $HTTP::Tiny::Multipart::VERSION eq "0.08";
  no warnings "redefine";
  *HTTP::Tiny::request = sub { return @_ };
  my $ua = HTTP::Tiny->new;
  my ($object, $method, $url, $args) =
    $ua->post_multipart("https://example.invalid/upload", [field => "value"]);
  die "wrong mocked request\n"
    unless $method eq "POST" && $url eq "https://example.invalid/upload";
  die "missing multipart content type\n"
    unless $args->{headers}{"content-type"} =~ /\Amultipart\/form-data; boundary=/;
  die "missing multipart field\n"
    unless $args->{content} =~ /name="field"/ && $args->{content} =~ /value/;
'
