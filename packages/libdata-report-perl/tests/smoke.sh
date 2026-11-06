#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-Report
rpm -q --whatprovides 'perl(Data::Report)'
rpm -q --whatprovides 'perl(Data::Report::Plugin::Csv)'
perl -MData::Report -e '
  die "unexpected Data::Report version\n"
    unless $Data::Report::VERSION eq "1.001";
  my $text = Data::Report->create(type => "text", layout => [
    { name => "name", title => "Name", width => 20 },
  ]);
  my $text_out = "";
  $text->set_output(\$text_out);
  $text->start;
  $text->add({ name => "report-smoke" });
  $text->finish;
  $text->close;
  die "text report output missing\n" unless $text_out =~ /report-smoke/;
  my $csv = Data::Report->create(type => "csv", layout => [
    { name => "name", title => "Name", width => 20 },
  ]);
  my $csv_out = "";
  $csv->set_output(\$csv_out);
  $csv->start;
  $csv->add({ name => "report-smoke" });
  $csv->finish;
  $csv->close;
  die "CSV report output missing\n" unless $csv_out =~ /report-smoke/;
'
