#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
scratch="$(mktemp -d -- "${TMPDIR:-/tmp}/file-find-rule-ppi.XXXXXX")"
trap 'rm -f -- "$scratch/Marked.pm" "$scratch/Plain.pm"; rmdir -- "$scratch"' EXIT
printf '%s\n' 'package Marked;' '# parser marker' '1;' > "$scratch/Marked.pm"
printf '%s\n' 'package Plain;' '1;' > "$scratch/Plain.pm"
perl -MFile::Find::Rule -MFile::Find::Rule::PPI -e '
    my @matches = File::Find::Rule->file->name("*.pm")->ppi_find_any("Token::Comment")->relative->in($ARGV[0]);
    die "comment rule selected the wrong files" unless @matches == 1 && $matches[0] eq "Marked.pm";
    print "ok 1 - installed PPI rule selects only the commented source fixture\n";
' "$scratch"
