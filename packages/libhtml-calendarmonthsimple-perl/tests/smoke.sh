#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-HTML-CalendarMonthSimple
perl -MHTML::CalendarMonthSimple -e 'my $c = HTML::CalendarMonthSimple->new(year => 2010, month => 7); die "calendar" unless $c->Days_in_Month == 31'
