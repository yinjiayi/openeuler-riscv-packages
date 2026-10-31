#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-IO-Tee
perl -MIO::Tee -e 'my ($a,$b)=("",""); open my $f, ">", \$a or die; open my $g, ">", \$b or die; my $t=IO::Tee->new($f,$g); print {$t} "hello"; $t->flush; die "tee failed" unless $a eq "hello" && $b eq "hello";'
