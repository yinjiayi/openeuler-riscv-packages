#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libregexp-reggrp-perl
unset PERL5LIB PERLLIB PERL5OPT
/usr/bin/perl - <<'PERL'
use 5.010;
use strict;
use warnings;
use Regexp::RegGrp;

my $group = Regexp::RegGrp->new({reggrp => [
    { regexp => 'foo', replacement => 'one' },
    { regexp => 'bar', replacement => 'two' },
]});
my $input = 'foo bar';
my $copy = $group->exec(\$input);
die "wrong copy result" unless $copy eq 'one two' && $input eq 'foo bar';
$group->exec(\$input);
die "wrong in-place result" unless $input eq 'one two';

our $executed = 0;
my $error;
{
    local $@;
    eval {
        my $probe = Regexp::RegGrp->new({reggrp => [
            { regexp => '(?{$main::executed=1})x', replacement => 'y' },
        ]});
        my $value = 'x';
        $probe->exec(\$value);
    };
    $error = $@;
}
die "embedded code was executed" if $executed;
die "dynamic embedded code was not rejected" unless
    $error =~ /Eval-group not (?:allowed|permitted)/i;
print "installed grouped substitution and dynamic-code rejection passed\n";
PERL
