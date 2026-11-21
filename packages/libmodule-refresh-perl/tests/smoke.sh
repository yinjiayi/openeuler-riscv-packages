#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-module-refresh
perl -MModule::Refresh -MFile::Temp=tempdir -e '
  my $dir = tempdir(CLEANUP => 1);
  unshift @INC, $dir;
  my $path = "$dir/LocalRefreshFixture.pm";
  sub write_fixture {
      open my $out, ">", $path or die $!;
      print {$out} "package LocalRefreshFixture; sub value { $_[0] } 1;\n";
      close $out or die $!;
  }
  write_fixture(1);
  require LocalRefreshFixture;
  die "initial fixture mismatch" unless LocalRefreshFixture::value() == 1;
  write_fixture(2);
  Module::Refresh->refresh_module("LocalRefreshFixture.pm");
  my $reloaded = LocalRefreshFixture->can("value");
  die "reload fixture mismatch" unless $reloaded && $reloaded->() == 2;
  print "ok 1 - installed Module::Refresh reloads a changed fixture\n";
'
