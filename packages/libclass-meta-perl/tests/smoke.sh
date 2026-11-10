#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libclass-meta-perl
perl -MClass::Meta -MClass::Meta::Types::Numeric -e '
    package Smoke::ClassMeta;
    my $class = Class::Meta->new(package => __PACKAGE__);
    $class->add_constructor(name => "new");
    $class->add_attribute(name => "whole", type => "whole", create => Class::Meta::GETSET);
    $class->build;
    my $object = __PACKAGE__->new;
    $object->whole(0);
    die "typed whole number did not round-trip zero\n"
        unless defined($object->whole) && $object->whole == 0;
    print "installed typed whole-number accepts zero\n";
'
