#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libclass-pluggable-perl
unset PERL5LIB PERLLIB PERL5OPT
/usr/bin/perl - <<'PERL'
use strict;
use warnings;
use Class::Pluggable;

{
    package FixturePlugin;
    our @EXPORT_AS_PLUGIN = qw(plugin_value);
    sub plugin_value { 42 }
    sub on_fixture { $_[0]{hook_ran}++ }
}
my $obj = bless {}, 'Class::Pluggable';
$obj->add_plugin('FixturePlugin');
die "unexpected registered plugin" unless join(',', $obj->get_plugins) eq 'FixturePlugin';
die "unexpected plugin result" unless $obj->plugin_value == 42;
$obj->add_hook('fixture', 'on_fixture');
$obj->run_hook('fixture');
die "registered hook was not called" unless $obj->{hook_ran} == 1;
print "installed registered plugin dispatch passed\n";
PERL
