#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-module-find
fixture="$(mktemp -d)"
trap 'rm -f -- "$fixture/MFSmoke/Child.pm" "$fixture/MFSmoke/Child/Nested.pm"; rmdir -- "$fixture/MFSmoke/Child" "$fixture/MFSmoke" "$fixture"' EXIT
perl -MModule::Find - "$fixture" <<'PERL'
use strict;
use warnings;

my ($root) = @ARGV;
mkdir "$root/MFSmoke" or die "create namespace: $!";
mkdir "$root/MFSmoke/Child" or die "create child namespace: $!";
open my $direct, '>', "$root/MFSmoke/Child.pm" or die "create child: $!";
print {$direct} 'package MFSmoke::Child; sub marker { 42 } 1;';
close $direct or die "close child: $!";
open my $nested, '>', "$root/MFSmoke/Child/Nested.pm" or die "create nested child: $!";
print {$nested} 'package MFSmoke::Child::Nested; 1;';
close $nested or die "close nested child: $!";

local @INC = ($root, @INC);
setmoduledirs($root);
my @direct = findsubmod("MFSmoke");
my @recursive = findallmod("MFSmoke");
die "direct discovery" unless join(",", sort @direct) eq "MFSmoke::Child";
die "recursive discovery" unless join(",", sort @recursive) eq "MFSmoke::Child,MFSmoke::Child::Nested";
usesub("MFSmoke");
die "loading discovered module" unless MFSmoke::Child::marker() == 42;
print "installed Module::Find discovery and loading passed\n";
PERL
