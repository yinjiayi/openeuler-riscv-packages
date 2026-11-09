#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
set -eu
tmp=$(mktemp -d)
trap 'rm -r "$tmp"' EXIT HUP INT TERM
cd "$tmp"
printf '%s\n' 'print "script stdout\n";' 'print STDERR "script stderr\n";' > fixture.pl
perl -MTest::Script -MTest2::API=intercept -e '
  my $events = intercept {
    script_compiles("./fixture.pl", "installed Test::Script compiles fixture");
    script_runs("./fixture.pl", "installed Test::Script runs fixture");
    script_stdout_is("script stdout\n", "captured fixture stdout");
    script_stderr_is("script stderr\n", "captured fixture stderr");
  };
  my @checks = grep { $_->isa("Test2::Event::Ok") } @$events;
  die "expected four assertions" unless @checks == 4;
  for my $event (@checks) {
    die "failed: " . $event->name unless $event->pass;
    print "ok - ", $event->name, "\n";
  }
'
