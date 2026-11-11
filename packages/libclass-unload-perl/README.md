<!-- SPDX-License-Identifier: Apache-2.0 -->
# libclass-unload-perl

This directory packages upstream `https://metacpan.org/release/ILMARI/Class-Unload-0.12` version `0.12` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The original archive and complete Perl terms are retained. The generated
`Makefile.PL`, `README`, `MANIFEST` and POD author tests use Ricardo SIGNES's
Dist::Zilla 6.033 templates. The generated EOL and no-tabs author tests use
the Dist::Zilla Test::EOL 0.19 and Test::NoTabs 0.15 templates. The complete
license notices of all three donor releases are pinned and installed alongside
the original distribution license. The upstream source and tests are unmodified.

The standard MakeMaker test target runs the original default selection,
including taint-mode unloading and inheritance checks. Upstream retains four
author-only guards and an optional Moose integration guard. The current
target repositories supply the mandatory inputs; the Moose test can skip
itself when that optional module is absent. The installed smoke checks class
unloading, module-load entry removal, and nested namespace preservation.
