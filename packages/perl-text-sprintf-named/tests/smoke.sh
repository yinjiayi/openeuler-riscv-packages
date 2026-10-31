#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Text-Sprintf-Named
perl -MText::Sprintf::Named -e 'my $o=Text::Sprintf::Named->new({fmt=>q{Hello %(name)s!}}); die "format failed" unless $o->format({args=>{name=>q{world}}}) eq q{Hello world!};'
