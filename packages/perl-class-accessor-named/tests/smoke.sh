#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-class-accessor-named
perl <<'PERL'
use strict;
use warnings;
use Class::Accessor::Named;
use Sub::Util qw(subname);

{
    package NamedProbe;
    use base 'Class::Accessor';
    __PACKAGE__->mk_accessors('answer');
}
{
    package NamedFastProbe;
    use base 'Class::Accessor::Fast';
    __PACKAGE__->mk_accessors('answer');
}
for my $class (qw(NamedProbe NamedFastProbe)) {
    my $object = $class->new({answer => 42});
    die "wrong profiler name for $class\n" unless
        subname($class->can('answer')) eq $class . '::answer';
    die "wrong value for $class\n" unless $object->answer() == 42;
    $object->answer(17);
    die "setter failed for $class\n" unless $object->answer() == 17;
}
PERL
