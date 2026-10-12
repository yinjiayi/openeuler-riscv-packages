#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-HTTP-Headers-Fast
rpm -q --whatprovides 'perl(HTTP::Headers::Fast)'
perl -MHTTP::Headers::Fast -e '
  die "wrong HTTP::Headers::Fast version\n"
    unless $HTTP::Headers::Fast::VERSION eq "0.22";
  my $headers = HTTP::Headers::Fast->new;
  $headers->header("Content-Type" => "text/plain");
  die "header access failed\n"
    unless $headers->header("Content-Type") eq "text/plain";
  my $flattened = $headers->psgi_flatten;
  die "PSGI flatten failed\n"
    unless @$flattened == 2
      && $flattened->[0] eq "Content-Type"
      && $flattened->[1] eq "text/plain";
  $headers->date(0);
  die "date conversion failed\n" unless $headers->date == 0;
  $headers->authorization_basic("user", "pass");
  my ($user, $pass) = $headers->authorization_basic;
  die "basic authorization failed\n"
    unless $user eq "user" && $pass eq "pass";
  my $copy = $headers->clone;
  die "header clone failed\n"
    unless $copy->header("Content-Type") eq "text/plain";
'
