#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
work=$(mktemp -d)
trap 'rm -f "$work/META.json"; rmdir "$work"' EXIT
printf '%s\n' '{"name":"Local-Fixture","version":"1.00","abstract":"Synthetic package metadata","author":["Package Test"],"license":["artistic_2"],"dynamic_config":0,"release_status":"stable","meta-spec":{"version":2,"url":"https://metacpan.org/pod/CPAN::Meta::Spec"},"generated_by":"local packaging smoke"}' > "$work/META.json"
perl -MTest::More=tests,3 -MTest::CPAN::Meta::JSON -e '
    my $meta = meta_spec_ok($ARGV[0], "2");
    is($meta->{name}, "Local-Fixture", "installed validator returns parsed metadata");
' "$work/META.json"
