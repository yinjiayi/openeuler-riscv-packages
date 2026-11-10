#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-digest-md5-file
scratch_dir=$(mktemp -d)
trap 'rm -f -- "$scratch_dir/plain" "$scratch_dir/literal|"; rmdir -- "$scratch_dir"' EXIT
printf '%s' abc > "$scratch_dir/plain"
printf '%s' abc > "$scratch_dir/literal|"
perl -MDigest::MD5::File -e '
    die "unexpected module version\n" unless $Digest::MD5::File::VERSION eq "0.08";
    for my $filename (@ARGV) {
        die "incorrect literal filename digest\n"
            unless Digest::MD5::File::file_md5_hex($filename) eq "900150983cd24fb0d6963f7d28e17f72";
    }
    print "ok - installed plain and literal pipe-suffix filename digests\n";
' "$scratch_dir/plain" "$scratch_dir/literal|"
