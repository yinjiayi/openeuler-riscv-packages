#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
set -eu
perl -MConfig::Properties -e '
  my $config = Config::Properties->new;
  my $text = "enabled=yes\nworkers=4\n";
  open my $input, "<", \$text or die "open: $!";
  $config->load($input);
  die "incorrect initial value\n" unless $config->getProperty("enabled") eq "yes";
  $config->setProperty("workers", 8);
  my $saved = $config->saveToString;
  die "updated property not serialized\n" unless $saved =~ /^workers=8$/m;
  print "ok - staged property parse and update\n";
'
