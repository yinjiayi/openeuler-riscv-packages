#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-lingua-en-namecase
perl -MLingua::EN::NameCase=NameCase,nc -e '
use strict; use warnings;
die "version" unless $Lingua::EN::NameCase::VERSION eq "1.21";
die "prefix" unless nc("john mcvey") eq "John McVey";
die "exception" unless nc("machado") eq "Machado";
die "roman" unless nc("louis xiv") eq "Louis XIV";
my @original = ("nancy", "drew");
my @out = NameCase(@original);
die "list" unless join("|", @out) eq "Nancy|Drew";
die "input mutation" unless join("|", @original) eq "nancy|drew";
NameCase(\@original);
die "in-place" unless join("|", @original) eq "Nancy|Drew";
print "NameCase installed API smoke passed\n";
'
