#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-ShareDir-Dist
rpm -q --whatprovides 'perl(File::ShareDir::Dist)'
perl -MApp::Prove::Plugin::ShareDirDist -MApp::Yath::Plugin::ShareDirDist -MFile::ShareDir::Dist::Install -e '1'
perl -MFile::ShareDir::Dist=dist_share -MFile::Temp=tempdir -e '
  die "unexpected version\n" unless $File::ShareDir::Dist::VERSION eq "0.07";
  my $root = tempdir(CLEANUP => 1);
  $ENV{PERL_FILE_SHAREDIR_DIST} = "Example-Dist=$root";
  die "shared directory lookup failed\n" unless dist_share("Example::Dist") eq $root;
'
