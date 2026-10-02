#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-HTTP-Parser
rpm -q --whatprovides 'perl(HTTP::Parser)'
perl -MHTTP::Parser -MHTTP::Request -MHTTP::Response -e '
  die "unexpected HTTP::Parser version\n" unless $HTTP::Parser::VERSION eq "0.06";
  my $request = HTTP::Parser->new;
  die "request not complete\n" unless $request->add("GET /hello HTTP/1.1\r\nHost: example.org\r\n\r\n") == 0;
  die "request method mismatch\n" unless $request->request->method eq "GET";
  die "request path mismatch\n" unless $request->request->uri->path eq "/hello";
  my $response = HTTP::Parser->new(response => 1);
  die "response not complete\n" unless $response->add("HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK") == 0;
  die "response body mismatch\n" unless $response->object->content eq "OK";
'
