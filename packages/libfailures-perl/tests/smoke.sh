#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
perl -e '
    use strict;
    use warnings;
    use failures qw/io::read/;
    use custom::failures "Smoke::Error" => ["disk::read"];
    my ($first,$second);
    eval { failure::io::read->throw({msg=>"bad read",payload=>41}); };
    $first=$@;
    eval { Smoke::Error::disk::read->throw("custom read"); };
    $second=$@;
    die "missing original typed error" unless ref($first) eq "failure::io::read" && $first->isa("failure::io") && $first->msg eq "bad read" && $first->payload==41;
    die "missing custom typed error" unless ref($second) eq "Smoke::Error::disk::read" && $second->isa("failure::disk::read") && "$second" =~ /custom read/;
    print "ok 1 - installed typed exception preserves message and payload\nok 2 - installed custom exception preserves derived class and string\n";
'
