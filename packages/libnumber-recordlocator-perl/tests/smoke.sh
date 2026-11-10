#!/usr/bin/env bash
set -euo pipefail

perl -MNumber::RecordLocator -e '
    die "wrong installed version" unless $Number::RecordLocator::VERSION eq "0.005";
    my $n = Number::RecordLocator->new;
    die "wrong locator" unless $n->encode(123456) eq "5RL2";
    die "wrong round trip" unless $n->decode("5RL2") == 123456;
    print "ok 1 - installed Number::RecordLocator round-trips record locators\n";
'
