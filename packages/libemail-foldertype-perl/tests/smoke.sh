#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libemail-foldertype-perl
unset PERL5LIB PERLLIB PERL5OPT
fixture=$(mktemp -d)
trap 'rm -r -- "$fixture"' EXIT
mkdir -p "$fixture/maildir/cur" "$fixture/maildir/new" "$fixture/maildir/tmp" \
    "$fixture/mh" "$fixture/ez/archive"
printf 'From sender@example.invalid Mon Nov  9 00:00:00 2026\n\nfixture\n' > "$fixture/mbox"
/usr/bin/perl - "$fixture" <<'PERL'
use strict;
use warnings;
use Email::FolderType qw(folder_type);

my ($root) = @ARGV;
my @cases = (
    [ "$root/mbox", 'Mbox' ],
    [ "$root/maildir", 'Maildir' ],
    [ "$root/mh/.", 'MH' ],
    [ "$root/ez", 'Ezmlm' ],
);
for my $case (@cases) {
    my ($path, $expected) = @$case;
    my $got = folder_type($path);
    die "expected $expected for $path" unless defined $got && $got eq $expected;
}
print "installed four folder types passed\n";
PERL
