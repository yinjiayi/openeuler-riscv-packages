#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
work=$(mktemp -d)
trap 'rm -f "$work/META.yml"; rmdir "$work"' EXIT
printf '%s\n' '--- #YAML:1.0' \
    'name: Local-Fixture' 'version: 1.00' 'abstract: Synthetic package metadata' \
    'author:' '  - Package Test' 'license: perl' 'distribution_type: module' \
    'requires: {}' 'meta-spec:' '  version: 1.3' \
    '  url: http://module-build.sourceforge.net/META-spec-v1.3.html' \
    'generated_by: local packaging smoke' > "$work/META.yml"
perl -MTest::More=tests,3 -MTest::CPAN::Meta -e '
    my $meta = meta_spec_ok($ARGV[0], "1.3");
    is($meta->{name}, "Local-Fixture", "installed validator returns parsed metadata");
' "$work/META.yml"
