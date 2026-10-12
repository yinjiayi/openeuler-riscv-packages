#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-CSV-Encoded
rpm -q --whatprovides 'perl(Text::CSV::Encoded)'

for backend in 0 1; do
  PERL_TEXT_CSV="$backend" perl -MText::CSV::Encoded -e '
    die "unexpected version\n" unless $Text::CSV::Encoded::VERSION eq "0.25";
    my $selected = $ENV{PERL_TEXT_CSV};
    die "wrong CSV backend\n" unless $selected
      ? Text::CSV::Encoded->is_xs : Text::CSV::Encoded->is_pp;
    my $csv = Text::CSV::Encoded->new({
      encoding_in => "latin1", encoding_out => "utf8"
    });
    die "CSV object unavailable\n" unless $csv;
    my $fields = $csv->decode("latin1", "caf\xe9");
    die "Latin-1 decode failed\n"
      unless @$fields == 1 && $fields->[0] eq "caf" . chr(0xe9);
    my $encoded = $csv->encode("utf8", $fields);
    die "UTF-8 encode failed\n" unless $encoded eq "caf\xc3\xa9";
  '
done
