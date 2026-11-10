#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libjson-pointer-perl
perl -MJSON::Pointer -e '
  my $base = { "a/b" => { "~key" => 7 } };
  my $pointer = q{/a~1b/~0key};
  die "escaped pointer" unless JSON::Pointer->get($base, $pointer, 1) == 7;
  my $updated = JSON::Pointer->add($base, q{/a~1b/next}, 11);
  die "add changed original" if exists $base->{"a/b"}->{next};
  die "escaped parent" unless JSON::Pointer->get($updated, q{/a~1b/next}, 1) == 11;
  my ($removed, $old) = JSON::Pointer->remove($updated, $pointer);
  die "remove did not isolate clone"
      unless $old == 7 && !exists $removed->{"a/b"}->{"~key"}
      && JSON::Pointer->get($updated, $pointer, 1) == 7;
  print "installed JSON pointer escaping and copy-on-update passed\n";
'
