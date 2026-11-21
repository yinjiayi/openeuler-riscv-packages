#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libio-dirent-perl
unset PERL5LIB PERLLIB PERL5OPT
fixture=$(mktemp -d)
trap 'rm -r -- "$fixture"' EXIT
mkdir "$fixture/folder"
touch "$fixture/file"
/usr/bin/perl - "$fixture" <<'PERL'
use strict;
use warnings;
use IO::Dirent qw(readdirent nextdirent DT_DIR DT_REG);

my ($fixture) = @ARGV;
my %expected = (folder => DT_DIR, file => DT_REG);
opendir(my $bulk, $fixture) or die "opendir: $!";
my %read = map { $_->{name} => $_->{type} } readdirent($bulk);
closedir($bulk) or die "closedir: $!";
opendir(my $single, $fixture) or die "opendir: $!";
my %walk;
while (my $entry = nextdirent($single)) {
    $walk{$entry->{name}} = $entry->{type};
}
closedir($single) or die "closedir: $!";
for my $name (keys %expected) {
    die "missing or incorrect entry type for $name" unless
        defined $read{$name} && $read{$name} == $expected{$name} &&
        defined $walk{$name} && $walk{$name} == $expected{$name};
}
print "installed XS directory enumeration and file types passed\n";
PERL
