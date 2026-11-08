#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-class-returnvalue
perl <<'PERL'
use strict;
use warnings;
use Class::ReturnValue;
die "version" unless $Class::ReturnValue::VERSION eq '0.55';
my $r=Class::ReturnValue->new;
$r->as_array('one','two');
my @a=$r->return_value;
die "list context" unless @a==2 && $a[0] eq 'one' && $a[1] eq 'two';
my $e=Class::ReturnValue->new;
$e->as_error(errno=>7,message=>'test error',do_backtrace=>1);
die "error context" if $e->return_value;
die "error fields" unless $e->errno==7 && $e->error_message eq 'test error';
die "stack trace" unless $e->backtrace=~/Trace begun/;
print "Class::ReturnValue smoke passed\n";
PERL
