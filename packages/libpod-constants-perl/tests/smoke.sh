#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libpod-constants-perl
unset PERL5LIB PERLLIB PERL5OPT
fixture=$(mktemp)
trap 'rm -f -- "$fixture"' EXIT
printf '%s\n' '=head2 Fixture' '' 'retained text' '' '=head2 Ignored' '' 'unexpected text' '' '=cut' > "$fixture"
/usr/bin/perl - "$fixture" <<'PERL'
use strict;
use warnings;
use Pod::Constants ();

my $text;
Pod::Constants::import_from_file($ARGV[0], -trim => 1, Fixture => \$text);
die "unexpected POD section text" unless defined($text) && $text eq 'retained text';
print "installed POD section extraction passed\n";
PERL
