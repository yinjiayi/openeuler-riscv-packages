#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-MicroTemplate
rpm -q --whatprovides 'perl(Text::MicroTemplate)'
rpm -q --whatprovides 'perl(Text::MicroTemplate::File)'
perl -MText::MicroTemplate=render_mt -MText::MicroTemplate::File -e '
  die "unexpected version\n" unless $Text::MicroTemplate::VERSION eq "0.24";
  my $out = render_mt(q{Hello, <?= $_[0] ?>}, q{RISC-V})->as_string;
  die "render mismatch\n" unless $out eq q{Hello, RISC-V};
  my $escaped = render_mt(q{<?= $_[0] ?>}, q{<node>})->as_string;
  die "HTML escaping mismatch\n" unless $escaped eq q{&lt;node&gt;};
'
