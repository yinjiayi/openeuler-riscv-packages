#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-BOM
rpm -q --whatprovides 'perl(File::BOM)'
perl -MFile::BOM=decode_from_bom -e '
  die "unexpected File::BOM version\n" unless $File::BOM::VERSION eq "0.18";
  my ($text, $encoding) = decode_from_bom("\xEF\xBB\xBFhello");
  die "UTF-8 BOM was not decoded\n" unless $text eq "hello" && $encoding eq "UTF-8";
'
