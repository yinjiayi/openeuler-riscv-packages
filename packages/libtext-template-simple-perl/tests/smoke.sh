#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-text-template-simple
perl -MText::Template::Simple -e 'die unless $Text::Template::Simple::VERSION eq "0.91"'
test "$(tts -e 'openEuler-RISC-V')" = openEuler-RISC-V
printf '%s\n' 'installed Perl template module and tts renderer passed'
