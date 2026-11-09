#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
set -eu
tmp=$(mktemp -d)
trap 'rm -r "$tmp"' EXIT HUP INT TERM
printf '%s\n' 'root=/srv/data' 'child=$root/bin' 'nested[host]=test' 'literal=value\#tag # ignored' > "$tmp/test.conf"
perl -MConfig::File -e '
  my $c = Config::File::read_config_file(shift);
  die "substitution failed" unless $c->{child} eq "/srv/data/bin";
  print "ok - substitutes earlier variables\n";
  die "nested key failed" unless $c->{nested}{host} eq "test";
  print "ok - parses nested keys\n";
  die "escaped comment failed" unless $c->{literal} eq "value#tag";
  print "ok - preserves escaped comment marker\n";
' "$tmp/test.conf"
