#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-MIME-tools
rpm -q --whatprovides 'perl(MIME::Parser)'
rpm -q --whatprovides 'perl(MIME::Entity)'
perl -MMIME::Parser -MMIME::Entity -MMIME::Tools -e '
  die "unexpected MIME-tools version\n" unless $MIME::Tools::VERSION eq "5.519";
  my $message = "From: sender\@example.invalid\nTo: reader\@example.invalid\nSubject: RVA23\nContent-Type: text/plain\n\nhello\n";
  my $parser = MIME::Parser->new;
  $parser->output_to_core(1);
  my $entity = $parser->parse_data($message);
  die "MIME::Entity unavailable\n" unless $entity->isa("MIME::Entity");
  die "MIME parse failed\n" unless $entity->bodyhandle->as_string eq "hello\n";
'
