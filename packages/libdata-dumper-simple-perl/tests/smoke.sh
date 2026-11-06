#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-Dumper-Simple
rpm -q --whatprovides 'perl(Data::Dumper::Simple)'
perl -MData::Dumper::Simple -e '
  die "unexpected Data::Dumper::Simple version\n"
    unless $Data::Dumper::Simple::VERSION eq "0.11";
'

# Filter::Simple transforms source files, not Perl -e or stdin snippets.
smoke_script="$(mktemp)"
trap 'rm -f -- "$smoke_script"' EXIT
printf '%s\n' \
  'use Data::Dumper::Simple;' \
  'my $value = 7;' \
  'my $dump = Dumper($value);' \
  'die "source filter dump mismatch\n" unless $dump eq "\$value = 7;\n";' \
  > "$smoke_script"
perl "$smoke_script"
