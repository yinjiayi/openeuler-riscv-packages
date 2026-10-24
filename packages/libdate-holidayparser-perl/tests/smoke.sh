#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Date-HolidayParser
rpm -q --whatprovides 'perl(Date::HolidayParser)'
rpm -q --whatprovides 'perl(Date::HolidayParser::iCalendar)'
perl -MDate::HolidayParser -MDate::HolidayParser::iCalendar -MFile::Temp -e '
  my $fixture = File::Temp->new;
  print {$fixture} qq{"Probe" on 17.5\n};
  close $fixture;
  my $parser = Date::HolidayParser->new("$fixture");
  die "base parser missed holiday\n" unless exists $parser->get(2006)->{5}{17}{Probe};
  my $calendar = Date::HolidayParser::iCalendar->new("$fixture");
  die "calendar missed holiday\n" unless grep { $_ == 17 } @{$calendar->get_monthinfo(2006, 5)};
  print "installed base parser and iCalendar OK\n";
'
