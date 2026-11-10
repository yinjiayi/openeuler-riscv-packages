#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-text-context
perl -MText::Context -MText::Context::Para <<'PERL'
use strict;
use warnings;
my $snippet = Text::Context->new('A Perl & tools example', 'Perl');
my $text = $snippet->as_text;
my $html = $snippet->as_html(start => '<b>', end => '</b>');
die "missing text context\n" unless $text =~ /Perl/;
die "missing escaped highlight\n" unless $html =~ m{<b>Perl</b>\s+&amp;\s+tools};
print "installed escaped context highlight passed\n";
PERL
