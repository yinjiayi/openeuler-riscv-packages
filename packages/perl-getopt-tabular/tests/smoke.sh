#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-getopt-tabular
perl -MGetopt::Tabular -e '
use strict; use warnings;
die "version" unless $Getopt::Tabular::VERSION == 0.3;
my ($number, $name, $flag); my @rest;
my @options = (["-number", "integer", 1, \$number, "integer"], ["-name", "string", 1, \$name, "name"], ["-flag", "boolean", 0, \$flag, "flag"]);
my @args = ("left", "-number", "7", "-name", "sample", "-flag", "right");
die "parse" unless GetOptions(\@options, \@args, \@rest);
die "values" unless $number == 7 && $name eq "sample" && $flag;
die "leftovers" unless join(",", @rest) eq "left,right";
die "original args" unless @args == 7;
print "GetoptTabular installed API smoke passed\n";
'
