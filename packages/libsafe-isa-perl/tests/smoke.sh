#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-safe-isa
perl -MSafe::Isa <<'PERL'
use strict;
use warnings;
{ package Local::Base; sub new { bless {}, shift } }
{ package Local::Child; our @ISA = ('Local::Base'); sub pair { return (3,7) } }
my $obj = Local::Child->new;
my $invalid = [];
die 'unexpected version' unless $Safe::Isa::VERSION eq '1.000010';
die 'valid object handling' unless $obj->$_isa('Local::Base') && $obj->$_can('pair');
die 'invalid object handling' if defined $invalid->$_isa('Local::Base');
die 'context lost' unless join(',', $obj->$_call_if_can('pair')) eq '3,7';
print "ok 1 - installed Safe::Isa guards non-objects and preserves list context\n";
PERL
