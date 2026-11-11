#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-IO-File-WithFilename
perl -MFile::Temp -MIO::File::WithFilename -e 'my $t = File::Temp->new; my $f = IO::File::WithFilename->new($t->filename, 0); die "filename mismatch" unless $f && $f->filename eq $t->filename;'
