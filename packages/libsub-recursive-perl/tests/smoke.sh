#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-sub-recursive
perl -MSub::Recursive=:ALL -e '
    die "unexpected Sub::Recursive version\n" unless $Sub::Recursive::VERSION eq "0.05";
    my $factorial = recursive { $_[0] < 2 ? 1 : $_[0] * $REC->($_[0] - 1) };
    my ($odd, $even) = mutually_recursive(
        odd  => sub { $_[0] == 0 ? 0 : $REC{even}->($_[0] - 1) },
        even => sub { $_[0] == 0 ? 1 : $REC{odd}->($_[0] - 1) },
    );
    die "incorrect recursive result\n"
        unless $factorial->(6) == 720 && $odd->(7) && $even->(8) && !$even->(7);
    print "ok - installed factorial and mutually recursive parity\n";
'
