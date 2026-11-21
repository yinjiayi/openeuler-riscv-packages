#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Pod-Spell-CommonMistakes
perl <<'PERL'
use strict;
use warnings;
use File::Temp qw(tempfile);
use Pod::Spell::CommonMistakes qw(check_pod check_pod_case check_pod_all);
die "Unexpected version\n" unless $Pod::Spell::CommonMistakes::VERSION eq '1.002';
my ($handle, $path) = tempfile(UNLINK => 1);
print {$handle} "=pod\n\n=head1 DESCRIPTION\n\nrecieve OpenLdap\n\n=cut\n";
close $handle or die "Close fixture: $!";
my $spelling = check_pod($path);
die "Missing spelling correction\n" unless $spelling->{recieve} eq 'receive';
my $capitalization = check_pod_case($path);
die "Missing capitalization correction\n" unless $capitalization->{OpenLdap} eq 'OpenLDAP';
my $all = check_pod_all($path);
die "Combined check differs\n" unless $all->{recieve} eq 'receive' && $all->{OpenLdap} eq 'OpenLDAP';
open $handle, '>', $path or die "Open fixture: $!";
print {$handle} "Plain text without POD.\n";
close $handle or die "Close fixture: $!";
die "Non-POD input produced corrections\n" if keys %{check_pod_all($path)};
print "Pod::Spell::CommonMistakes smoke passed\n";
PERL
