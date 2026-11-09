#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-text-shellwords
perl -MText::Shellwords <<'PERL'
use strict;
use warnings;
my @tokens = shellwords(q{echo "two words" one\ two | done});
die "wrong tokenization" unless join("\x1f", @tokens) eq
    join("\x1f", "echo", "two words", "one two", "|", "done");
print "ok 1 - installed Text::Shellwords preserves quotes, escaped spaces and literal pipe tokens\n";
PERL
