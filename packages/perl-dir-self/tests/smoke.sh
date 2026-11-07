#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Dir-Self
perl -MDir::Self -MFile::Spec -e 'die "version" unless $Dir::Self::VERSION eq "0.11"; die "directory" unless __DIR__ eq File::Spec->rel2abs(".");'
perl -MDir::Self=:static -MFile::Spec -e 'die "static directory" unless __DIR__ eq File::Spec->rel2abs(".");'
