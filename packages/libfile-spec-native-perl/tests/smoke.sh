#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Spec-Native
rpm -q --whatprovides 'perl(File::Spec::Native)'
perl -MFile::Spec -MFile::Spec::Native -e '
  die "unexpected File::Spec::Native version\n"
    unless $File::Spec::Native::VERSION eq "1.004";
  my @parts = qw(native path.txt);
  die "native catfile differs\n"
    unless File::Spec::Native->catfile(@parts) eq File::Spec->catfile(@parts);
'
