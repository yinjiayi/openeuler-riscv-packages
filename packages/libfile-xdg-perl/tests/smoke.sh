#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-XDG
rpm -q --whatprovides 'perl(File::XDG)'
test_home="$(mktemp -d)"
trap 'rmdir -- "$test_home"' EXIT
env -u XDG_CONFIG_HOME -u XDG_DATA_HOME -u XDG_CACHE_HOME HOME="$test_home" perl -MFile::XDG -e '
  die "unexpected File::XDG version\n"
    unless $File::XDG::VERSION eq "1.03";
  my $xdg = File::XDG->new(name => "file-xdg-smoke");
  die "unexpected config directory\n"
    unless $xdg->config_home eq "$ENV{HOME}/.config/file-xdg-smoke";
'
