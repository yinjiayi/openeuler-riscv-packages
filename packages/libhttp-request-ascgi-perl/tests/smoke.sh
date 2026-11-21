#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libhttp-request-ascgi-perl
/usr/bin/perl - <<'PERL'
use strict;
use warnings;
use HTTP::Request;
use HTTP::Request::AsCGI;

my $request = HTTP::Request->new(GET => 'http://example.invalid/probe?q=42');
my $cgi = HTTP::Request::AsCGI->new($request)->setup;
my $env_ok = $ENV{REQUEST_METHOD} eq 'GET'
    && $ENV{PATH_INFO} eq '/probe' && $ENV{QUERY_STRING} eq 'q=42';
print "Status: 201 Created\nContent-Type: text/plain\n\naccepted";
my $response = $cgi->restore->response;
die "unexpected CGI environment\n" unless $env_ok;
die "unexpected CGI response\n"
    unless $response->code == 201 && $response->content eq 'accepted';
print "installed CGI request and response passed\n";
PERL
