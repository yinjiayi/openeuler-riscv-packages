#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
scratch="$(mktemp -d -- "${TMPDIR:-/tmp}/parse-gitignore.XXXXXX")"
trap 'rm -f -- "$scratch/.gitignore" "$scratch/output.cache" "$scratch/retained.txt"; rmdir -- "$scratch"' EXIT
printf '%s\n' '*.cache' > "$scratch/.gitignore"
printf '%s\n' 'generated' > "$scratch/output.cache"
printf '%s\n' 'retained' > "$scratch/retained.txt"
(
    cd "$scratch"
    perl -MParse::Gitignore -e '
        my $rules = Parse::Gitignore->new($ARGV[0]);
        die "glob missed the generated file" unless $rules->ignored("output.cache");
        die "ordinary file was unexpectedly ignored" if $rules->ignored("retained.txt");
        print "ok 1 - installed ignore parser distinguishes matching and ordinary files\n";
    ' "$scratch/.gitignore"
)
