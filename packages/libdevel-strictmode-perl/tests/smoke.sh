#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
unset PERL_STRICT EXTENDED_TESTING AUTHOR_TESTING RELEASE_TESTING
perl -MDevel::StrictMode=STRICT,LAX -e 'die "default constants\n" unless !STRICT && LAX'
PERL_STRICT=1 perl -MDevel::StrictMode=STRICT,LAX -e 'die "strict constants\n" unless STRICT && !LAX'
printf '%s\n' 'ok 1 - installed Devel::StrictMode default and explicit strict constants'
