#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Tie-ToObject
perl <<'PERL'
use strict;
use warnings;
use Scalar::Util qw(refaddr);
use Tie::RefHash;
use Tie::ToObject;
die "version" unless $Tie::ToObject::VERSION eq '0.03';
tie my %original, 'Tie::RefHash';
$original{value} = 3;
my $object = tied %original;
tie my %alias, 'Tie::ToObject', $object;
die "object identity" unless refaddr(tied %alias) == refaddr($object);
die "read through alias" unless $alias{value} == 3;
$alias{value} = 7;
die "write through alias" unless $original{value} == 7;
eval { Tie::ToObject->TIEHASH({}) };
die "non-object accepted" unless $@ =~ /object.*tie/i;
eval { Tie::ToObject->unsupported($object) };
die "unsupported method accepted" unless $@ =~ /method.*unsupported/i;
print "Tie::ToObject installed API checks passed\n";
PERL
