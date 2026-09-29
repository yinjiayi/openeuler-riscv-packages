#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-MailTools
perl -MMailTools -MMail::Mailer -MMail::Header -e '
  die "unexpected MailTools version\n" unless $MailTools::VERSION eq "2.22";
  my $header = Mail::Header->new;
  $header->add(Subject => "RVA23");
  die "header round-trip failed\n" unless $header->get("Subject") eq "RVA23\n";
  die "Mail::Mailer unavailable\n" unless Mail::Mailer->new;
'
